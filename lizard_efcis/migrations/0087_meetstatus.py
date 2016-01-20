# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0086_auto_20160119_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(unique=True)),
                ('naam', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name': 'biologisch/fysisch/chemische  status',
                'verbose_name_plural': 'biologisch/fysisch/chemische statussen',
            },
            bases=(models.Model,),
        ),
    ]
