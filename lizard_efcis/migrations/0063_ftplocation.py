# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0062_auto_20150710_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='FTPLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['host'],
                'verbose_name': 'FTP locatie voor automatische import',
                'verbose_name_plural': 'FTP locaties vor automatische import',
            },
            bases=(models.Model,),
        ),
    ]
