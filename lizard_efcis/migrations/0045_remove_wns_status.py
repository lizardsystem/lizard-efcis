# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0044_auto_20150703_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wns',
            name='status',
        ),
    ]
