# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0061_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='wns',
            name='validate_max',
            field=models.FloatField(help_text='Kan gebruikt worden voor validatie van opnames', null=True, verbose_name='maximum valide waarde', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wns',
            name='validate_min',
            field=models.FloatField(help_text='Kan gebruikt worden voor validatie van opnames', null=True, verbose_name='minimum valide waarde', blank=True),
            preserve_default=True,
        ),
    ]
