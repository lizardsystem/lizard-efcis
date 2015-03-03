# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0008_auto_20150225_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opname',
            name='tijd',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
