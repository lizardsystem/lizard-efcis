# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, timedelta
from itertools import groupby
import logging

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.text import slugify
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
import numpy as np

from lizard_efcis import export_data
from lizard_efcis import models
from lizard_efcis import serializers
from lizard_efcis import tasks
from lizard_efcis.manager import UNRELIABLE
from lizard_efcis.manager import VALIDATED
from lizard_efcis.manager import VALIDATION_CHOICES

MAX_GRAPH_RESULTS = 20000
GRAPH_KEY_SEPARATOR = '___'

logger = logging.getLogger(__name__)


def str_to_datetime(datetime_string):
    dtformat = "%d-%m-%Y"
    try:
        return datetime.strptime(datetime_string, dtformat)
    except:
        logger.debug("Datetime string %r doesn't match format %s.",
                     datetime_string, dtformat)


def possibly_halved_or_krw_value(opname):
    if opname.get('waarde_krw') is not None:
        return opname['waarde_krw']
    value = opname['waarde_n']
    if opname.get('detect__teken') == '<':
        return value / 2.0
    return value


class ApproximateCountPaginator(Paginator):

    def _get_count(self):
        # Much quicker approximate count for big datasets.
        # Partial copy/paste from https://djangosnippets.org/snippets/2855/
        # See http://wiki.postgresql.org/wiki/Slow_Counting
        # Drawback: this returns the total number of items and does **not**
        # take into account any filtering.
        if self._count is None:
            cursor = connection.cursor()
            cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s",
                           [self.object_list.query.model._meta.db_table])
            self._count = int(cursor.fetchone()[0])
        return self._count
    count = property(_get_count)


@api_view()
def api_root(request, format=None):
    return Response({
        'opnames': reverse(
            'efcis-opname-list',
            request=request,
            format=format),
        'graphs': reverse(
            'efcis-graphs',
            request=request,
            format=format),
        'parametergroeps': reverse(
            'efcis-parametergroep-tree',
            request=request,
            format=format),
        'locaties': reverse(
            'efcis-locaties-list',
            request=request,
            format=format),
        'map': reverse(
            'efcis-map',
            request=request,
            format=format),
        'meetstatuses': reverse(
            'efcis-meetstatuses',
            request=request,
            format=format),
        'KRW gebieden': reverse(
            'efcis-krw-areas',
            request=request,
            format=format),
        'meetnetten': reverse(
            'efcis-meetnet-tree',
            request=request,
            format=format),
        'parameters': reverse(
            'efcis-parameters-list',
            request=request,
            format=format),
        'export formaten': reverse(
            'efcis-export-formats',
            request=request,
            format=format),
    })


@api_view()
def opname_detail(request, pk):
    try:
        opname = models.Opname.objects.get(pk=pk)
    except models.Opname.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    show_admin_link = request.user.is_staff
    serializer = serializers.OpnameDetailSerializer(
        opname, context={'request': request,
                         'show_admin_link': show_admin_link})
    return Response(serializer.data)


class ParameterGroepAPI(APIView):

    def get(self, request, format=None):
        parametergroeps = models.ParameterGroep.objects.filter(
            parent__isnull=True)
        serializer = serializers.ParameterGroepSerializer(
            parametergroeps,
            many=True,
            context={'request': self.request}
        )
        return Response(serializer.data)


class ParameterAPI(generics.ListAPIView):

    model = models.Parameter
    serializer_class = serializers.ParameterSerializer
    paginate_by_param = 'page_size'
    paginate_by = 50
    max_page_size = 500

    def _get_parametergroep_childs(self, groep_ids):
        groep_tree_ids = []
        for groep_id in groep_ids:
            par_groeppen = models.ParameterGroep.objects.filter(
                Q(id=groep_id) |
                Q(parent=groep_id) |
                Q(parent__parent=groep_id))
            groep_tree_ids.extend(par_groeppen.values_list('id', flat=True))
        return groep_tree_ids

    def get_queryset(self):
        parametergroups = self.request.query_params.get('parametergroups')
        if parametergroups:
            groep_tree_ids = self._get_parametergroep_childs(
                parametergroups.split(','))
            parameters = models.Parameter.objects.filter(
                parametergroep__id__in=groep_tree_ids)
        else:
            parameters = models.Parameter.objects.all()
        return parameters


class MeetnetAPI(APIView):

    def get(self, request, format=None):
        meetnetten = models.Meetnet.objects.filter(
            parent__isnull=True)
        serializer = serializers.MeetnetSerializer(
            meetnetten,
            many=True,
            context={'request': self.request}
        )
        return Response(serializer.data)


