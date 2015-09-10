# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0073_auto_20150909_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='opname',
            name='opmerkingen',
            field=models.TextField(null=True, verbose_name='Opmerkingen', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opname',
            name='vis_cm',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opname',
            name='vis_kg',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opname',
            name='vis_opp_ha',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
