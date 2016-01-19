# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_bio_status_to_actief(apps, schema_editor):
    # Update empty and 'onbekend' values of bio_status field
    # in model Locatie to 'actief' status.
    Locatie = apps.get_model("lizard_efcis", "Locatie")
    BioStatus = apps.get_model("lizard_efcis", "BioStatus")
    bio_actief = BioStatus.objects.get(naam="ACTIEF")
    locations = Locatie.objects.exclude(
        bio_status__naam__in=["ACTIEF", "BUITEN GEBRUIK"])
    for locatie in locations:
        locatie.bio_status = bio_actief
        locatie.save()


def update_fc_status_to_actief(apps, schema_editor):
    # Update empty and 'onbekend' values of bio_status field
    # in model Locatie to 'actief' status.
    Locatie = apps.get_model("lizard_efcis", "Locatie")
    FCStatus = apps.get_model("lizard_efcis", "FCStatus")
    fc_actief = FCStatus.objects.get(naam="ACTIEF")
    locations = Locatie.objects.exclude(
        fc_status__naam__in=["ACTIEF", "BUITEN GEBRUIK"])
    for locatie in locations:
        locatie.fc_status = fc_actief
        locatie.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0083_parameter_par_oms_nl'),
    ]

    operations = [
        migrations.RunPython(update_bio_status_to_actief),
        migrations.RunPython(update_fc_status_to_actief),
    ]
