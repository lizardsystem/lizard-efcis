# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0002_auto_20150126_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opname',
            name='detect',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Detectiegrens', null=True),
            preserve_default=True,
        ),
    ]
