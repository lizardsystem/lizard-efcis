# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0033_auto_20150630_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opname',
            name='import_run',
            field=models.ForeignKey(related_name='opnames', blank=True, to='lizard_efcis.ImportRun', null=True),
            preserve_default=True,
        ),
    ]
