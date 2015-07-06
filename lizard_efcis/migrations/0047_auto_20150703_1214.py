# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0046_biostatus_fcstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='bio_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='biologische status', blank=True, to='lizard_efcis.BioStatus', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locatie',
            name='fc_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='fysisch/chemische status', blank=True, to='lizard_efcis.FCStatus', null=True),
            preserve_default=True,
        ),
    ]
