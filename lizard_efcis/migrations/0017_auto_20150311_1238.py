# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0016_auto_20150310_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='x1',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='x2',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='y1',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='y2',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
