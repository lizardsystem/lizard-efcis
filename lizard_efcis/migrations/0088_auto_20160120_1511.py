# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_none_to_bg(apps, schema_editor):
    """
    Set NONE values in fc_status and bio_status
    to NIET BEMETEN.
    """
    Locatie = apps.get_model('lizard_efcis', 'Locatie')
    BioStatus = apps.get_model('lizard_efcis', 'BioStatus')
    FCStatus = apps.get_model('lizard_efcis', 'FCStatus')
    bio_nb = BioStatus.objects.get(naam="NIET BEMETEN")
    fc_nb = FCStatus.objects.get(naam="NIET BEMETEN")
    locations = Locatie.objects.all()
    for location in locations:
        if location.fc_status in [None, '']:
            location.fc_status = fc_nb
            location.save()
        if location.bio_status in [None, '']:
            location.bio_status = bio_nb
            location.save()


def migrate_bio_fc_status(apps, schema_editor):
    Locatie = apps.get_model('lizard_efcis', 'Locatie')
    MeetStatus = apps.get_model('lizard_efcis', 'MeetStatus')
    BioStatus = apps.get_model('lizard_efcis', 'BioStatus')
    FCStatus = apps.get_model('lizard_efcis', 'FCStatus')
    locations = Locatie.objects.all()
    map_status = {
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=1),
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="BUITEN GEBRUIK")): MeetStatus.objects.get(index=2),
        (FCStatus.objects.get(naam="ACTIEF"), BioStatus.objects.get(naam="NIET BEMETEN")): MeetStatus.objects.get(index=3),
        (FCStatus.objects.get(naam="BUITEN GEBRUIK"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=4),
        (FCStatus.objects.get(naam="NIET BEMETEN"), BioStatus.objects.get(naam="ACTIEF")): MeetStatus.objects.get(index=5),
        (FCStatus.objects.get(naam="BUITEN GEBRUIK"), BioStatus.objects.get(naam="BUITEN GEBRUIK")): MeetStatus.objects.get(index=6),
        (FCStatus.objects.get(naam="NIET BEMETEN"), BioStatus.objects.get(naam="BUITEN GEBRUIK")): MeetStatus.objects.get(index=7),
        (FCStatus.objects.get(naam="BUITEN GEBRUIK"), BioStatus.objects.get(naam="NIET BEMETEN")): MeetStatus.objects.get(index=8)
    }
    for location in locations:
        location.meet_status = map_status[(location.fc_status, location.bio_status)]
        location.save()
        

class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0087_locatie_meet_status'),
    ]

    operations = [
        migrations.RunPython(set_none_to_bg),
        migrations.RunPython(migrate_bio_fc_status)
    ]
