from __future__ import absolute_import

from datetime import datetime
from celery import shared_task

from lizard_efcis.import_data import DataImport
from lizard_efcis.models import ImportRun
from lizard_efcis import utils

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
        import_run.action_log = utils.add_text_to_top(
            import_run.action_log,
            '-------------------------------\n')
        import_run.action_log = utils.add_text_to_top(
            import_run.action_log,
            "%s %s %s.\n" % (
            datetime.now().strftime(datetime_format),
            "Start controle", 
            username))
        import_run.save(force_update=True, update_fields=['action_log'])
        result = data_import.check_csv(
            import_run, datetime_format)
        
        import_run.action_log = utils.add_text_to_top(
            import_run.action_log,
            "%s %s: %s.\n" % (
                datetime.now().strftime(datetime_format),
                "Controle status",
                result))
        import_run.action_log = utils.add_text_to_top(
            import_run.action_log,
            "%s %s.\n" % (
                datetime.now().strftime(datetime_format),
                "Eind controle"))
        import_run.validated = result
        import_run.uploaded_by = username
        import_run.save()


@shared_task
def import_data(username, importrun=None, *args, **options):
    """Validate passed import_run or
    all active automatic import_runs"""
    import_runs = []
    data_import = DataImport()
    data_import.log = False
    if importrun:
        import_runs.append(importrun)
    else:
        import_runs = list(ImportRun.objects.filter(
            **{'type_run': ImportRun.AUTO, 'actief': True}))
    for import_run in import_runs:
        action_log = '-------------------------------\n'
        action_log += "Begin import, %s %s.\n" % (
            datetime.now().strftime('%Y-%m-%d %H:%M'),
            username)
        result = data_import.manual_import_csv(
            import_run.attachment.path,
            import_run.import_mapping.code,
            activiteit=import_run.activiteit
        )
        for code, message in result[1].iteritems():
            action_log += '%s: %s\n' % (code, message)
        action_log += 'Eind import, %s.\n' % (
            datetime.now().strftime('%Y-%m-%d %H:%M'))
        import_run.action_log = utils.add_text_to_top(
            import_run.action_log,
            utils.reverse_lines_in_text(action_log))
        import_run.imported = result[0]
        import_run.uploaded_by = username
        import_run.save()
