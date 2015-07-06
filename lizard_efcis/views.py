# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from itertools import groupby
import logging
import numpy as np
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.utils.functional import cached_property
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer

from lizard_efcis import models
from lizard_efcis import serializers

MAX_GRAPH_RESULTS = 20000
GRAPH_KEY_SEPARATOR = '___'

logger = logging.getLogger(__name__)


def str_to_datetime(dtstr):
    dtformat = "%d-%m-%Y"
    try:
        return datetime.strptime(dtstr, dtformat)
    except:
        logger.warn("Error on formating datimestr to datetime "
                    "{0} doesn't match {1}.".format(dtstr, dtformat))


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
        'meetnetten': reverse(
            'efcis-meetnet-tree',
            request=request,
            format=format),
        'parameters': reverse(
            'efcis-parameters-list',
            request=request,
            format=format),
    })


@api_view()
def opname_detail(request, pk):
    try:
        opname = models.Opname.objects.get(pk=pk)
    except models.Opname.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.OpnameDetailSerializer(
        opname, context={'request': request})
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

    def post(self, request, format=None):
        # Dirty hack around long URLs due to long query parameters.  Note that
        # this only works for the FilteredOpnamesAPIView descendants!
        return self.get(request, format=None)

    def get_or_post_param(self, param):
        # Collary to abovementioned POST hack.
        return (self.request.query_params.get(param)
                or self.request.data.get(param))

    @property
    def filtered_opnames(self):
        opnames = models.Opname.objects.all()

        start_date = self.get_or_post_param('start_date')
        end_date = self.get_or_post_param('end_date')
        locations = self.get_or_post_param('locations')
        parametergroeps = self.get_or_post_param('parametergroeps')
        meetnets = self.get_or_post_param('meetnets')
        parameter_ids = self.get_or_post_param('parameters')

        if start_date:
            start_datetime = str_to_datetime(start_date)
            if start_datetime:
                opnames = opnames.filter(datum__gte=start_datetime)
        if end_date:
            end_datetime = str_to_datetime(end_date)
            if end_datetime:
                opnames = opnames.filter(datum__lte=end_datetime)

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
        opnames = opnames.filter(location_filter)
        return opnames


class LocatieAPI(generics.ListAPIView):

    model = models.Locatie
    serializer_class = serializers.LocatieSerializer
    paginate_by_param = 'page_size'
    paginate_by = 50
    max_page_size = 500

    def get_queryset(self):
        meetnets = self.request.query_params.get('meetnets')
        locaties = None
        if meetnets is None:
            locaties = models.Locatie.objects.all()
        else:
            meetnet_ids = meetnets.split(',')
            meetnetten = models.Meetnet.objects.filter(
                Q(id__in=meetnet_ids) |
                Q(parent__in=meetnet_ids) |
                Q(parent__parent__in=meetnet_ids) |
                Q(parent__parent__parent__in=meetnet_ids) |
                Q(parent__parent__parent__parent__in=meetnet_ids)
            )
            locaties = models.Locatie.objects.filter(
                meetnet__in=meetnetten).distinct()
        return locaties


