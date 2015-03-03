# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0009_auto_20150302_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterGroep',
            fields=[
                ('code', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('parent', models.ForeignKey(blank=True, to='lizard_efcis.ParameterGroep', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
