# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0059_auto_20150709_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='is_krw_area',
            field=models.BooleanField(default=False, verbose_name='is KRW gebied', editable=False),
            preserve_default=True,
        ),
    ]
