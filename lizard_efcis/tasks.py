from __future__ import absolute_import

from datetime import datetime
from celery import shared_task

from lizard_efcis.import_data import DataImport
from lizard_efcis.models import ImportRun


def reverse_lines_in_text(text_with_lines):
    if text_with_lines is None:
        text_with_lines = ''
    lines = text_with_lines.split('\n')
    lines.reverse()
    return '\n'.join(lines)


def add_text_to_top(dest_text, text):
    """Add text on top, the dest_text contains lines"""
    if dest_text is None:
        dest_text = ''
    if text is None:
        text = ''
    lines = dest_text.split('\n')
    lines.insert(0, text)
    return '\n'.join(lines)


@shared_task
def add(x, y):
    return x + y


@shared_task
def validate(username, import_run=None, *args, **options):
    """Validate passed import_run or
    all active automatic import_runs"""
    import_runs = []
    data_import = DataImport()
    if import_run:
        import_runs.append(import_run)
    else:
        import_runs = list(ImportRun.objects.filter(
            **{'type_run': ImportRun.AUTO, 'actief': True}))
    for import_run in import_runs:
        result_as_text = '-------------------------------\n'
        result_as_text += "Start validatie, %s %s.\n" % (
            datetime.now().strftime('%Y-%m-%d %H:%M'),
            username)
        result = data_import.validate_csv(
            import_run.attachment.path,
            import_run.import_mapping.code)
        for code, message in result[1].iteritems():
            result_as_text += '%s: %s\n' % (code, message)
        result_as_text += "Gevalideerd: %s.\n" % result[0]
        result_as_text += 'Eind validatie, %s.\n' % (
            datetime.now().strftime('%Y-%m-%d %H:%M'))
        import_run.action_log = add_text_to_top(
            import_run.action_log,
            reverse_lines_in_text(result_as_text))
        import_run.validated = result[0]
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
        import_run.action_log = add_text_to_top(
            import_run.action_log,
            reverse_lines_in_text(action_log))
        import_run.imported = result[0]
        import_run.uploaded_by = username
        import_run.save()
