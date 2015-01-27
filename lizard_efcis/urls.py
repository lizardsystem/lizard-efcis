# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from rest_framework import routers

from lizard_efcis import views

admin.autodiscover()

router = routers.DefaultRouter()

urlpatterns = patterns(
    'lizard_efcis.views',
    url(r'^$', 'api_root'),
    url(r'^opnames/$', 'opname_list', name='opname-list'),
    #url(r'^$', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^something/',
    #     views.some_method,
    #     name="name_it"),
    # url(r'^something_else/$',
    #     views.SomeClassBasedView.as_view(),
    #     name='name_it_too'),
    )
#urlpatterns += debugmode_urlpatterns()
