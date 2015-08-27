# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0067_auto_20150827_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='ftplocation',
            name='import_mapping',
            field=models.ForeignKey(blank=True, to='lizard_efcis.ImportMapping', null=True),
            preserve_default=True,
        ),
    ]
