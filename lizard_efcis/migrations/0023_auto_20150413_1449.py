# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0022_auto_20150330_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importmapping',
            name='tabel_naam',
            field=models.CharField(help_text='Import tabel', max_length=255, choices=[('Opname', 'Opname'), ('Locatie', 'Locatie'), ('ParameterGroep', 'ParameterGroep'), ('Meetnet', 'Meetnet'), ('Activiteit', 'Activiteit')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mappingfield',
            name='db_datatype',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('float', 'float'), ('date', 'date'), ('time', 'time'), ('WNS', 'WNS'), ('Locatie', 'Locatie'), ('Detectiegrens', 'Detectiegrens'), ('ParameterGroep', 'ParameterGroep'), ('Meetnet', 'Meetnet'), ('StatusKRW', 'StatusKRW'), ('Waterlichaam', 'Waterlichaam'), ('Watertype', 'Watertype'), ('Activiteit', 'Activiteit')]),
            preserve_default=True,
        ),
    ]
