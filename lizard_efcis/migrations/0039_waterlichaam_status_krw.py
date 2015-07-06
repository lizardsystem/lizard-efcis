# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0038_auto_20150702_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterlichaam',
            name='status_krw',
            field=models.ForeignKey(related_name='waterlichamen', verbose_name='status', blank=True, to='lizard_efcis.StatusKRW', null=True),
            preserve_default=True,
        ),
    ]
