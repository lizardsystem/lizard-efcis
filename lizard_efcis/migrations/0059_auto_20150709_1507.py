# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0058_auto_20150709_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wns',
            options={'ordering': ['wns_code'], 'verbose_name': 'waarnemingssoort (WNS)', 'verbose_name_plural': 'waarnemingssoorten (WNS)'},
        ),
        migrations.AlterField(
            model_name='opname',
            name='validation_state',
            field=models.IntegerField(default=4, help_text="Alleen opnames met status 'Gevalideerd' zijn voor iedereen zichtbaar", verbose_name='validatiestatus', choices=[(1, b'Gevalideerd'), (2, b'Gevalideerd - niet tonen'), (3, b'Onbetrouwbaar'), (4, b'Niet gevalideerd')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wns',
            name='wns_code',
            field=models.CharField(unique=True, max_length=30, verbose_name='code WNS', db_index=True),
            preserve_default=True,
        ),
    ]
