# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0074_auto_20150910_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='opname',
            name='waarde_krw',
            field=models.FloatField(help_text='Automatisch gegenereerd voor de KRW kleuring', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
