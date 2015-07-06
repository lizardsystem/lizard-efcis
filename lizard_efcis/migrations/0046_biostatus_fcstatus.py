# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0045_remove_wns_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='BioStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naam', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name': 'biologische status',
                'verbose_name_plural': 'biologische statussen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FCStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naam', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name': 'fysisch/chemische status',
                'verbose_name_plural': 'fysisch/chemische statussen',
            },
            bases=(models.Model,),
        ),
    ]
