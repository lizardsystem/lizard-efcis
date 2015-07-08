# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0054_auto_20150706_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importrun',
            name='imported',
            field=models.BooleanField(default=False, verbose_name='ge\xefmporteerd'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importrun',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='gecontroleerd'),
            preserve_default=True,
        ),
    ]
