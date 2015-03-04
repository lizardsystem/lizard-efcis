# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0013_parameter_parametergroup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parameter',
            old_name='parametergroup',
            new_name='parametergroep',
        ),
    ]
