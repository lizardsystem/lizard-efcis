# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0003_auto_20150209_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opname',
            name='waarde_a',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
    ]
