from __future__ import absolute_import

import logging
from celery import shared_task

from lizard_efcis import validation
from lizard_efcis.import_data import DataImport
from lizard_efcis.models import FTPLocation

logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    return x + y


@shared_task
def ftpimport():
    from lizard_efcis import ftp_access
    for ftp_location in FTPLocation.objects.all():
        ftp_access.handle_first_file(ftp_location)


@shared_task
def check_file(username, importrun, *args, **options):
    """Check passed importrun or
    all active automatic importruns"""
    data_import = DataImport()
    datetime_format = '%Y-%m-%d %H:%M'
    if importrun is None:
        logger.debug("Error: ImportRun is None")
        return
    importrun.add_log_separator()
    importrun.add_log_line("Start controle", username=username)
    importrun.save(force_update=True, update_fields=['action_log'])
    if importrun.has_xml_attachment:
        result = data_import.check_xml(importrun, datetime_format)
    elif importrun.has_csv_attachment:
        result = data_import.check_csv(importrun, datetime_format)
    else:
        importrun.add_log_line(
            "Niet uitgevoerd, bestandsextentie is geen .csv of .xml")
    importrun.add_log_line("Controle status is %s" % result)
    importrun.add_log_line("Eind controle", username=username)
    importrun.validated = result
    importrun.uploaded_by = username
    importrun.save()


@shared_task
def import_data(username, importrun, *args, **options):
    """Import data from csv"""
    data_import = DataImport()
    datetime_format = '%Y-%m-%d %H:%M'
    data_import.log = False
    if importrun is None:
        logger.debug("ImportRun is Nones")
        return

    importrun.add_log_separator()
    importrun.add_log_line("Start import", username)
    importrun.save(force_update=True, update_fields=['action_log'])
    if importrun.has_xml_attachment:
        result = data_import.manual_import_xml(importrun, datetime_format)
    elif importrun.has_csv_attachment:
        result = data_import.manual_import_csv(importrun, datetime_format)
    else:
        importrun.add_log_line(
            "Niet uitgevoerd, bestandsextentie is geen .csv of .xml")
    importrun.add_log_line("Import status is %s" % result)
    importrun.add_log_line("Eind import", username)
    importrun.imported = result
    importrun.uploaded_by = username
    importrun.save()


@shared_task
def validate_opnames_min_max(queryset):
    messages = validation.MinMaxValidator(queryset).validate()
    if messages:
        logger.debug('/n'.join(messages))


@shared_task
def validate_stddev(queryset, period_to_look_back):
    messages = validation.StandardDeviationValidator(
        queryset,
        period_to_look_back=period_to_look_back).validate()
