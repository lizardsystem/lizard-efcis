# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0040_auto_20150702_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterlichaam',
            name='status',
        ),
    ]
