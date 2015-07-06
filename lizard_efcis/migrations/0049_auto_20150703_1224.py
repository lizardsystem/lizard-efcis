# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0048_auto_20150703_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locatie',
            name='status_bio',
        ),
        migrations.RemoveField(
            model_name='locatie',
            name='status_fc',
        ),
    ]
