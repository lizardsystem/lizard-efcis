# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint

from django.db import models, migrations


def migrate_from_text_status_to_domain_table(apps, schema_editor):
    Waterlichaam = apps.get_model("lizard_efcis", "Waterlichaam")
    StatusKRW = apps.get_model("lizard_efcis", "StatusKRW")
    ids_and_codes = StatusKRW.objects.all().values('id', 'code')
    mapping = {item['code'].lower(): item['id']
               for item in ids_and_codes}
    pprint(mapping)

    for waterlichaam in Waterlichaam.objects.all():
        code = waterlichaam.status.lower()
        if code in mapping:
            waterlichaam.status_krw_id = mapping[code]
            print("Setting status of %s to StatusKRW(id=%s)" % (
                code, mapping[code]))
            waterlichaam.save()
        else:
            print("Status %r not found" % code)


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0039_waterlichaam_status_krw'),
    ]

    operations = [
        migrations.RunPython(migrate_from_text_status_to_domain_table),
    ]
