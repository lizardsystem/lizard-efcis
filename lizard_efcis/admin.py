# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import messages
from django.conf import settings

from lizard_efcis import models
from lizard_efcis import tasks


def check_file(modeladmin, request, queryset):

    for import_run in queryset:
        can_run, warn_messages = import_run.can_run_any_action()
        if not can_run:
            messages.warning(
                request,
                "Controle van '%s' NIET uitgevoerd: '%s'." %
                (import_run.name, ', '.join(warn_messages)))
            continue
        if settings.CELERY_MIN_FILE_SIZE < (
                import_run.attachment.size / 1024 / 1024):
            task_result = tasks.check_file.delay(
                request.user.get_full_name(),
                import_run=import_run)
            messages.success(
                request,
                "Controle wordt uitgevoerd op achtergrond, "
                "want het bestand is te groot '%s', status '%s'." % (
                    import_run.name, task_result.status))
        else:
            tasks.check_file(
                request.user.get_full_name(),
                import_run=import_run)
            messages.success(
                request,
                "Controle van '%s' is uitgevoerd." % import_run.name)
check_file.short_description = "Controleer geselecteerde imports"


def import_csv(modeladmin, request, queryset):

    for import_run in queryset:
        if not import_run.validated:
            messages.warning(
                request,
                "Import van '%s' NIET uitgevoerd:"
                " niet valid." % import_run.name)
            continue
        can_run, warn_messages = import_run.can_run_any_action()
        if not can_run:
            messages.warning(
                request,
                "Import van '%s' NIET uitgevoerd: '%s'." %
                (import_run.name, ', '.join(warn_messages)))
            continue
        if settings.CELERY_MIN_FILE_SIZE < (
                import_run.attachment.size / 1024 / 1024):
            task_result = tasks.import_data.delay(
                request.user.get_full_name(),
                importrun=import_run)
            messages.success(
                request,
                "Import wordt uitgevoerd op achtergrond, "
                "want het bestand is te groot '%s', status '%s'." % (
                    import_run.name, task_result.status))
        else:
            tasks.import_data(
                request.user.get_full_name(),
                importrun=import_run)
            messages.success(
                request,
                "Import van '%s' is uitgevoerd." % import_run.name)
import_csv.short_description = "Uitvoeren geselecteerde imports"


@admin.register(models.ImportRun)
class ImportRunAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'attachment',
                    'activiteit',
                    'uploaded_by',
                    'uploaded_date',
                    'validated',
                    'imported']
    list_filter = ['type_run', 'uploaded_by']
    search_fields = ['name', 'uploaded_by', 'attachment', 'activiteit']
    actions = [check_file, import_csv]
    readonly_fields = ['validated', 'imported']


class MappingFieldInlineAdmin(admin.TabularInline):
    model = models.MappingField


@admin.register(models.ImportMapping)
class ImportMappingAdmin(admin.ModelAdmin):
    inlines = [MappingFieldInlineAdmin]


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['naam']


@admin.register(models.Eenheid)
class EenheidAdmin(admin.ModelAdmin):
    list_display = ['eenheid',
                    'eenheid_oms',
                    'dimensie',
                    'eenheidgroep',
                    'datum_status',
                    'status']
    list_filter = ['eenheidgroep',
                   'dimensie',
                   'status']


@admin.register(models.Hoedanigheid)
class HoedanigheidAdmin(admin.ModelAdmin):
    list_display = ['hoedanigheid',
                    'hoed_oms',
                    'hoedanigheidgroep',
                    'datum_status',
                    'status']
    list_filter = ['hoedanigheidgroep',
                   'status']


@admin.register(models.Compartiment)
class CompartimentAdmin(admin.ModelAdmin):
    list_display = ['compartiment',
                    'comp_oms',
                    'compartimentgroep',
                    'datum_status',
                    'status']
    list_filter = ['compartimentgroep',
                   'status']


@admin.register(models.Detectiegrens)
class DetectiegrensAdmin(admin.ModelAdmin):
    list_display = ['teken',
                    'omschrijving']


@admin.register(models.Locatie)
class LocatieAdmin(admin.ModelAdmin):

    list_display = ['loc_id',
                    'loc_oms',
                    'waterlichaam',
                    'watertype']
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
                     'parameter__par_oms']
    list_select_related = ['parameter__code', 'eenheid__eenheid']


@admin.register(models.ParameterGroep)
class ParameterGroepAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']


@admin.register(models.Parameter)
class Parameter(admin.ModelAdmin):
    search_fields = ['par_code',
                    'par_oms',
                    'casnummer',
                    'datum_status',
                    'status',
                    'parametergroep']
    list_display = ['par_code',
                    'par_oms',
                    'casnummer',
                    'datum_status',
                    'status',
                    'parametergroep']
    list_filter = ['parametergroep',
                   'status']


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
                    'met_toets',
                    'uitvoerende']
    list_filter = ['act_type',
                   'uitvoerende']
    search_fields = ['activiteit',
                     'act_oms']


@admin.register(models.Uitvoerende)
class UitvoerendeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
