# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0091_auto_20160315_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetstatus',
            name='omschrijving',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
