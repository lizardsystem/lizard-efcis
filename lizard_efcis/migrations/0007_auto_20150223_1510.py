# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0006_auto_20150223_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opname',
            name='moment',
        ),
        migrations.AddField(
            model_name='mappingfield',
            name='data_format',
            field=models.CharField(help_text='b.v. %d-%m-%Y voor de datum.', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='opname',
            name='datum',
            field=models.DateField(default=datetime.datetime(2015, 2, 23, 15, 10, 8, 214669)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opname',
            name='tijd',
            field=models.TimeField(default=datetime.datetime(2015, 2, 23, 15, 10, 19, 990441)),
            preserve_default=False,
        ),
    ]
