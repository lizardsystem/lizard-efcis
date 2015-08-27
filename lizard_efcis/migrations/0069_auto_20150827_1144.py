# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0068_ftplocation_import_mapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ftplocation',
            name='import_mapping',
            field=models.ForeignKey(to='lizard_efcis.ImportMapping', null=True),
            preserve_default=True,
        ),
    ]
