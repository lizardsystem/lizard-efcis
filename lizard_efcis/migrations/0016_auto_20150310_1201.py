# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0015_auto_20150304_1131'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parametergroep',
            options={'ordering': ['code']},
        ),
    ]
