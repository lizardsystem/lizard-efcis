# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0055_auto_20150707_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locatie',
            name='loc_oms',
            field=models.TextField(default='', verbose_name='omschrijving', blank=True),
            preserve_default=False,
        ),
    ]
