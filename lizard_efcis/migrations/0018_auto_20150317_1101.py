# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0017_auto_20150311_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetnet',
            options={'ordering': ['code']},
        ),
        migrations.AddField(
            model_name='meetnet',
            name='code',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetnet',
            name='parent',
            field=models.ForeignKey(to='lizard_efcis.Meetnet', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='meetnet',
            unique_together=set([('code', 'parent')]),
        ),
        migrations.RemoveField(
            model_name='meetnet',
            name='net_oms',
        ),
    ]
