# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def remove_bio_status_onbekend(apps, schema_editor):
    BioStatus = apps.get_model("lizard_efcis", "BioStatus")
    BioStatus.objects.filter(naam="ONBEKEND").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0084_auto_20160119_1420'),
    ]

    operations = [
        migrations.RunPython(remove_bio_status_onbekend),
    ]
