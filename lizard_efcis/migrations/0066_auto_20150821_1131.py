# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0065_auto_20150818_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappingfield',
            name='db_datatype',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('float', 'float'), ('date', 'date'), ('time', 'time'), ('Activiteit', 'Activiteit'), ('BioStatus', 'BioStatus'), ('Detectiegrens', 'Detectiegrens'), ('FCStatus', 'FCStatus'), ('Locatie', 'Locatie'), ('Meetnet', 'Meetnet'), ('ParameterGroep', 'ParameterGroep'), ('StatusKRW', 'StatusKRW'), ('Waterlichaam', 'Waterlichaam'), ('Watertype', 'Watertype'), ('WNS', 'WNS')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetnet',
            name='parent',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Meetnet', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parameter',
            name='parametergroep',
            field=models.ForeignKey(blank=True, to='lizard_efcis.ParameterGroep', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parametergroep',
            name='parent',
            field=models.ForeignKey(blank=True, to='lizard_efcis.ParameterGroep', null=True),
            preserve_default=True,
        ),
    ]
