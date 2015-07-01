# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0030_auto_20150615_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='importrun',
            name='actief',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
