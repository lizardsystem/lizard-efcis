# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0088_auto_20160120_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='locatie',
            name='meet_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='biologische fysisch/chemische status', blank=True, to='lizard_efcis.MeetStatus', null=True),
            preserve_default=True,
        ),
    ]