class FilteredOpnamesAPIView(APIView):
    """Base view for returning opnames, filted by GET parameters."""

    exclude_unreliable_also_for_managers = True

    def post(self, *args, **kwargs):
        # Dirty hack around long URLs due to long query parameters.  Note that
        # this only works for the FilteredOpnamesAPIView descendants!
        return self.get(*args, **kwargs)

    def get_or_post_param(self, param):
        # Collary to abovementioned POST hack.
        return (self.request.query_params.get(param)
                or self.request.data.get(param))

    @property
    def filtered_opnames(self):
        opnames = models.Opname.objects.all()

        if self.exclude_unreliable_also_for_managers:
            opnames = opnames.exclude(validation_state=UNRELIABLE)

        start_date = self.get_or_post_param('start_date')
        end_date = self.get_or_post_param('end_date')
        season = self.get_or_post_param('season')
        locations = self.get_or_post_param('locations')
        parametergroeps = self.get_or_post_param('parametergroeps')
        meetnets = self.get_or_post_param('meetnets')
        parameter_ids = self.get_or_post_param('parameters')
        start_datetime = None
        end_datetime = None
        if start_date:
            start_datetime = str_to_datetime(start_date)
            if start_datetime:
                opnames = opnames.filter(datum__gte=start_datetime)
        if end_date:
            end_datetime = str_to_datetime(end_date)
            # retrieve 1-day where end == start
            if end_datetime and end_datetime == start_datetime:
                opnames = opnames.filter(datum=start_datetime)
            if end_datetime and end_datetime > start_datetime:
                opnames = opnames.filter(datum__lte=end_datetime)
        if season == 'winter':
            opnames = opnames.filter(
                Q(datum__month=10) |
                Q(datum__month=11) |
                Q(datum__month=12) |
                Q(datum__month=1) |
                Q(datum__month=2) |
                Q(datum__month=3)
            )
        if season == 'summer':
            opnames = opnames.filter(
                Q(datum__month=4) |
                Q(datum__month=5) |
                Q(datum__month=6) |
                Q(datum__month=7) |
                Q(datum__month=8) |
                Q(datum__month=9)
            )

        # Locations: parameter and parametergroep should be additive, not
        # restrictive.
        parameter_filter = Q()
        if parameter_ids:
            parameter_filter = parameter_filter | Q(
                wns__parameter__id__in=parameter_ids.split(','))
        if parametergroeps:
            parameter_group_ids = parametergroeps.split(',')
            parametergroepen = models.ParameterGroep.objects.filter(
                Q(id__in=parameter_group_ids) |
                Q(parent__in=parameter_group_ids) |
                Q(parent__parent__in=parameter_group_ids))
            parameter_filter = parameter_filter | Q(
                wns__parameter__parametergroep__in=parametergroepen)
        opnames = opnames.filter(parameter_filter)

        # Locations: meetnet and individual selections should be additive, not
        # restrictive.
        location_filter = Q()
        if locations:
            location_filter = location_filter | Q(
                locatie__in=locations.split(','))
        if meetnets:
            meetnet_ids = meetnets.split(',')
            meetnetten = models.Meetnet.objects.filter(
                Q(id__in=meetnet_ids) |
                Q(parent__in=meetnet_ids) |
                Q(parent__parent__in=meetnet_ids) |
                Q(parent__parent__parent__in=meetnet_ids) |
                Q(parent__parent__parent__parent__in=meetnet_ids)
            )

            location_filter = location_filter | Q(
                locatie__meetnet__in=meetnetten)
        opnames = opnames.filter(location_filter).distinct()
        return opnames


class MeetStatusAPI(generics.ListAPIView):

    model = models.MeetStatus
    serializer_class = serializers.MeetStatusSerializer

    def get_queryset(self):
        meetstatuses = models.MeetStatus.objects.all()
        return meetstatuses


class LocatieAPI(generics.ListAPIView):

    model = models.Locatie
    serializer_class = serializers.LocatieSerializer
    paginate_by_param = 'page_size'
    paginate_by = 50
    max_page_size = 500

    def get_queryset(self):
        meetnets = self.request.query_params.get('meetnets')
        locaties = models.Locatie.objects.exclude(geo_punt1__isnull=True,
                                                  area__isnull=True)
        if meetnets is not None:
            meetnet_ids = meetnets.split(',')
            meetnetten = models.Meetnet.objects.filter(
                Q(id__in=meetnet_ids) |
                Q(parent__in=meetnet_ids) |
                Q(parent__parent__in=meetnet_ids) |
                Q(parent__parent__parent__in=meetnet_ids) |
                Q(parent__parent__parent__parent__in=meetnet_ids)
            )
            locaties = locaties.filter(
                meetnet__in=meetnetten).distinct()
        return locaties


