# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0031_importrun_actief'),
    ]

    operations = [
        migrations.AddField(
            model_name='wns',
            name='wns_oms_space_less',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
