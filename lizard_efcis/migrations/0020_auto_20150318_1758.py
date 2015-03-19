# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0019_locatie_meetnet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuskrw',
            name='code',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
    ]
