# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0004_auto_20150217_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('omschrijving', models.TextField(null=True, blank=True)),
                ('tabel_naam', models.CharField(help_text='Import tabel', max_length=255, choices=[('Opname', 'Opname'), ('Locatie', 'Locatie')])),
            ],
            options={
                'ordering': ['tabel_naam'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MappingField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('db_field', models.CharField(max_length=255)),
                ('file_field', models.CharField(max_length=255)),
                ('db_datatype', models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('float', 'float'), ('WNS', 'WNS'), ('Activiteit', 'Activiteit'), ('Locatie', 'Locatie'), ('Detectiegrens', 'Detectiegrens')])),
                ('foreignkey_field', models.CharField(help_text='Wordt gebruik in combinatie met foreign_key, Veldnaam van de Foreign tabel, meestal id of code.', max_length=255, null=True, blank=True)),
                ('mapping', models.ForeignKey(to='lizard_efcis.ImportMapping')),
            ],
            options={
                'ordering': ['db_field'],
            },
            bases=(models.Model,),
        ),
    ]
