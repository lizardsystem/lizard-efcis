# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0089_auto_20160212_1018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetstatus',
            options={'ordering': ['index'], 'verbose_name': 'locatiestatus', 'verbose_name_plural': 'locatiestatus'},
        ),
        migrations.AlterField(
            model_name='locatie',
            name='meet_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='locatiestatus', to='lizard_efcis.MeetStatus'),
            preserve_default=True,
        ),
    ]
