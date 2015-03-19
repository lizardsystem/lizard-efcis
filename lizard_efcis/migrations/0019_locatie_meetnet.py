# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0018_auto_20150318_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='meetnet',
            field=models.ManyToManyField(to='lizard_efcis.Meetnet', null=True, blank=True),
            preserve_default=True,
        ),
    ]
