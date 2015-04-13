# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0023_auto_20150413_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opname',
            name='waarde_a',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
