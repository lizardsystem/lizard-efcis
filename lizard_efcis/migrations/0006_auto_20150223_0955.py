# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0005_importmapping_mappingfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='importmapping',
            name='code',
            field=models.CharField(default=datetime.datetime(2015, 2, 23, 9, 55, 33, 642687), unique=True, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mappingfield',
            name='foreignkey_field',
            field=models.CharField(help_text='Veldnaam van de Foreign tabel, meestal id of code. Wordt gebruik in combinatie met foreign_key,', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
