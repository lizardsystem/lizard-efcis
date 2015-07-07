# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0036_auto_20150702_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='activiteit',
            name='uitvoerende',
            field=models.ForeignKey(related_name='activiteiten', blank=True, to='lizard_efcis.Uitvoerende', null=True),
            preserve_default=True,
        ),
    ]
