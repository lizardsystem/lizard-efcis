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
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

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


def get_filtered_opnames(queryset, request):

    location = request.QUERY_PARAMS.get('locatie')
    startdatetime = str_to_datetime(
        request.QUERY_PARAMS.get('start_date'))
    enddatetime = str_to_datetime(
        request.QUERY_PARAMS.get('end_date'))
    par_code = request.QUERY_PARAMS.get('par_code')
    if par_code:
        queryset = queryset.filter(
            wns__parameter__par_code__iexact=par_code)
    if startdatetime:
        queryset = queryset.filter(
            datum__gt=startdatetime)
    if enddatetime:
        queryset = queryset.filter(
            datum__lt=enddatetime)
    if location:
        queryset = queryset.filter(
            locatie__loc_id__iexact=location)

    return queryset


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
    })


@api_view()
def opname_list(request):

    ITEMS_PER_PAGE = 30

    page = request.QUERY_PARAMS.get('page')
    page_size = request.QUERY_PARAMS.get('page_size')
    if page_size not in [None, '']:
        ITEMS_PER_PAGE = page_size
    queryset = get_filtered_opnames(
        models.Opname.objects.all(),
        request)

    paginator = Paginator(queryset, ITEMS_PER_PAGE)
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


class LinesAPI(APIView):
    """API to return lines for a graph."""

    # TODO: use
    # http://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
    # to get some basic pagination stuff for free.

    @property
    def filtered_opnames(self):
        opnames = models.Opname.objects.all()

        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        locations = self.request.GET.getlist('locatie', None)
        parameter_codes = self.request.GET.getlist('par_code', None)

        if start_date:
            start_datetime = str_to_datetime(start_date)
            if start_datetime:
                opnames = opnames.filter(datum__gt=start_datetime)
        if end_date:
            end_datetime = str_to_datetime(end_date)
            if end_datetime:
                opnames = opnames.filter(datum__tt=end_datetime)
        if locations:
            opnames = opnames.filter(locatie__loc_id__in=locations)
        if parameter_codes:
            opnames = opnames.filter(
                wns__parameter__par_code__in=parameter_codes)

        return opnames

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
            data = [{'date': point['datum'],
                     'time': point['tijd'],
                     'value': point['waarde_n']} for point in points]
            line = {'wns': first['wns__wns_oms'],
                    'location': first['locatie__loc_oms'],
                    'unit': first['wns__parameter__par_code'],
                    'data': data}
            lines.append(line)

        return Response(lines)
