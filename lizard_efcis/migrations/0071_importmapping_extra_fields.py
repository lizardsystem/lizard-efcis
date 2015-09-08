# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0070_auto_20150902_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='importmapping',
            name='extra_fields',
            field=models.TextField(help_text='Geef hier extra velden velddnaam=waarde, gebruik ENTER om velden te scheiden.', null=True, verbose_name='Extra export velden', blank=True),
            preserve_default=True,
        ),
    ]