class MapAPI(FilteredOpnamesAPIView):
    """Lists locations as geojson for the map.

    ``features`` lists the actual geojson locations. In the properties,
    ``color_value`` is a value between 0 and 100 that you can use to color the
    points. The value is ``null`` when there's no value at this location for
    the measurement.

    ``min_value`` and ``max_value`` are the minimum and maximum values found
    in all the available "opnames" for the "wns" that we color on.

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
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        # opnames = numerical_opnames.values(
        #     'locatie', 'wns', 'datum', 'tijd', 'waarde_n')
        opnames = numerical_opnames.values('locatie', 'wns').order_by()
        # ^^^ Note: unordered for speed reasons.
        relevant_locatie_ids = list(set(
            [opname['locatie'] for opname in opnames]))
        locaties = models.Locatie.objects.filter(id__in=relevant_locatie_ids)
        relevant_wns_ids = list(set(
            [opname['wns'] for opname in opnames]))
        color_by_fields = models.WNS.objects.filter(
            pk__in=relevant_wns_ids).values('id', 'wns_oms')

        latest_values = {}  # Latest value per location.
        color_values = {}  # Latest value converted to 0-100 scale.
        boxplot_values = {}
        latest_datetimes = {}

        min_value = None
        max_value = None
        color_by_name = None

        if self.color_by:
            color_by_name = models.WNS.objects.get(pk=self.color_by).wns_oms
            # Re-fetch numerical opnames, now including values
            numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
            opnames_for_color_by = numerical_opnames.filter(
                wns=self.color_by).values(
                    'locatie', 'datum', 'tijd', 'waarde_n')

            values = [item['waarde_n'] for item in opnames_for_color_by]
            min_value = min(values)
            max_value = max(values)
            difference = max_value - min_value

            def _key(opname):
                return opname['locatie']

            for locatie, group in groupby(opnames_for_color_by, _key):

                opnames_per_locatie = list(group)
                values = [opname['waarde_n'] for opname in opnames_per_locatie]

                boxplot_data = {'mean': np.mean(values),
                                'num_values': len(values),
                                'median': np.median(values),
                                'min': np.min(values),
                                'max': np.max(values),
                                'q1': np.percentile(values, 25),
                                'q3': np.percentile(values, 75),
                                'p10': np.percentile(values, 10),
                                'p90': np.percentile(values, 90)}

                if not opnames_per_locatie:
                    continue
                # Group is sorted according to date/time, we can grab the
                # latest one.
                latest_value = values[-1]
                latest_values[locatie] = latest_value
                latest_opname = opnames_per_locatie[-1]
                latest_datetime = '%sT%s.000Z' % (latest_opname['datum'], latest_opname['tijd'])
                latest_datetimes[locatie] = latest_datetime
                if difference:
                    color_value = round(
                        (latest_value - min_value) / difference * 100)
                else:
                    color_value = 100.0
                color_values[locatie] = color_value
                boxplot_values[locatie] = boxplot_data

        serializer = serializers.MapSerializer(
            locaties,
            many=True,
            context={'latest_values': latest_values,
                     'latest_datetimes': latest_datetimes,
                     'color_values': color_values,
                     'boxplot_values': boxplot_values})
        result = serializer.data

        result['color_by_fields'] = color_by_fields
        result['min_value'] = min_value
        result['max_value'] = max_value
        result['color_by_name'] = color_by_name

        return Response(result)


class OpnamesAPI(FilteredOpnamesAPIView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [CSVRenderer]

    def get(self, request, format=None):
        # TODO: refactor pagination stuff with djangorestframework 3.1
        loc_id_filter = self.get_or_post_param('loc_id')
        wns_oms_filter = self.get_or_post_param('wns_oms')
        loc_oms_filter = self.get_or_post_param('loc_oms')
        activiteit_filter = self.get_or_post_param('activiteit')
        detectiegrens_filter = self.get_or_post_param('detectiegrens')
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
        if activiteit_filter:
            filtered_opnames = filtered_opnames.filter(
                activiteit__activiteit__icontains=activiteit_filter)
        if detectiegrens_filter:
            filtered_opnames = filtered_opnames.filter(
                detect__teken__icontains=detectiegrens_filter)
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
            elif fieldname == 'hoed_oms':
                fieldname = 'wns__hoedanigheid__hoed_oms'
            elif fieldname == 'comp_oms':
                fieldname = 'wns__compartiment__comp_oms'
            elif fieldname == 'eenheid_oms':
                fieldname = 'wns__eenheid__eenheid_oms'
            ordering.append('%s%s' % (direction_sign, fieldname))
        filtered_opnames = filtered_opnames.order_by(*ordering)
        return filtered_opnames


class GraphsAPI(FilteredOpnamesAPIView):
    """API to return available graph lines."""

    def get(self, request, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        all_points = numerical_opnames.values(
            'wns__wns_code', 'wns__wns_oms', 'wns__parameter__par_code',
            'wns__eenheid__eenheid',
            'locatie__loc_id', 'locatie__loc_oms')[:MAX_GRAPH_RESULTS]

        def _key(point):
            return '%s%s%s' % (point['wns__wns_code'],
                               GRAPH_KEY_SEPARATOR,
                               point['locatie__loc_id'])

        lines = []
        for key, group in groupby(all_points, _key):
            points = list(group)
            first = points[0]
            line = {'wns': first['wns__wns_oms'],
                    'location': first['locatie__loc_oms'],
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
            'datum',
            'tijd',
            'waarde_n')

        points = list(points)
        first = points[0]
        data = [{'datetime': '%sT%s.000Z' % (point['datum'], point['tijd']),
                 'value': point['waarde_n']} for point in points]
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
        our_opnames = numerical_opnames.filter(
            wns__wns_code=wns_code, locatie__loc_id=loc_id)
        points = our_opnames.values(
            'wns__wns_oms',
            'wns__parameter__par_code',
            'wns__eenheid__eenheid',
            'locatie__loc_oms',
            'datum',
            'tijd',
            'waarde_n')

        points = list(points)
        first = points[0]
        values = [point['waarde_n'] for point in points]
        boxplot_data = {'mean': np.mean(values),
                        'median': np.median(values),
                        'min': np.min(values),
                        'max': np.max(values),
                        'q1': np.percentile(values, 25),
                        'q3': np.percentile(values, 75),
                        'p10': np.percentile(values, 10),
                        'p90': np.percentile(values, 90)}
        line = {'wns': first['wns__wns_oms'],
                'location': first['locatie__loc_oms'],
                'unit': first['wns__eenheid__eenheid'],
                'boxplot_data': boxplot_data,
                'id': key}
        return Response(line)


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
            'wns__eenheid__eenheid',
            'locatie__loc_oms',
            'locatie__loc_id',
            'datum',
            'tijd')
        points = list(points)
        first = points[0]

        dates = [point['datum'] for point in points]
        opnames_with_correct_date = numerical_opnames.filter(
            datum__in=dates)
        lines_with_correct_dates = opnames_with_correct_date.values(
            'wns__wns_code',
            'wns__wns_oms',
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
                'datum',
                'waarde_n')
        our_opnames2 = numerical_opnames.filter(
            wns__wns_code=wns_code2, locatie__loc_id=loc_id2).values(
                'wns__wns_oms',
                'wns__parameter__par_code',
                'wns__eenheid__eenheid',
                'locatie__loc_oms',
                'datum',
                'waarde_n')
        dates = [opname['datum'] for opname in our_opnames1]

        points = []
        for date in dates:
            x_candidates = [opname for opname in our_opnames1
                            if opname['datum']==date]
            y_candidates = [opname for opname in our_opnames2
                            if opname['datum']==date]
            if not (x_candidates and y_candidates):
                continue
            x = x_candidates[0]['waarde_n']
            y = y_candidates[0]['waarde_n']
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
