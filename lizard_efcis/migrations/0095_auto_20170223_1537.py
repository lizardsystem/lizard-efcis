# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0094_locatie_krw_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locatie',
            name='krw_color',
            field=models.IntegerField(help_text='Kleur voor KRW op kaart. Keuze = 1, 2, 3.', null=True, verbose_name='krw_color', blank=True),
            preserve_default=True,
        ),
    ]
