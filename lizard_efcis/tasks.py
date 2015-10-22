from __future__ import absolute_import

import logging
import os

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from lizard_efcis import validation
from lizard_efcis.import_data import DataImport
from lizard_efcis.models import FTPLocation, Opname
from lizard_efcis import export_data

logger = logging.getLogger(__name__)


EXPORT_DIR = "task_export/"


@shared_task
def add(x, y):
    return x + y


@shared_task
def export_opnames_to_csv(to_email, query, filename, import_mapping, domain):
    """
    Argument query of django.db.models.sql.query.Query

    contains filters, ordering, etc.
    """
    body = ""
    export_dir = os.path.join(settings.MEDIA_ROOT, EXPORT_DIR)
    queryset = Opname.objects.all()
    queryset.query = query
    queryset = queryset.prefetch_related(
            'locatie',
            'locatie__watertype',
            'wns',
            'activiteit',
            'detect',
            'wns__parameter',
            'wns__eenheid',
            'wns__hoedanigheid',
            'wns__compartiment',
            'locatie__waterlichaam',
    )
    if not os.path.isdir(export_dir):
        body = "'%s' is geen export directory."
        send_mail('EFCIS: Fout bij csv-export',
                  body,
                  settings.DEFAULT_FROM_EMAIL,
                  [to_email])
        return
    filepath = os.path.join(export_dir, filename)
    with open(filepath, 'wb') as csv_file:
        writer = export_data.UnicodeWriter(
            csv_file,
            dialect='excel',
            delimiter=str(import_mapping.scheiding_teken))
        for row in export_data.get_csv_context(
                queryset, import_mapping):
            writer.writerow(row)
        url = ''.join([domain,
                       settings.MEDIA_URL,
                       EXPORT_DIR,
                       filename])
        body = '<html><body>CSV-export is klaar en kan opgehaald worden via deze link '\
               '<a href="%s">%s</a>.</body></html>' % (url, url)
        send_mail('EFCIS: CSV-export',
                  settings.DEFAULT_FROM_EMAIL,
                  [to_email],
                  html_message=body
        )


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
def validate_opnames_min_max(queryset, to_email):
    messages = validation.MinMaxValidator(queryset).validate()
    body = '\n'.join(['De validatie is klaar.', ''] + messages)
    send_mail('De validatie is klaar',
              body,
              settings.DEFAULT_FROM_EMAIL,
              [to_email])


@shared_task
def validate_stddev(queryset, period_to_look_back, to_email):
    messages = validation.StandardDeviationValidator(
        queryset,
        period_to_look_back=period_to_look_back).validate()
    body = '\n'.join(['De validatie is klaar.', ''] + messages)
    send_mail('De validatie is klaar',
              body,
              settings.DEFAULT_FROM_EMAIL,
              [to_email])
