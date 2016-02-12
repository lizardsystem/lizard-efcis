# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0088_auto_20160120_1511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetstatus',
            options={'ordering': ['index'], 'verbose_name': 'Locatiestatus', 'verbose_name_plural': 'Locatiestatus'},
        ),
        migrations.RemoveField(
            model_name='locatie',
            name='bio_status',
        ),
        migrations.DeleteModel(
            name='BioStatus',
        ),
        migrations.RemoveField(
            model_name='locatie',
            name='fc_status',
        ),
        migrations.DeleteModel(
            name='FCStatus',
        ),
        migrations.AlterField(
            model_name='locatie',
            name='meet_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='locatiestatus', blank=True, to='lizard_efcis.MeetStatus', null=True),
            preserve_default=True,
        ),
    ]
