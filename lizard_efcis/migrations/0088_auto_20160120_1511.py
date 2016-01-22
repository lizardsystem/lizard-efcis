# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_bio_fc_status(apps, schema_editor):
    Locatie = apps.get_model('lizard_efcis', 'Locatie')
    MeetStatus = apps.get_model('lizard_efcis', 'MeetStatus')
    BioStatus = apps.get_model('lizard_efcis', 'BioStatus')
    FCStatus = apps.get_model('lizard_efcis', 'FCStatus')
    locations = Locatie.objects.all()
    map_status = {
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=1),
        (FCStatus.objects.get(naam="BUITEN GEBRUIK"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=2),
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="BUITEN GEBRUIK")): MeetStatus.objects.get(index=3),
        (FCStatus.objects.get(naam="BUITEN GEBRUIK"), BioStatus.objects.get(naam="BUITEN GEBRUIK")): MeetStatus.objects.get(index=4),
        (None, BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=1),
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=1),
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=1),
    for location in locations:
        

class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0087_locatie_meet_status),
    ]

    operations = [
    ]
