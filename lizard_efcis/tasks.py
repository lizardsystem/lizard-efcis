from __future__ import absolute_import

from celery import shared_task

from lizard_efcis.import_data import DataImport
from lizard_efcis.models import ImportRun


@shared_task
def add(x, y):
    return x + y


@shared_task
def check_file(username, import_run=None, *args, **options):
    """Check passed import_run or
    all active automatic import_runs"""
    import_runs = []
    data_import = DataImport()
    datetime_format = '%Y-%m-%d %H:%M'
    if import_run:
        import_runs.append(import_run)
    else:
        import_runs = list(ImportRun.objects.filter(
            **{'type_run': ImportRun.AUTO, 'actief': True}))
    for import_run in import_runs:
        import_run.add_log_separator()
        import_run.add_log_line("Start controle",
                                username=username)
        import_run.save(force_update=True, update_fields=['action_log'])
        if import_run.has_xml_attachment:
            result = data_import.check_xml(
                import_run, datetime_format)
        elif import_run.has_csv_attachment:
            result = data_import.check_csv(
                import_run, datetime_format)
        else:
            import_run.add_log_line(
                "Niet uitgevoerd, bestandsextentie is geen .csv of .xml")
            continue
        import_run.add_log_line("Controle status is %s" % result)
        import_run.add_log_line("Eind controle", username=username)
        import_run.validated = result
        import_run.uploaded_by = username
        import_run.save()


@shared_task
def import_data(username, importrun=None, *args, **options):
    """Import data from csv"""
    import_runs = []
    data_import = DataImport()
    datetime_format = '%Y-%m-%d %H:%M'
    data_import.log = False
    if importrun:
        import_runs.append(importrun)
    else:
        import_runs = list(ImportRun.objects.filter(
            **{'type_run': ImportRun.AUTO, 'actief': True}))
    for import_run in import_runs:
        import_run.add_log_separator()
        import_run.add_log_line("Start import",
                                username)
        import_run.save(force_update=True, update_fields=['action_log'])
        if import_run.has_xml_attachment:
            result = data_import.manual_import_xml(
                import_run, datetime_format)
        elif import_run.has_csv_attachment:
            result = data_import.manual_import_csv(
                import_run, datetime_format)
        else:
            import_run.add_log_line(
                "Niet uitgevoerd, bestandsextentie is geen .csv of .xml")
            continue
        import_run.add_log_line("Import status is %s" % result)
        import_run.add_log_line("Eind import", username)
        import_run.imported = result
        import_run.uploaded_by = username
        import_run.save()