class MapAPI(FilteredOpnamesAPIView):
    """Lists locations as geojson for the map.

    ``features`` lists the actual geojson locations. In the properties,
    ``color_value`` (and ``abs_color_value``, see below) is a value between 0
    and 100 that you can use to color the points. The value is ``null`` when
    there's no value at this location for the measurement.

    ``abs_min_value`` and ``abs_max_value`` are the minimum and maximum
    (validated) values found in all the available "opnames" for the "wns" that
    we color on.

    ``min_value`` and ``max_value`` are the minimum and maximum values found
    for the current selection.

    ``color_by_fields`` is a list of fields (rather "wns" id/description
    pairs) that we can color the locations by. Add a GET parameter
    ``color_by=id``, taking the id from this list to enable it.

    """

    @cached_property
    def color_by(self):
        from_query_param = self.get_or_post_param('color_by')
        if from_query_param:
            return int(from_query_param)

    def get(self, request, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None,
                                                          waarde_krw=None)
        opnames = numerical_opnames.values('locatie', 'wns').order_by()
        # ^^^ Note: unordered for speed reasons.
        relevant_locatie_ids = list(set(
            [opname['locatie'] for opname in opnames]))
        locaties = models.Locatie.objects.filter(id__in=relevant_locatie_ids)
        relevant_wns_ids = list(set(
            [opname['wns'] for opname in opnames]))
        color_by_fields = models.WNS.objects.filter(
            pk__in=relevant_wns_ids).values('id', 'wns_oms', 'parameter__par_oms_nl')

        latest_values = {}  # Latest value per location.
        latest_krw_values = {}  # Latest value per location.
        color_values = {}  # Latest value converted to 0-100 scale.
        abs_color_values = {}  # Same, but scaled to all values.
        boxplot_values = {}
        latest_datetimes = {}

        min_value = None
        max_value = None
        abs_min_value = None
        abs_max_value = None
        color_by_name = None
        is_krw_score = False

        if self.color_by:
            color_by_name = models.WNS.objects.get(pk=self.color_by).wns_oms
            # Re-fetch numerical opnames, now including values
            numerical_opnames = self.filtered_opnames.exclude(waarde_n=None,
                                                              waarde_krw=None)
            opnames_for_color_by = numerical_opnames.filter(
                wns=self.color_by).values(
                    'locatie', 'datum', 'tijd', 'waarde_n',
                    'waarde_a',
                    'waarde_krw',
                    'detect__teken', 'activiteit__act_type')

            if opnames_for_color_by:
                is_krw_score = (
                    opnames_for_color_by[0]['activiteit__act_type'] ==
                    models.Activiteit.T2)

            abs_min_max = models.Opname.objects.filter(
                wns=self.color_by,
                validation_state=VALIDATED).aggregate(
                    Min('waarde_n'), Max('waarde_n'))
            abs_min_value = abs_min_max['waarde_n__min']
            abs_max_value = abs_min_max['waarde_n__max']
            if abs_min_value is not None and abs_max_value is not None:
                abs_difference = abs_max_value - abs_min_value
            else:
                abs_difference = None

            selection_values = [opname['waarde_n'] for opname in opnames_for_color_by
                                if opname['waarde_n'] is not None]
            if selection_values:
                min_value = min(selection_values)
                max_value = max(selection_values)
                difference = max_value - min_value
            else:
                # min([]) raises an error!
                min_value = None
                max_value = None
                difference = None

            if is_krw_score:
                # Hard-code the range to 0-1
                min_value = 0
                abs_min_value = 0
                max_value = 1
                abs_max_value = 1
                difference = 1
                abs_difference = 1

            def _key(opname):
                return opname['locatie']

            for locatie, group in groupby(opnames_for_color_by, _key):

                opnames_per_locatie = list(group)
                values = [
                    possibly_halved_or_krw_value(opname)
                    for opname in opnames_per_locatie]
                summer_values = [
                    possibly_halved_or_krw_value(opname) for opname in opnames_per_locatie
                    if opname['datum'].month in [4, 5, 6, 7, 8, 9]]
                winter_values = [
                    possibly_halved_or_krw_value(opname) for opname in opnames_per_locatie
                    if opname['datum'].month not in [4, 5, 6, 7, 8, 9]]
                if summer_values:
                    summer_mean = np.mean(summer_values)
                else:
                    # Otherwise you get a "mean of empty slice" error.
                    summer_mean = None
                if winter_values:
                    winter_mean = np.mean(winter_values)
                else:
                    winter_mean = None

                boxplot_data = {'mean': np.mean(values),
                                'summer_mean': summer_mean,
                                'winter_mean': winter_mean,
                                'num_values': len(values),
                                'median': np.median(values),
                                'min': np.min(values),
                                'max': np.max(values),
                                'std': np.std(values),
                                'q1': np.percentile(values, 25),
                                'q3': np.percentile(values, 75),
                                'p10': np.percentile(values, 10),
                                'p90': np.percentile(values, 90)}

                if is_krw_score:
                    krw_values = [opname['waarde_a'] for opname in opnames_per_locatie
                                  if opname['waarde_a']]
                    latest_krw_values[locatie] = krw_values[-1]

                if not opnames_per_locatie:
                    continue
                # Group is sorted according to date/time, we can grab the
                # latest one.
                latest_value = values[-1]
                latest_values[locatie] = latest_value
                latest_opname = opnames_per_locatie[-1]
                latest_datetime = '%sT%s.000Z' % (latest_opname['datum'],
                                                  latest_opname['tijd'] or '00:00:00')
                latest_datetimes[locatie] = latest_datetime
                if difference:
                    color_value = round(
                        (latest_value - min_value) / difference * 100)
                else:
                    color_value = 100.0
                if abs_difference:
                    abs_color_value = round(
                        (latest_value - abs_min_value) / abs_difference * 100)
                else:
                    abs_color_value = 100.0
                color_values[locatie] = color_value
                abs_color_values[locatie] = abs_color_value
                boxplot_values[locatie] = boxplot_data

        serializer = serializers.MapSerializer(
            locaties,
            many=True,
            context={'latest_values': latest_values,
                     'latest_krw_values': latest_krw_values,
                     'latest_datetimes': latest_datetimes,
                     'is_krw_score': is_krw_score,
                     'color_values': color_values,
                     'abs_color_values': abs_color_values,
                     'boxplot_values': boxplot_values})
        result = serializer.data

        result['color_by_fields'] = color_by_fields
        result['min_value'] = min_value
        result['max_value'] = max_value
        result['abs_min_value'] = abs_min_value
        result['abs_max_value'] = abs_max_value
        result['color_by_name'] = color_by_name
        result['is_krw_score'] = is_krw_score

        return Response(result)


