# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0056_auto_20150708_1015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importmapping',
            options={'ordering': ['tabel_naam', 'code'], 'verbose_name': 'importmapping', 'verbose_name_plural': 'importmappings'},
        ),
    ]
