# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0090_auto_20160222_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappingfield',
            name='db_datatype',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('TextField', 'TextField'), ('float', 'float'), ('date', 'date'), ('time', 'time'), ('boolean', 'boolean'), ('Activiteit', 'Activiteit'), ('BioStatus', 'BioStatus'), ('Compartiment', 'Compartiment'), ('Detectiegrens', 'Detectiegrens'), ('Eenheid', 'Eenheid'), ('FCStatus', 'FCStatus'), ('Hoedanigheid', 'Hoedanigheid'), ('Locatie', 'Locatie'), ('Meetnet', 'Meetnet'), ('MeetStatus', 'MeetStatus'), ('Parameter', 'Parameter'), ('ParameterGroep', 'ParameterGroep'), ('Status', 'Status'), ('StatusKRW', 'StatusKRW'), ('WNS', 'WNS'), ('WNSStatus', 'WNSStatus'), ('Waterlichaam', 'Waterlichaam'), ('Watertype', 'Watertype')]),
            preserve_default=True,
        ),
    ]
