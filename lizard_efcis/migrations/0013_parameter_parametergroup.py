# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0012_parametergroep'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='parametergroup',
            field=models.ForeignKey(to='lizard_efcis.ParameterGroep', null=True),
            preserve_default=True,
        ),
    ]
