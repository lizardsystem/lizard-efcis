# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0049_auto_20150703_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wns',
            name='wns_oms_space_less',
        ),
        migrations.AlterField(
            model_name='wns',
            name='wns_oms',
            field=models.CharField(max_length=255, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
