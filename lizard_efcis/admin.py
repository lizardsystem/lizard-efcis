# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.utils.text import slugify

from lizard_efcis import ftp_access
from lizard_efcis import models
from lizard_efcis import tasks
from lizard_efcis.manager import VALIDATED


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
            tasks.check_file.delay(
                request.user.get_full_name(),
                importrun=import_run)
            messages.success(
                request,
                "Controle wordt uitgevoerd op achtergrond, "
                "volg de voortgang in 'Action log' veld van '%s'." % (
                    import_run.name))
        else:
            tasks.check_file(
                request.user.get_full_name(),
                importrun=import_run)
            messages.success(
                request,
                "Controle van '%s' is uitgevoerd." % import_run.name)
check_file.short_description = "Controleer geselecteerde imports"


def import_file(modeladmin, request, queryset):

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
            tasks.import_data.delay(
                request.user.get_full_name(),
                importrun=import_run)
            messages.success(
                request,
                "Import wordt uitgevoerd op achtergrond, "
                "volg de voortgang in 'Action log' veld van '%s'." % (
                    import_run.name))
        else:
            tasks.import_data(
                request.user.get_full_name(),
                importrun=import_run)
            messages.success(
                request,
                "Import van '%s' is uitgevoerd." % import_run.name)
import_file.short_description = "Uitvoeren geselecteerde imports"


def download_csv(modeladmin, request, queryset):
    if queryset.model == models.Locatie:
        mapping_code = 'locaties'
        queryset = queryset.prefetch_related(
            'meet_status',
            'meetnet',
            'status_krw',
            'waterlichaam',
            'watertype'
        )
    elif queryset.model == models.ParameterGroep:
        mapping_code = 'parametergroep-export'
        queryset = queryset.prefetch_related('parent')
    elif queryset.model == models.Meetnet:
        mapping_code = 'meetnet'
        queryset = queryset.prefetch_related('parent')
    elif queryset.model == models.Parameter:
        mapping_code = 'parameter'
        queryset = queryset.prefetch_related(
            'parametergroep',
            'status')
    elif queryset.model == models.WNS:
        mapping_code = 'waarnemingssoorten'
        queryset = queryset.prefetch_related(
            'compartiment',
            'eenheid',
            'hoedanigheid',
            'parameter',
            'wns_status')
    else:
        messages.warning(
            request,
            "Export voor de tabel '%s' is niet aanwezig." % (
                queryset.model.__name__))
        return

    import_mapping = models.ImportMapping.objects.get(
        code=mapping_code)

    filename = "%s-%s.csv" % (
        slugify(import_mapping.code),
        datetime.now().strftime("%Y-%m-%d_%H%M"))
    tasks.export_to_csv.delay(
        request.user.email,
        queryset.query,
        filename,
        import_mapping,
        request.get_host()
    )
    messages.success(
        request,
        "Exporteren is gestart "
        "U ontvangt een e-mail (adres: %s) met een downloadlink "
        "als de export gereed is. Deze link blijft geldig tot "
        "middernacht" % request.user.email
    )
download_csv.short_description = "Download CSV"


def validate_opnames_min_max(modeladmin, request, queryset):
    to_email = request.user.email
    tasks.validate_opnames_min_max.delay(queryset, to_email)
    messages.success(request, "Taak is gestart.")
validate_opnames_min_max.short_description = (
    "Valideer volgens ingestelde min/max")


def validate_stddev_half_year(modeladmin, request, queryset):
    to_email = request.user.email
    tasks.validate_stddev.delay(queryset, 365/2, to_email)
    messages.success(request, "Taak is gestart.")
validate_stddev_half_year.short_description = (
    "Valideer t.o.v. waardes afgelopen halfjaar")


def validate_stddev_1year(modeladmin, request, queryset):
    to_email = request.user.email
    tasks.validate_stddev.delay(queryset, 365, to_email)
    messages.success(request, "Taak is gestart.")
validate_stddev_1year.short_description = (
    "Valideer t.o.v. waardes afgelopen jaar")


def validate_stddev_2year(modeladmin, request, queryset):
    to_email = request.user.email
    tasks.validate_stddev.delay(queryset, 365 * 2, to_email)
    messages.success(request, "Taak is gestart.")
