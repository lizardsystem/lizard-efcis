# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_status(apps, schema_editor):
    FCStatus = apps.get_model("lizard_efcis", "FCStatus")
    BioStatus = apps.get_model("lizard_efcis", "BioStatus")
    Locatie = apps.get_model("lizard_efcis", "Locatie")

    for locatie in Locatie.objects.all():
        if locatie.status_fc:
            fc_status, created = FCStatus.objects.get_or_create(
                naam=locatie.status_fc)
            if created:
                print("Created fc status %s" % fc_status.naam)
            locatie.fc_status = fc_status
        if locatie.status_bio:
            bio_status, created = BioStatus.objects.get_or_create(
                naam=locatie.status_bio)
            if created:
                print("Created bio status %s" % bio_status.naam)
            locatie.bio_status = bio_status
        locatie.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0047_auto_20150703_1214'),
    ]

    operations = [
        migrations.RunPython(migrate_status),
    ]
