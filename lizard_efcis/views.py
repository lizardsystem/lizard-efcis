# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from itertools import groupby
import logging
import json

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics

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
                json.loads(parametergroups))
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

    # TODO: use
    # http://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
    # to get some basic pagination stuff for free.

    @property
    def filtered_opnames(self):
        opnames = models.Opname.objects.all()

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        locations = self.request.query_params.getlist('locatie')
        parametergroep_id = self.request.query_params.get('parametergroep')
        meetnet_id = self.request.query_params.get('meetnet')
        parameter_ids = self.request.query_params.get('parameters')
        if start_date:
            start_datetime = str_to_datetime(start_date)
            if start_datetime:
                opnames = opnames.filter(datum__gt=start_datetime)
        if end_date:
            end_datetime = str_to_datetime(end_date)
            if end_datetime:
                opnames = opnames.filter(datum__lt=end_datetime)
        if locations:
            opnames = opnames.filter(locatie__loc_id__in=locations)
        if parametergroep_id:
            par_groepen = models.ParameterGroep.objects.filter(
                Q(id=parametergroep_id) |
                Q(parent=parametergroep_id) |
                Q(parent__parent=parametergroep_id))

            opnames = opnames.filter(
                wns__parameter__parametergroep__in=par_groepen)
        if meetnet_id:
            meetnetten = models.Meetnet.objects.filter(
                Q(id=meetnet_id) |
                Q(parent=meetnet_id) |
                Q(parent__parent=meetnet_id) |
                Q(parent__parent__parent=meetnet_id) |
                Q(parent__parent__parent__parent=meetnet_id)
            )

            opnames = opnames.filter(
                locatie__meetnet__in=meetnetten)
        if parameter_ids:
            ids_list = json.loads(parameter_ids)
            opnames = opnames.filter(wns__parameter__id__in=ids_list)
        return opnames


class LocatieAPI(generics.ListAPIView):

    model = models.Locatie
    serializer_class = serializers.LocatieSerializer
    paginate_by_param = 'page_size'
    paginate_by = 50
    max_page_size = 500

    def get_queryset(self):
        meetnet_id = self.request.query_params.get('meetnet')
        locaties = None
        if meetnet_id is None:
            locaties = models.Locatie.objects.all()
        else:
            meetnetten = models.Meetnet.objects.filter(
                Q(id=meetnet_id) |
                Q(parent=meetnet_id) |
                Q(parent__parent=meetnet_id) |
                Q(parent__parent__parent=meetnet_id) |
                Q(parent__parent__parent__parent=meetnet_id)
            )
            locaties = models.Locatie.objects.filter(meetnet__in=meetnetten)
        return locaties


class OpnamesAPI(FilteredOpnamesAPIView):

    def get(self, request, format=None):
        # TODO: refactor pagination stuff with djangorestframework 3.1
        ITEMS_PER_PAGE = 30

        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        if page_size not in [None, '']:
            ITEMS_PER_PAGE = page_size
        paginator = Paginator(self.filtered_opnames, ITEMS_PER_PAGE)
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


class LinesAPI(FilteredOpnamesAPIView):
    """API to return lines for a graph."""

    def get(self, request, format=None):
        numerical_opnames = self.filtered_opnames.exclude(waarde_n=None)
        points = numerical_opnames.values(
            'wns__wns_code', 'wns__wns_oms', 'wns__parameter__par_code',
            'locatie__loc_id', 'locatie__loc_oms',
            'datum', 'tijd', 'waarde_n')[:500]
        # :500 is a temporary limit.

        def _key(point):
            return (point['wns__wns_code'], point['locatie__loc_id'])

        lines = []
        for key, group in groupby(points, _key):
            points = list(group)
            first = points[0]
            data = [{'datetime': '%s %s' % (point['datum'], point['tijd']),
                     'value': point['waarde_n']} for point in points]
            line = {'wns': first['wns__wns_oms'],
                    'location': first['locatie__loc_oms'],
                    'unit': first['wns__parameter__par_code'],
                    'data': data}
            lines.append(line)

        return Response(lines)
