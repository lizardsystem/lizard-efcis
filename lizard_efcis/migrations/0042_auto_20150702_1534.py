# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0041_remove_waterlichaam_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuskrw',
            options={'ordering': ['code'], 'verbose_name': 'watertype status', 'verbose_name_plural': 'watertype statussen'},
        ),
        migrations.AlterField(
            model_name='waterlichaam',
            name='status_krw',
            field=models.ForeignKey(related_name='waterlichamen', verbose_name='status watertype', blank=True, to='lizard_efcis.StatusKRW', null=True),
            preserve_default=True,
        ),
    ]
