# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0093_auto_20161108_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='krw_color',
            field=models.IntegerField(help_text='Kleur voor KRW op kaart.', null=True, verbose_name='krw_color', blank=True),
            preserve_default=True,
        ),
    ]
