# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activiteit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activiteit', models.CharField(max_length=50)),
                ('act_type', models.CharField(default='Meting', max_length=10, choices=[('', ''), ('Meting', 'Meting'), ('Toetsing', 'Toetsing')])),
                ('uitvoerende', models.CharField(max_length=50, null=True, blank=True)),
                ('act_oms', models.TextField(null=True, blank=True)),
                ('met_mafa', models.CharField(max_length=255, null=True, blank=True)),
                ('met_mafy', models.CharField(max_length=255, null=True, blank=True)),
                ('met_fyt', models.CharField(max_length=255, null=True, blank=True)),
                ('met_vis', models.CharField(max_length=255, null=True, blank=True)),
                ('met_fc', models.CharField(max_length=255, null=True, blank=True)),
                ('met_toets', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Compartiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('compartiment', models.CharField(unique=True, max_length=20)),
                ('comp_oms', models.TextField(null=True, blank=True)),
                ('compartimentgroep', models.CharField(max_length=30, null=True, blank=True)),
                ('datum_status', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Detectiegrens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teken', models.CharField(unique=True, max_length=5)),
                ('omschrijving', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Eenheid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eenheid', models.CharField(unique=True, max_length=20)),
                ('eenheid_oms', models.TextField(null=True, blank=True)),
                ('dimensie', models.CharField(max_length=20, null=True, blank=True)),
                ('omrekenfactor', models.FloatField(null=True, blank=True)),
                ('eenheidgroep', models.CharField(max_length=50, null=True, blank=True)),
                ('datum_status', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hoedanigheid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hoedanigheid', models.CharField(unique=True, max_length=20)),
                ('hoed_oms', models.TextField(null=True, blank=True)),
                ('hoedanigheidgroep', models.CharField(max_length=30, null=True, blank=True)),
                ('datum_status', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locatie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('loc_id', models.CharField(help_text='Locatiecode', max_length=50)),
                ('loc_oms', models.TextField(help_text='Locatieomschrijving', null=True, blank=True)),
                ('geo_punt1', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('geo_punt2', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meetnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('net_oms', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Opname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moment', models.DateTimeField()),
                ('waarde_n', models.FloatField(null=True, blank=True)),
                ('waarde_a', models.FloatField(null=True, blank=True)),
                ('activiteit', models.ForeignKey(to='lizard_efcis.Activiteit')),
                ('detect', models.ForeignKey(to='lizard_efcis.Detectiegrens')),
                ('locatie', models.ForeignKey(to='lizard_efcis.Locatie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('par_code', models.CharField(max_length=30)),
                ('par_oms', models.CharField(max_length=255, null=True, blank=True)),
                ('casnummer', models.CharField(max_length=30, null=True, blank=True)),
                ('datum_status', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ['par_code'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naam', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusKRW',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=5)),
                ('omschrijving', models.TextField(null=True, blank=True)),
                ('datum_begin', models.DateField(null=True, blank=True)),
                ('datum_eind', models.DateField(null=True, blank=True)),
                ('datum_status', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Waterlichaam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wl_code', models.CharField(max_length=20)),
                ('wl_naam', models.CharField(max_length=255, null=True, blank=True)),
                ('wl_type', models.CharField(max_length=10, null=True, blank=True)),
                ('wl_oms', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watertype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=5)),
                ('omschrijving', models.TextField(null=True, blank=True)),
                ('groep', models.CharField(max_length=10, choices=[('zout', 'zout'), ('zoet', 'zoet')])),
                ('datum_begin', models.DateField(null=True, blank=True)),
                ('datum_eind', models.DateField(null=True, blank=True)),
                ('datum_status', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WNS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wns_code', models.CharField(max_length=30)),
                ('wns_oms', models.CharField(max_length=255, null=True, blank=True)),
                ('datum_status', models.DateField(null=True, blank=True)),
                ('compartiment', models.ForeignKey(blank=True, to='lizard_efcis.Compartiment', null=True)),
                ('eenheid', models.ForeignKey(blank=True, to='lizard_efcis.Eenheid', null=True)),
                ('hoedanigheid', models.ForeignKey(blank=True, to='lizard_efcis.Hoedanigheid', null=True)),
                ('parameter', models.ForeignKey(blank=True, to='lizard_efcis.Parameter', null=True)),
                ('status', models.ForeignKey(blank=True, to='lizard_efcis.Status', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='parameter',
            name='status',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Status', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opname',
            name='wns',
            field=models.ForeignKey(to='lizard_efcis.WNS'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='meetnet',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Meetnet', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='status_krw',
            field=models.ForeignKey(blank=True, to='lizard_efcis.StatusKRW', help_text='Status KRW Watertype', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='waterlichaam',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Waterlichaam', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='watertype',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Watertype', help_text='KRW Watertype', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hoedanigheid',
            name='status',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Status', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eenheid',
            name='status',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Status', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='compartiment',
            name='status',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Status', null=True),
            preserve_default=True,
        ),
    ]
