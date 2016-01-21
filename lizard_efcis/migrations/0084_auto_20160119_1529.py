# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def remove_bio_status_onbekend(apps, schema_editor):
    BioStatus = apps.get_model("lizard_efcis", "BioStatus")
    BioStatus.objects.filter(naam="ONBEKEND").delete()


def create_niet_bemeten_status(apps, schema_editor):
    BioStatus = apps.get_model("lizard_efcis", "BioStatus")
    FCStatus = apps.get_model("lizard_efcis", "FCStatus")
    try:
        BioStatus(naam="NIET BEMETEN").save()
    except Exception as ex:
        print(ex.message)
    try:
        FCStatus(naam="NIET BEMETEN").save()
    except Exception as ex:
        print(ex.message)

        
class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0083_parameter_par_oms_nl'),
    ]

    operations = [
        migrations.RunPython(remove_bio_status_onbekend),
        migrations.RunPython(create_niet_bemeten_status),
    ]
