# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0071_importmapping_extra_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locatie',
            name='meetnet',
            field=models.ManyToManyField(related_name='locaties', null=True, to='lizard_efcis.Meetnet', blank=True),
            preserve_default=True,
        ),
    ]
