# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0017_auto_20150311_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetnet',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='locatie',
            name='meetnet',
        ),
        migrations.AddField(
            model_name='locatie',
            name='status_bio',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='status_fc',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetnet',
            name='code',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetnet',
            name='parent',
            field=models.ForeignKey(to='lizard_efcis.Meetnet', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importmapping',
            name='tabel_naam',
            field=models.CharField(help_text='Import tabel', max_length=255, choices=[('Opname', 'Opname'), ('Locatie', 'Locatie'), ('ParameterGroep', 'ParameterGroep'), ('Meetnet', 'Meetnet')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mappingfield',
            name='db_datatype',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie', choices=[('CharField', 'CharField'), ('float', 'float'), ('date', 'date'), ('time', 'time'), ('WNS', 'WNS'), ('Locatie', 'Locatie'), ('Detectiegrens', 'Detectiegrens'), ('ParameterGroep', 'ParameterGroep'), ('Meetnet', 'Meetnet')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='meetnet',
            unique_together=set([('code', 'parent')]),
        ),
        migrations.RemoveField(
            model_name='meetnet',
            name='net_oms',
        ),
    ]
