# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0007_auto_20150223_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='importmapping',
            name='scheiding_teken',
            field=models.CharField(default=';', help_text='Veld scheidingsteken.', max_length=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mappingfield',
            name='db_datatype',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('float', 'float'), ('date', 'date'), ('time', 'time'), ('WNS', 'WNS'), ('Locatie', 'Locatie'), ('Detectiegrens', 'Detectiegrens')]),
            preserve_default=True,
        ),
    ]
