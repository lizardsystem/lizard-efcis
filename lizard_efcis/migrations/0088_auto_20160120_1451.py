# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def init_meet_status(apps, schema_editor):
    """Create meet statuses for hdsr-locations."""
    MeetStatus = apps.get_model('lizard_efcis', 'MeetStatus')
    MeetStatus(index=1, naam="FC-A BIO-A").save()
    MeetStatus(index=2, naam="FC-BG BIO-A").save()
    MeetStatus(index=3, naam="FC-A BIO-BG").save()
    MeetStatus(index=4, naam="FC-BG BIO-BG").save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0087_meetstatus'),
    ]

    operations = [
        migrations.RunPython(init_meet_status),
    ]


