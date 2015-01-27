# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activiteit',
            name='activiteit',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='loc_id',
            field=models.CharField(help_text='Locatiecode', unique=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wns',
            name='wns_code',
            field=models.CharField(unique=True, max_length=30),
            preserve_default=True,
        ),
    ]
