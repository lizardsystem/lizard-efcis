# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0035_auto_20150702_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uitvoerende',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'uitvoerende',
                'verbose_name_plural': 'uitvoerenden',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='activiteit',
            name='uitvoerende',
        ),
    ]