class OpnamesAPI(FilteredOpnamesAPIView):

    exclude_unreliable_also_for_managers = False
    # ^^^ The table view is the only place were managers want to see
    # unreliable opnames. In all other places (especially the mean/min/max
    # values) they should be filtered out even for them. (Normal users already
    # only see validated opnames).

    def get(self, request, format=None):
        loc_id_filter = self.get_or_post_param('loc_id')
        wns_oms_filter = self.get_or_post_param('wns_oms')
        par_oms_filter = self.get_or_post_param('par_oms')
        par_oms_nl_filter = self.get_or_post_param('par_oms_nl')
        loc_oms_filter = self.get_or_post_param('loc_oms')
        activiteit_filter = self.get_or_post_param('activiteit')
        detectiegrens_filter = self.get_or_post_param('detectiegrens')
        validation_state_filter = self.get_or_post_param('validatiestatus')
        waarde_n_filter = self.get_or_post_param('waarde_n')
        waarde_a_filter = self.get_or_post_param('waarde_a')
        eenheid_oms_filter = self.get_or_post_param('eenheid_oms')
        hoedanigheid_oms_filter = self.get_or_post_param('hoed_oms')
        compartiment_oms_filter = self.get_or_post_param('comp_oms')
        sort_fields = self.get_or_post_param('sort_fields')
        sort_dirs = self.get_or_post_param('sort_dirs')
        ITEMS_PER_PAGE = 30

        page = self.get_or_post_param('page')
        page_size = self.get_or_post_param('page_size')
        filtered_opnames = self.filtered_opnames

        if loc_id_filter:
            filtered_opnames = filtered_opnames.filter(
                locatie__loc_id__icontains=loc_id_filter)
        if wns_oms_filter:
            filtered_opnames = filtered_opnames.filter(
                wns__wns_oms__icontains=wns_oms_filter)
        if loc_oms_filter:
            filtered_opnames = filtered_opnames.filter(
                locatie__loc_oms__icontains=loc_oms_filter)
        if par_oms_filter:
            filtered_opnames = filtered_opnames.filter(
                wns__parameter__par_oms__icontains=par_oms_filter)
        if par_oms_nl_filter:
            filtered_opnames = filtered_opnames.filter(
                wns__parameter__par_oms_nl__icontains=par_oms_nl_filter)
        if activiteit_filter:
            filtered_opnames = filtered_opnames.filter(
                activiteit__activiteit__icontains=activiteit_filter)
        if detectiegrens_filter:
            filtered_opnames = filtered_opnames.filter(
                detect__teken__icontains=detectiegrens_filter)
        if validation_state_filter:
            search_text = validation_state_filter.lower()
            matching_states = [number for (number, text) in VALIDATION_CHOICES
                               if search_text in text.lower()]
            filtered_opnames = filtered_opnames.filter(
                validation_state__in=matching_states)
        if waarde_n_filter:
            if '..' in waarde_n_filter:
                waarde_range = waarde_n_filter.split('..')
                filtered_opnames = filtered_opnames.filter(
                    waarde_n__gt=waarde_range[0])
                filtered_opnames = filtered_opnames.filter(
                    waarde_n__lt=waarde_range[1])
            elif '<' in waarde_n_filter:
                waarde_n_filter = waarde_n_filter.replace('<', '').strip()
                filtered_opnames = filtered_opnames.filter(
                    waarde_n__lt=waarde_n_filter)
            elif '>' in waarde_n_filter:
                waarde_n_filter = waarde_n_filter.replace('>', '').strip()
                filtered_opnames = filtered_opnames.filter(
                    waarde_n__gt=waarde_n_filter)
            else:
                filtered_opnames = filtered_opnames.filter(
                    waarde_n=waarde_n_filter)
        if waarde_a_filter:
            filtered_opnames = filtered_opnames.filter(
                waarde_a=waarde_a_filter)
        if eenheid_oms_filter:
            filtered_opnames = filtered_opnames.filter(
                wns__eenheid__eenheid_oms__icontains=eenheid_oms_filter)
        if hoedanigheid_oms_filter:
            filtered_opnames = filtered_opnames.filter(
                wns__hoedanigheid__hoed_oms__icontains=hoedanigheid_oms_filter)
        if compartiment_oms_filter:
            filtered_opnames = filtered_opnames.filter(
                wns__compartiment__comp_oms__icontains=compartiment_oms_filter)
        if sort_fields and sort_dirs:
            filtered_opnames = self.order_opnames(
                sort_fields, sort_dirs, filtered_opnames)

        if page_size not in [None, '']:
            ITEMS_PER_PAGE = page_size

        filtered_opnames = filtered_opnames.prefetch_related(
            'locatie',
            'locatie__watertype',
            'wns',
            'activiteit',
            'detect',
            'wns__parameter',
            'wns__eenheid',
            'wns__hoedanigheid',
            'wns__compartiment',
            )

        if self.get_or_post_param('format') == 'csv':
            serializer = serializers.OpnameSerializer(
                filtered_opnames,
                many=True,
                context={'request': self.request})
            return Response(serializer.data)

        # paginator = ApproximateCountPaginator(filtered_opnames, ITEMS_PER_PAGE)
        paginator = Paginator(filtered_opnames, ITEMS_PER_PAGE)
        try:
            opnames = paginator.page(page)
        except PageNotAnInteger:
            opnames = paginator.page(1)
        except EmptyPage:
            opnames = paginator.page(paginator.num_pages)

        serializer = serializers.PaginatedOpnameSerializer(
            opnames,
            context={'request': self.request})
        return Response(serializer.data)

    def order_opnames(self, sort_fields, sort_dirs, filtered_opnames):
        sort_field_names = sort_fields.split(',')
        sort_directions = sort_dirs.split(',')
        ordering = []
        for fieldname in sort_field_names:
            direction = sort_directions[sort_field_names.index(fieldname)]

            if direction.startswith('-'):
                direction_sign = '-'
            else:
                direction_sign = ''

            if fieldname == 'wns_oms':
                fieldname = 'wns__wns_oms'
            elif fieldname == 'loc_id':
                fieldname = 'locatie__loc_id'
            elif fieldname == 'loc_oms':
                fieldname = 'locatie__loc_oms'
            elif fieldname == 'activiteit':
                fieldname == 'activiteit__activiteit'
            elif fieldname == 'detectiegrens':
                fieldname = 'detect__teken'
            elif fieldname == 'par_oms':
                fieldname = 'wns__parameter__par_oms'
            elif fieldname == 'par_oms_nl':
                fieldname = 'wns__parameter__par_oms_nl'
            elif fieldname == 'hoed_oms':
                fieldname = 'wns__hoedanigheid__hoed_oms'
            elif fieldname == 'comp_oms':
                fieldname = 'wns__compartiment__comp_oms'
            elif fieldname == 'eenheid_oms':
                fieldname = 'wns__eenheid__eenheid_oms'
            elif fieldname == 'validatiestatus':
                fieldname = 'validation_state'
            elif fieldname == 'grondsoort':
                fieldname = 'locatie__grondsoort'
            elif fieldname == 'landgebruik':
                fieldname = 'locatie__landgebruik'
            ordering.append('%s%s' % (direction_sign, fieldname))
        filtered_opnames = filtered_opnames.order_by(*ordering)
        return filtered_opnames


