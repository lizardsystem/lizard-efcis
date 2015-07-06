# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0034_auto_20150630_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activiteit',
            name='met_fc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_fyt',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_mafa',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_mafy',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_toets',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activiteit',
            name='met_vis',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
