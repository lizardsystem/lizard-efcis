# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count

from lizard_efcis import models


class MappingFieldInlineAdmin(admin.TabularInline):
    model = models.MappingField


class ImportMappingAdmin(admin.ModelAdmin):
    inlines = [MappingFieldInlineAdmin]


@admin.register(models.Locatie)
class LocatieAdmin(admin.ModelAdmin):

    list_display = ['loc_id',
                    'loc_oms',
                    'waterlichaam',
                    'watertype',
    ]
    search_fields = ['loc_id',
                     'loc_oms']
    list_filter = ['waterlichaam',
                   'watertype',
                   'status_fc',
                   'status_bio']


@admin.register(models.Meetnet)
class MeetnetAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']


@admin.register(models.Opname)
class OpnameAdmin(admin.ModelAdmin):
    list_display = ['wns',
                    'locatie',
                    'waarde_n',
                    'waarde_a',
                    'datum',
                    'tijd']
    search_fields = ['wns__wns_oms',
                     'locatie__loc_oms']
    list_filter = ['datum']


@admin.register(models.WNS)
class WNSAdmin(admin.ModelAdmin):

    list_display = ['wns_code',
                    'wns_oms',
                    'parameter',
                    'eenheid']
    search_fields = ['wns_code',
                     'wns_oms',
                     'parameter__par_code',
                     'parameter__par_oms',
                 ]
    list_select_related = ['parameter__code', 'eenheid__eenheid']


@admin.register(models.ParameterGroep)
class ParameterGroepAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']


@admin.register(models.StatusKRW)
class StatusKRWAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'omschrijving',
                    'datum_status',
                    'datum_begin',
                    'datum_eind']


@admin.register(models.Waterlichaam)
class WaterlichaamAdmin(admin.ModelAdmin):
    list_display = ['wl_code',
                    'wl_naam',
                    'wl_type',
                    'wl_oms',
                    'status']
    list_filter = ['wl_type',
                   'status']
    search_fields = ['wl_code',
                     'wl_naam']


@admin.register(models.Watertype)
class WatertypeAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'omschrijving',
                    'groep',
                    'datum_status',
                    'datum_begin',
                    'datum_eind']
    list_filter = ['groep',
                   'datum_status']
    search_fields = ['code',
                     'omschrijving']


@admin.register(models.Activiteit)
class ActiviteitAdmin(admin.ModelAdmin):
    list_display = ['activiteit',
                    'act_oms',
                    'act_type',
                    'met_mafa',
                    'met_mafy',
                    'met_fyt',
                    'met_vis',
                    'met_fc',
                    'met_toets']
    list_filter = ['act_type',
                   'uitvoerende']
    search_fields = ['activiteit',
                     'act_oms']