class GraphsAPI(FilteredOpnamesAPIView):
    """API to return available graph lines."""

    def get(self, request, format=None):
        numerical_opnames = self.filtered_opnames.exclude(
            waarde_n=None).order_by()
        all_points = numerical_opnames.values(
            'wns__wns_code', 'wns__wns_oms', 'wns__parameter__par_code',
            'wns__eenheid__eenheid', 'wns__parameter__par_oms_nl',
            'locatie__loc_id', 'locatie__loc_oms')[:MAX_GRAPH_RESULTS]

        def _key(point):
            return '%s%s%s' % (point['wns__wns_code'],
                               GRAPH_KEY_SEPARATOR,
                               point['locatie__loc_id'])

        all_points = list(all_points)
        all_points.sort(key=_key)
        lines = []
        for key, group in groupby(all_points, _key):
            points = list(group)
            if not points:
                # Weird corner case?
                continue
            first = points[0]
            line = {'wns': first['wns__wns_oms'],
                    'location': first['locatie__loc_oms'],
                    'parameter_nl': first['wns__parameter__par_oms_nl'],
                    'unit': first['wns__eenheid__eenheid'],
                    'id': key,
                    'line-url': reverse(
                        'efcis-line',
                        kwargs={'key': key},
                        format=format,
                        request=self.request),
                    'boxplot-url': reverse(
                        'efcis-boxplot',
                        kwargs={'key': key},
                        format=format,
                        request=self.request),
                    'scatterplot-second-axis-url': reverse(
                        'efcis-scatterplot-second-axis',
                        kwargs={'axis1_key': key},
                        format=format,
                        request=self.request),
            }
            lines.append(line)

        return Response(lines)


