# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0072_auto_20150908_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='wns',
            name='wns_oms_ecolims',
            field=models.CharField(verbose_name='omschrijving', max_length=255, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importmapping',
            name='extra_fields',
            field=models.TextField(help_text='Geef hier extra velden veldnaam=waarde, gebruik ENTER om velden te scheiden.', null=True, verbose_name='Extra export velden', blank=True),
            preserve_default=True,
        ),
    ]