validate_stddev_2year.short_description = (
    "Valideer t.o.v. waardes afgelopen twee jaar")


def validate_stddev_5year(modeladmin, request, queryset):
    to_email = request.user.email
    tasks.validate_stddev.delay(queryset, 365 * 5, to_email)
    messages.success(request, "Taak is gestart.")
validate_stddev_5year.short_description = (
    "Valideer t.o.v. waardes afgelopen vijf jaar")


def validate_stddev_all(modeladmin, request, queryset):
    to_email = request.user.email
    tasks.validate_stddev.delay(queryset, 365 * 99, to_email)
    messages.success(request, "Taak is gestart.")
validate_stddev_all.short_description = (
    "Valideer t.o.v. alle waardes")


def mark_as_validated(modeladmin, request, queryset):
    num_updated = 0
    for opname in queryset:
        if opname.validation_state != VALIDATED:
            opname.validation_state = VALIDATED
            opname.save()
            num_updated += 1
    messages.success(request, "%s opnames op gevalideerd gezet" % num_updated)
mark_as_validated.short_description = (
    "Markeer rechtstreeks als gevalideerd")


def ftp_connection_test(modeladmin, request, queryset):
    result = ''
    for ftp_location in queryset:
        result += ftp_access.debug_info(ftp_location)
    response = HttpResponse(content_type='text/plain')
    response.write(result)
    return response
ftp_connection_test.short_description = "Test the FTP connection"


def ftp_run_import(modeladmin, request, queryset):
    result = ''
    for ftp_location in queryset:
        result += ftp_access.handle_first_file(ftp_location)
    response = HttpResponse(content_type='text/plain')
    response.write(result)
    return response
ftp_run_import.short_description = "Import oldest available FTP file"


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
    search_fields = ['name',
                     'uploaded_by',
                     'attachment',
                     'activiteit__activiteit'
    ]
    raw_id_fields = ['activiteit']
    actions = [check_file, import_file]
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
                   'is_krw_area',
                   'meet_status',
                   'landgebruik',
                   'afvoergebied',
                   'grondsoort']
    filter_horizontal = ['meetnet']
    actions = [download_csv]


@admin.register(models.Meetnet)
class MeetnetAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']
    actions = [download_csv]


@admin.register(models.Opname)
class OpnameAdmin(admin.ModelAdmin):
    list_display = ['wns',
                    'locatie',
                    'waarde_n',
                    'waarde_a',
                    'datum',
                    'validation_state',
                    'opmerkingen',
                    'vis_opp_ha',
                    'vis_kg',
                    'vis_cm']
    search_fields = ['wns__wns_code',
                     'wns__wns_oms',
                     'locatie__loc_oms',
                     'locatie__loc_id']
    raw_id_fields = ['wns',
                     'locatie']
    list_filter = ['datum',
                   'validation_state']
    actions = [validate_opnames_min_max,
               validate_stddev_half_year,
               validate_stddev_1year,
               validate_stddev_2year,
               validate_stddev_5year,
               validate_stddev_all,
               mark_as_validated]


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
    raw_id_fields = ['parameter']
    list_select_related = ['parameter__code', 'eenheid__eenheid']
    list_filter = ['wns_status']
    actions = [download_csv]


@admin.register(models.ParameterGroep)
class ParameterGroepAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'parent']
    actions = [download_csv]


@admin.register(models.Parameter)
class Parameter(admin.ModelAdmin):
    search_fields = ['par_code',
                     'par_oms',
                     'par_oms_nl',
                     'casnummer']
    list_display = ['par_code',
                    'par_oms',
                    'par_oms_nl',
                    'casnummer',
                    'datum_status',
                    'status',
                    'parametergroep']
    list_filter = ['parametergroep',
                   'status']
    actions = [download_csv]


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
                    'status_krw']
    list_filter = ['wl_type',
                   'status_krw']
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


@admin.register(models.FTPLocation)
class FTPLocationAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'directory', 'username']
    actions = [ftp_connection_test,
               ftp_run_import]


@admin.register(models.MeetStatus)
class MeetStatusAdmin(admin.ModelAdmin):
    list_display = ['naam', 'omschrijving', 'index']
    search_fields = ['naam']
