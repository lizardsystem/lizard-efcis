# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0057_auto_20150709_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importmapping',
            options={'ordering': ['tabel_naam', 'code'], 'verbose_name': 'mapping', 'verbose_name_plural': 'mappings'},
        ),
        migrations.AddField(
            model_name='importmapping',
            name='is_export',
            field=models.BooleanField(default=False, help_text='Mapping mag gebruikt worden voor Export.', verbose_name='Export'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='importmapping',
            name='is_import',
            field=models.BooleanField(default=False, help_text='Mapping mag gebruikt worden voor Import.', verbose_name='Import'),
            preserve_default=True,
        ),
    ]
