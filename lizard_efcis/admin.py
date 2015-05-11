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


class LocatieAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(LocatieAdmin, self).get_queryset(request)
        return qs.annotate(aantal_opnames=Count('opnames'))

    def aantal_opnames(self, inst):
        return inst.aantal_opnames

    aantal_opnames.admin_order_field = 'aantal_opnames'

    list_display = ['loc_id',
                    'loc_oms',
                    'waterlichaam',
                    'watertype',
                    'aantal_opnames']
    search_fields = ['loc_id',
                     'loc_oms']
    list_filter = ['waterlichaam',
                   'watertype',
                   'status_fc',
                   'status_bio']


class MeetnetAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']


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


class WNSAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(WNSAdmin, self).get_queryset(request)
        return qs.annotate(
            aantal_opnames=Count('opnames')).select_related(
                'parameter__code', 'eenheid__eenheid')

    def aantal_opnames(self, inst):
        return inst.aantal_opnames

    aantal_opnames.admin_order_field = 'aantal_opnames'

    list_display = ['wns_code',
                    'wns_oms',
                    'parameter',
                    'eenheid',
                    'aantal_opnames']
    search_fields = ['wns_code',
                     'wns_oms',
                     'parameter__par_code',
                     'parameter__par_oms',
                 ]


class ParameterGroepAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']


class StatusKRWAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'omschrijving',
                    'datum_status',
                    'datum_begin',
                    'datum_eind']


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


admin.site.register(models.ImportMapping, ImportMappingAdmin)
admin.site.register(models.Locatie, LocatieAdmin)
admin.site.register(models.Meetnet, MeetnetAdmin)
admin.site.register(models.Opname, OpnameAdmin)
admin.site.register(models.ParameterGroep, ParameterGroepAdmin)
admin.site.register(models.StatusKRW, StatusKRWAdmin)
admin.site.register(models.Waterlichaam, WaterlichaamAdmin)
admin.site.register(models.Watertype, WatertypeAdmin)
admin.site.register(models.Activiteit, ActiviteitAdmin)
admin.site.register(models.WNS, WNSAdmin)
