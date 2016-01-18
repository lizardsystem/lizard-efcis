# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0082_auto_20151203_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='par_oms_nl',
            field=models.CharField(max_length=255, null=True, verbose_name='NL-omschrijving', blank=True),
            preserve_default=True,
        ),
    ]
