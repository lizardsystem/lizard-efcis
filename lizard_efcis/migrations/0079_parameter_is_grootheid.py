# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0078_auto_20150914_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='is_grootheid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
