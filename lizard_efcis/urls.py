# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

from lizard_efcis import views

router = routers.DefaultRouter()

urlpatterns = patterns(
    'lizard_efcis.views',
    url(r'^$', 'api_root'),
    url(r'^opnames/$',
        views.OpnamesAPI.as_view(),
        name='efcis-opname-list'),
    url(r'^opnames/(?P<pk>[0-9]+)/$',
        'opname_detail',
        name='opname-detail'),

    url(r'^graphs/$',
        views.GraphsAPI.as_view(),
        name='efcis-graphs'),
    url(r'^lines/(?P<key>[^/]+)/$',
        views.LineAPI.as_view(),
        name='efcis-line'),
    url(r'^boxplots/(?P<key>[^/]+)/$',
        views.BoxplotAPI.as_view(),
        name='efcis-boxplot'),
    url(r'^scatterplots/(?P<axis1_key>[^/]+)/$',
        views.ScatterplotSecondAxisAPI.as_view(),
        name='efcis-scatterplot-second-axis'),
    url(r'^scatterplots/(?P<axis1_key>[^/]+)/(?P<axis2_key>[^/]+)/$',
        views.ScatterplotGraphAPI.as_view(),
        name='efcis-scatterplot-graph'),

    url(r'^parametergroeps/$',
        views.ParameterGroepAPI.as_view(),
        name='efcis-parametergroep-tree'),

    url(r'^parameters/$',
        views.ParameterAPI.as_view(),
        name='efcis-parameters-list'),

    url(r'^locaties/$',
        views.LocatieAPI.as_view(),
        name='efcis-locaties-list'),

    url(r'^map/$',
        views.MapAPI.as_view(),
        name='efcis-map'),

    url(r'^meetnetten/$',
        views.MeetnetAPI.as_view(),
        name='efcis-meetnet-tree'),
    # url(r'^$', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    )
