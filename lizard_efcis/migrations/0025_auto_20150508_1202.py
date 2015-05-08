# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0024_auto_20150413_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opname',
            name='datum',
            field=models.DateField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opname',
            name='tijd',
            field=models.TimeField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opname',
            name='waarde_a',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opname',
            name='waarde_n',
            field=models.FloatField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
