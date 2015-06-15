# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0029_auto_20150612_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='importrun',
            name='activiteit',
            field=models.ForeignKey(blank=True, to='lizard_efcis.Activiteit', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importrun',
            name='type_run',
            field=models.CharField(default='Handmatig', max_length=20, choices=[('Automatisch', 'Automatisch'), ('Handmatig', 'Handmatig')]),
            preserve_default=True,
        ),
    ]
