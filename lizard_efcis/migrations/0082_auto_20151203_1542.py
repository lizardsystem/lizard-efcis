# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0081_auto_20151203_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappingfield',
            name='ordering',
            field=models.IntegerField(default=1000, help_text='Veldvolgorde bij export, een getaal.', verbose_name='Ordering'),
            preserve_default=True,
        ),
    ]
