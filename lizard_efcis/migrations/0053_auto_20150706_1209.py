# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0052_opname_validation_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='afvoergebied',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='grondsoort',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='landgebruik',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='act_oms',
            field=models.TextField(null=True, verbose_name='omschrijving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='act_type',
            field=models.CharField(default='Meting', max_length=10, verbose_name='type activiteit', choices=[('', ''), ('Meting', 'Meting'), ('Toetsing', 'Toetsing')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_fc',
            field=models.TextField(null=True, verbose_name='methode fysisch-chemisch', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_fyt',
            field=models.TextField(null=True, verbose_name='methode fytoplankton', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_mafa',
            field=models.TextField(null=True, verbose_name='methode macrofauna', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_mafy',
            field=models.TextField(null=True, verbose_name='methode macrofyten', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_toets',
            field=models.TextField(null=True, verbose_name='methode toetsing', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_vis',
            field=models.TextField(null=True, verbose_name='methode vissen', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='compartiment',
            name='comp_oms',
            field=models.TextField(null=True, verbose_name='omschrijving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eenheid',
            name='eenheid_oms',
            field=models.TextField(null=True, verbose_name='omschrijving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hoedanigheid',
            name='hoed_oms',
            field=models.TextField(null=True, verbose_name='omschriving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='loc_id',
            field=models.CharField(unique=True, max_length=50, verbose_name='code locatie'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='loc_oms',
            field=models.TextField(null=True, verbose_name='omschrijving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parameter',
            name='casnummer',
            field=models.CharField(max_length=30, null=True, verbose_name='CAS-nummer', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parameter',
            name='par_code',
            field=models.CharField(max_length=30, verbose_name='code'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parameter',
            name='par_oms',
            field=models.CharField(max_length=255, null=True, verbose_name='omschrijving', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parametergroep',
            name='code',
            field=models.CharField(unique=True, max_length=255, verbose_name='parametergroepnaam'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statuskrw',
            name='code',
            field=models.CharField(unique=True, max_length=50, verbose_name='status watertype'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waterlichaam',
            name='wl_code',
            field=models.CharField(max_length=20, verbose_name='code'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waterlichaam',
            name='wl_naam',
            field=models.CharField(max_length=255, null=True, verbose_name='naam', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='waterlichaam',
            name='wl_type',
            field=models.CharField(max_length=10, null=True, verbose_name='type', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wns',
            name='wns_code',
            field=models.CharField(unique=True, max_length=30, verbose_name='code WNS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wns',
            name='wns_oms',
            field=models.CharField(verbose_name='omschrijving', max_length=255, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
