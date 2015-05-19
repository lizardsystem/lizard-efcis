# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from itertools import groupby
import logging

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
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
        'lines': reverse(
            'efcis-lines',
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
            context={'request': request}
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
            context={'request': request}
        )
        return Response(serializer.data)


class FilteredOpnamesAPIView(APIView):
    """Base view for returning opnames, filted by GET parameters."""

    @property
    def filtered_opnames(self):
        opnames = models.Opname.objects.all()

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        locations = self.request.query_params.get('locations')
        parametergroeps = self.request.query_params.get('parametergroeps')
        meetnets = self.request.query_params.get('meetnets')
        parameter_ids = self.request.query_params.get('parameters')

        if start_date:
            start_datetime = str_to_datetime(start_date)
            if start_datetime:
                opnames = opnames.filter(datum__gt=start_datetime)
        if end_date:
            end_datetime = str_to_datetime(end_date)
            if end_datetime:
                opnames = opnames.filter(datum__lt=end_datetime)

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
        from_query_param = self.request.query_params.get('color_by')
        if from_query_param:
            return int(from_query_param)

    def get(self, request, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        opnames = numerical_opnames.values(
            'locatie', 'wns', 'datum', 'tijd', 'waarde_n')
        relevant_locatie_ids = list(set(
            [opname['locatie'] for opname in opnames]))
        relevant_wns_ids = list(set(
            [opname['wns'] for opname in opnames]))

        latest_values = {}  # Latest value per location.
        color_values = {}  # Latest value converted to 0-100 scale.
        min_value = None
        max_value = None
        color_by_name = None
        if self.color_by:
            color_by_name = models.WNS.objects.get(pk=self.color_by).wns_oms
            min_max = models.Opname.objects.filter(
                wns=self.color_by).aggregate(
                Min('waarde_n'), Max('waarde_n'))
            min_value = min_max['waarde_n__min']
            max_value = min_max['waarde_n__max']
            difference = max_value - min_value
            opnames_for_color_by = [opname for opname in opnames
                                    if opname['wns'] == self.color_by]

            def _key(opname):
                return opname['locatie']

            for locatie, group in groupby(opnames_for_color_by, _key):
                opnames_per_locatie = list(group)
                if not opnames_per_locatie:
                    continue
                # Group is sorted according to date/time, we can grab the
                # latest one.
                latest_value = opnames_per_locatie[-1]['waarde_n']
                latest_values[locatie] = latest_value
                if difference:
                    color_value = round(
                        (latest_value - min_value) / difference * 100)
                else:
                    color_value = 100.0
                color_values[locatie] = color_value

        locaties = models.Locatie.objects.filter(id__in=relevant_locatie_ids)
        serializer = serializers.MapSerializer(
            locaties,
            many=True,
            context={'latest_values': latest_values,
                     'color_values': color_values})
        result = serializer.data

        color_by_fields = models.WNS.objects.filter(
            pk__in=relevant_wns_ids).values('id', 'wns_oms')
        result['color_by_fields'] = color_by_fields

        result['min_value'] = min_value
        result['max_value'] = max_value
        result['color_by_name'] = color_by_name
        return Response(result)


class OpnamesAPI(FilteredOpnamesAPIView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [CSVRenderer]

    def get(self, request, format=None):
        # TODO: refactor pagination stuff with djangorestframework 3.1
        loc_id_filter = self.request.query_params.get('loc_id')
        wns_oms_filter = self.request.query_params.get('wns_oms')
        loc_oms_filter = self.request.query_params.get('loc_oms')
        activiteit_filter = self.request.query_params.get('activiteit')
        detectiegrens_filter = self.request.query_params.get('detectiegrens')
        waarde_n_filter = self.request.query_params.get('waarde_n')
        sort_fields = self.request.query_params.get('sort_fields')
        sort_dirs = self.request.query_params.get('sort_dirs')
        ITEMS_PER_PAGE = 30

        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
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
        if sort_fields and sort_dirs:
            filtered_opnames = self.order_opnames(
                sort_fields, sort_dirs, filtered_opnames)

        if page_size not in [None, '']:
            ITEMS_PER_PAGE = page_size

        filtered_opnames = filtered_opnames.select_related(
            'locatie__loc_id',
            'locatie__loc_oms',
            'wns__wns_oms',
            'activiteit__activiteit',
            'detect__teken',
            'wns__parameter__par_oms',
            )

        if request.query_params.get('format') == 'csv':
            serializer = serializers.OpnameSerializer(
                filtered_opnames,
                many=True,
                context={'request': request})
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
            context={'request': request})
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
            ordering.append('%s%s' % (direction_sign, fieldname))
        filtered_opnames = filtered_opnames.order_by(*ordering)
        return filtered_opnames


class LinesAPI(FilteredOpnamesAPIView):
    """API to return lines for a graph."""

    def get(self, request, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        points = numerical_opnames.values(
            'wns__wns_code', 'wns__wns_oms', 'wns__parameter__par_code',
            'wns__eenheid__eenheid',
            'locatie__loc_id', 'locatie__loc_oms',
            'datum', 'tijd', 'waarde_n')

        def _key(point):
            return '%s_%s' % (point['wns__wns_code'], point['locatie__loc_id'])

        lines = []
        for key, group in groupby(points, _key):
            points = list(group)
            first = points[0]
            data = [{'datetime': '%sT%s.000Z' % (point['datum'], point['tijd']),
                     'value': point['waarde_n']} for point in points]
            line = {'wns': first['wns__wns_oms'],
                    'location': first['locatie__loc_oms'],
                    'unit': first['wns__eenheid__eenheid'],
                    'data': data,
                    'id': key}
            lines.append(line)

        return Response(lines)
