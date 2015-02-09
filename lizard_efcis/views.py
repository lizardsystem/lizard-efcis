# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import logging
from datetime import datetime

from django.utils.translation import ugettext as _

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

from lizard_efcis import models
from lizard_efcis import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


logger = logging.getLogger(__name__)


def str_to_datetime(dtstr):
    dtformat = "%d-%m-%Y"
    dt = None
    try:
        dt = datetime.strptime(dtstr, dtformat)
    except:
        logger.warn("Error on formating datimestr to datetime"
                    "{0} not match to {1}.".format(dtstr, dtformat))
    return dt


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
    if startdatetime and enddatetime:
        queryset = queryset.filter(
            moment__gt=startdatetime,
            moment__lt=enddatetime)
    if location:
        queryset = queryset.filter(
            locatie__loc_id__iexact=location)

    return queryset


@api_view()
def api_root(request, format=None):
    return Response({
        'opnames': reverse(
            'opname-list',
            request=request,
            format=format),
    })


@api_view(['GET'])
def opname_list(request):

    ITEMS_PER_PAGE = 30

    if request.method == 'GET':

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
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def opname_detail(request, pk):

    try:
        opname = models.Opname.objects.get(pk=pk)
    except models.Opname.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.OpnameDetailSerializer(
            opname, context={'request': request})
        return Response(serializer.data)
    else:
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED)
