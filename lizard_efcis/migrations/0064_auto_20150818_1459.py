# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0063_ftplocation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ftplocation',
            options={'ordering': ['hostname'], 'verbose_name': 'FTP locatie voor automatische import', 'verbose_name_plural': 'FTP locaties vor automatische import'},
        ),
        migrations.RenameField(
            model_name='ftplocation',
            old_name='host',
            new_name='hostname',
        ),
    ]
