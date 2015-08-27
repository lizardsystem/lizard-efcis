# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0066_auto_20150821_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importmapping',
            name='tabel_naam',
            field=models.CharField(max_length=255, verbose_name='Import tabel', choices=[('Activiteit', 'Activiteit'), ('Locatie', 'Locatie'), ('Meetnet', 'Meetnet'), ('Parameter', 'Parameter'), ('ParameterGroep', 'ParameterGroep'), ('Opname', 'Opname'), ('WNS', 'WNS')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mappingfield',
            name='db_datatype',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('float', 'float'), ('date', 'date'), ('time', 'time'), ('Activiteit', 'Activiteit'), ('BioStatus', 'BioStatus'), ('Detectiegrens', 'Detectiegrens'), ('FCStatus', 'FCStatus'), ('Locatie', 'Locatie'), ('Meetnet', 'Meetnet'), ('ParameterGroep', 'ParameterGroep'), ('Status', 'Status'), ('StatusKRW', 'StatusKRW'), ('Waterlichaam', 'Waterlichaam'), ('Watertype', 'Watertype'), ('WNS', 'WNS')]),
            preserve_default=True,
        ),
    ]
