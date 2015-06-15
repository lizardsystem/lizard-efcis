# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0028_auto_20150610_1640'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['naam'], 'verbose_name': 'status', 'verbose_name_plural': 'statussen'},
        ),
        migrations.AddField(
            model_name='importrun',
            name='action_log',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='importrun',
            name='imported',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='importrun',
            name='validated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
