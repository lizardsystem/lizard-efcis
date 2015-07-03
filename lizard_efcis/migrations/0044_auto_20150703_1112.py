# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_wns_status(apps, schema_editor):
    WNSStatus = apps.get_model("lizard_efcis", "WNSStatus")
    WNS = apps.get_model("lizard_efcis", "WNS")
    current_status_values = WNS.objects.all().values_list(
        'status__naam', flat=True)
    wns_status_per_name = {}
    for status_name in set(current_status_values):
        if status_name is None:
            continue
        wns_status, created = WNSStatus.objects.get_or_create(
            naam=status_name)
        wns_status_per_name[status_name] = wns_status
        print("Created new WNS status %r" % status_name)

    for wns in WNS.objects.all():
        if not wns.status:
            continue
        wns.wns_status = wns_status_per_name[wns.status.naam]
        wns.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0043_auto_20150703_1112'),
    ]

    operations = [
        migrations.RunPython(migrate_wns_status),
    ]
