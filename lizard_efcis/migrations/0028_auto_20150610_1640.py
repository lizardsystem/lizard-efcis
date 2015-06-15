# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0027_importrun'),
    ]

    operations = [
        migrations.AddField(
            model_name='importrun',
            name='import_mapping',
            field=models.ForeignKey(blank=True, to='lizard_efcis.ImportMapping', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importrun',
            name='attachment',
            field=models.FileField(null=True, upload_to=b'manual_import', blank=True),
            preserve_default=True,
        ),
    ]
