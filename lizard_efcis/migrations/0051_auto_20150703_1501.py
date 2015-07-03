# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_wns_oms(apps, schema_editor):
    # Re-save all WNS objects so that the wns_oms is generated anew.
    WNS = apps.get_model("lizard_efcis", "WNS")
    for wns in WNS.objects.all():
        wns.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0050_auto_20150703_1459'),
    ]

    operations = [
        migrations.RunPython(fix_wns_oms),
    ]