class LineAPI(FilteredOpnamesAPIView):
    """API to return line for a single graph."""

    def get(self, request, key=None, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        wns_code, loc_id = key.split(GRAPH_KEY_SEPARATOR)
        our_opnames = numerical_opnames.filter(
            wns__wns_code=wns_code, locatie__loc_id=loc_id)
        points = our_opnames.values(
            'wns__wns_oms',
            'wns__parameter__par_code',
            'wns__eenheid__eenheid',
            'locatie__loc_oms',
            'detect__teken',
            'datum',
            'tijd',
            'waarde_n')

        points = list(points)
        if not points:
            # Incorrect dates, probably.
            return Response({})
        first = points[0]
        data = [{'datetime': '%sT%s.000Z' % (point['datum'],
                                             point['tijd'] or '00:00:00'),
                 'value': possibly_halved_or_krw_value(point)} for point in points]
        line = {'wns': first['wns__wns_oms'],
                'location': first['locatie__loc_oms'],
                'unit': first['wns__eenheid__eenheid'],
                'data': data,
                'id': key}
        return Response(line)


class BoxplotAPI(FilteredOpnamesAPIView):
    """API to return the Boxplot values for a single graph"""

    def get(self, request, key=None, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        wns_code, loc_id = key.split(GRAPH_KEY_SEPARATOR)
        split_by_year = self.get_or_post_param('split_by_year')
        our_opnames = numerical_opnames.filter(
            wns__wns_code=wns_code, locatie__loc_id=loc_id)
        points = our_opnames.values(
            'wns__wns_oms',
            'wns__parameter__par_code',
            'wns__eenheid__eenheid',
            'locatie__loc_id',
            'locatie__loc_oms',
            'datum',
            'tijd',
            'detect__teken',
            'waarde_n')

        points = list(points)
        if not points:
            # Incorrect dates, probably.
            return Response({})

        first = points[0]
        last = points[len(points) - 1]

        lines = []

        ## Some code are equal in 'if ... else ...' block below
        if split_by_year == "true":
            for year in range(first['datum'].year, last['datum'].year + 1):
                values = [possibly_halved_or_krw_value(point)
                          for point in points if point['datum'].year == year]
                if len(values) <= 0:
                    continue

                boxplot_data = {'mean': np.mean(values),
                                'median': np.median(values),
                                'min': np.min(values),
                                'max': np.max(values),
                                'std': np.std(values),
                                'num_values': len(values),
                                'q1': np.percentile(values, 25),
                                'q3': np.percentile(values, 75),
                                'p10': np.percentile(values, 10),
                                'p90': np.percentile(values, 90)}
                line = {'wns': first['wns__wns_oms'],
                        'location_id': first['locatie__loc_id'],
                        'location': first['locatie__loc_oms'],
                        'unit': first['wns__eenheid__eenheid'],
                        'boxplot_data': boxplot_data,
                        'id': key,
                        'start_date': "%s-%s-%s" % ("1", "1", year),
                        'end_date': "%s-%s-%s" % ("31", "12", year)}
                lines.append(line)
        else:
            values = [possibly_halved_or_krw_value(point)
                      for point in points]

            boxplot_data = {'mean': np.mean(values),
                            'median': np.median(values),
                            'min': np.min(values),
                            'max': np.max(values),
                            'std': np.std(values),
                            'num_values': len(values),
                            'q1': np.percentile(values, 25),
                            'q3': np.percentile(values, 75),
                            'p10': np.percentile(values, 10),
                            'p90': np.percentile(values, 90)}
            line = {'wns': first['wns__wns_oms'],
                    'location_id': first['locatie__loc_id'],
                    'location': first['locatie__loc_oms'],
                    'unit': first['wns__eenheid__eenheid'],
                    'boxplot_data': boxplot_data,
                    'id': key,
                    'start_date': self.get_or_post_param("start_date"),
                    'end_date': self.get_or_post_param("end_date")}
            lines.append(line)
        return Response(lines)


class ScatterplotSecondAxisAPI(FilteredOpnamesAPIView):
    """API to return second axis lines for a single graph."""

    def get(self, request, axis1_key=None, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        wns_code, loc_id = axis1_key.split(GRAPH_KEY_SEPARATOR)
        our_opnames = numerical_opnames.filter(
            wns__wns_code=wns_code, locatie__loc_id=loc_id)
        points = our_opnames.values(
            'wns__wns_code',
            'wns__wns_oms',
            'wns__parameter__par_code',
            'wns__parameter__par_oms_nl',
            'wns__eenheid__eenheid',
            'locatie__loc_oms',
            'locatie__loc_id',
            'datum',
            'tijd')
        points = list(points)
        if not points:
            # Incorrect dates, probably.
            return Response({})
        first = points[0]

        dates = [point['datum'] for point in points]
        opnames_with_correct_date = numerical_opnames.filter(
            datum__in=dates)
        lines_with_correct_dates = opnames_with_correct_date.values(
            'wns__wns_code',
            'wns__wns_oms',
            'wns__parameter__par_oms_nl',
            'wns__parameter__par_code',
            'wns__eenheid__eenheid',
            'locatie__loc_oms',
            'locatie__loc_id').exclude(
                wns__wns_code=wns_code, locatie__loc_id=loc_id).annotate(
                    Count('datum')).order_by('-datum__count')
        desired_number_of_points = len(points) * 0.5
        # ^^^ At least 50% matching points.
        lines_with_correct_dates = [
            line for line in lines_with_correct_dates
            if line['datum__count'] > desired_number_of_points]
        second_axis_lines = []
        for line in lines_with_correct_dates:
            key = '%s%s%s' % (line['wns__wns_code'],
                              GRAPH_KEY_SEPARATOR,
                              line['locatie__loc_id'])
            second_axis_lines.append(
                {'wns': line['wns__wns_oms'],
                 'parameter_nl': line['wns__parameter__par_oms_nl'],
                 'location': line['locatie__loc_oms'],
                 'unit': line['wns__eenheid__eenheid'],
                 'url': reverse('efcis-scatterplot-graph',
                                kwargs={'axis1_key': axis1_key,
                                        'axis2_key': key},
                                format=format,
                                request=self.request),
                 'id': key})

        line = {'wns': first['wns__wns_oms'],
                'location': first['locatie__loc_oms'],
                'unit': first['wns__eenheid__eenheid'],
                'parameter_nl': first['wns__parameter__par_oms_nl'],
                'second_axis_lines': second_axis_lines,
                'id': axis1_key}

        return Response(line)


class ScatterplotGraphAPI(FilteredOpnamesAPIView):
    """API to return scatterplot x/y data for two axes."""

    def get(self, request, axis1_key=None, axis2_key=None, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        wns_code1, loc_id1 = axis1_key.split(GRAPH_KEY_SEPARATOR)
        wns_code2, loc_id2 = axis2_key.split(GRAPH_KEY_SEPARATOR)
        our_opnames1 = numerical_opnames.filter(
            wns__wns_code=wns_code1, locatie__loc_id=loc_id1).values(
                'wns__wns_oms',
                'wns__parameter__par_code',
                'wns__eenheid__eenheid',
                'locatie__loc_oms',
                'detect__teken',
                'datum',
                'waarde_n')
        our_opnames2 = numerical_opnames.filter(
            wns__wns_code=wns_code2, locatie__loc_id=loc_id2).values(
                'wns__wns_oms',
                'wns__parameter__par_code',
                'wns__eenheid__eenheid',
                'locatie__loc_oms',
                'detect__teken',
                'datum',
                'waarde_n')
        dates = [opname['datum'] for opname in our_opnames1]

        points = []
        for date in dates:
            x_candidates = [opname for opname in our_opnames1
                            if opname['datum'] == date]
            y_candidates = [opname for opname in our_opnames2
                            if opname['datum'] == date]
            if not (x_candidates and y_candidates):
                continue
            x = possibly_halved_or_krw_value(x_candidates[0])
            y = possibly_halved_or_krw_value(y_candidates[0])
            points.append({'x': x, 'y': y})

        first_x = our_opnames1[0]
        first_y = our_opnames2[0]
        result = {
            'x_wns': first_x['wns__wns_oms'],
            'x_location': first_x['locatie__loc_oms'],
            'x_unit': first_x['wns__eenheid__eenheid'],
            'x_id': axis1_key,

            'y_wns': first_y['wns__wns_oms'],
            'y_location': first_y['locatie__loc_oms'],
            'y_unit': first_y['wns__eenheid__eenheid'],
            'y_id': axis2_key,

            'points': points}
        return Response(result)


class ExportFormatsAPI(APIView):
    """Show available export formats (umaquo xml + various csv exports)."""

    def get(self, request, format=None):
        result = []
        for import_mapping in models.ImportMapping.objects.filter(
                tabel_naam='Opname').filter(is_export=True):
            url = reverse('efcis-export-csv',
                          request=request,
                          kwargs={'import_mapping_id': import_mapping.id})
            result.append({'name': import_mapping.code,
                           'url': url})

        xml_url = reverse('efcis-export-xml', request=request)
        result.append({'name': "umaquo XML",
                       'url': xml_url})
        return Response(result)


class ExportCSVView(FilteredOpnamesAPIView):
    """Export through celery."""

    def get(self, request, import_mapping_id=None, format=None):
        import_mapping = models.ImportMapping.objects.get(
            pk=import_mapping_id)
        filename = "%s-%s.csv" % (
            slugify(import_mapping.code),
            datetime.now().strftime("%Y-%m-%d_%H%M"))
        tasks.export_opnames_to_csv.delay(
            request.user.email,
            self.filtered_opnames.query,
            filename,
            import_mapping,
            self.request.get_host()
        )
        response = Response(
            {"message": "Export is gestart, u krijgt een email als het klaar is.",
             "email": request.user.email})
        return response


class UmaquoXMLRenderer(TemplateHTMLRenderer):
    media_type = 'application/xml'
    format = 'xml'
    template_name = 'lizard_efcis/umaquo.xml'


class ExportXMLView(FilteredOpnamesAPIView):
    renderer_classes = (UmaquoXMLRenderer, )

    def data(self):
        """Return context for the renderer's template.

        So: if you have 'for thingy in thingies' in your template, you need to
        have 'thingies' in the dictionary you return here.
        """
        context = export_data.get_xml_context(self.filtered_opnames)
        return context

    def get(self, request, format=None):
        filename = "umaquo-%s.xml" % datetime.now().strftime("%Y-%m-%d_%H%M")
        headers = {'Content-Disposition': 'attachment; filename="%s"' % filename}
        return Response(self.data(),
                        headers=headers)


class KRWAreasAPI(APIView):
    """Return KRW areas for simple display.
    """

    def get(self, request, format=None):
        locaties = models.Locatie.objects.filter(is_krw_area=True)
        serializer = serializers.KRWAreaSerializer(
            locaties,
            many=True)
        result = serializer.data
        return Response(result)
