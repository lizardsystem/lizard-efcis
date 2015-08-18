# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0064_auto_20150818_1459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ftplocation',
            options={'ordering': ['hostname'], 'verbose_name': 'FTP locatie voor automatische import', 'verbose_name_plural': 'FTP locaties voor automatische import'},
        ),
        migrations.AddField(
            model_name='ftplocation',
            name='directory',
            field=models.CharField(help_text='Base directory (TEST or PROD, currently)', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
