# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0080_auto_20150930_1013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mappingfield',
            options={'ordering': ['ordering', 'db_field'], 'verbose_name': 'mappingveld', 'verbose_name_plural': 'mappingvelden'},
        ),
        migrations.AddField(
            model_name='mappingfield',
            name='ordering',
            field=models.IntegerField(default=0, help_text='Veldvolgorde bij export, een getaal.', verbose_name='Ordering'),
            preserve_default=True,
        ),
    ]
