# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0037_activiteit_uitvoerende'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuskrw',
            options={'ordering': ['code'], 'verbose_name': 'KRW watertype status', 'verbose_name_plural': 'KRW watertype statussen'},
        ),
        migrations.AlterField(
            model_name='importmapping',
            name='scheiding_teken',
            field=models.CharField(default=';', max_length=3, verbose_name='Veld scheidingsteken.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importmapping',
            name='tabel_naam',
            field=models.CharField(max_length=255, verbose_name='Import tabel', choices=[('Opname', 'Opname'), ('Locatie', 'Locatie'), ('ParameterGroep', 'ParameterGroep'), ('Meetnet', 'Meetnet'), ('Activiteit', 'Activiteit'), ('WNS', 'WNS')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='geo_punt1',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='geo_punt2',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='loc_id',
            field=models.CharField(unique=True, max_length=50, verbose_name='locatiecode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='loc_oms',
            field=models.TextField(null=True, verbose_name='locatieomschrijving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='status_krw',
            field=models.ForeignKey(related_name='locaties', verbose_name='status watertype', blank=True, to='lizard_efcis.StatusKRW', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='watertype',
            field=models.ForeignKey(verbose_name='KRW watertype', blank=True, to='lizard_efcis.Watertype', null=True),
            preserve_default=True,
        ),
    ]
