# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import lizard_efcis.models


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0026_auto_20150522_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('type_run', models.CharField(max_length=20, choices=[('Automatisch', 'Automatisch'), ('Handmatig', 'Handmatig')])),
                ('attachment', models.FileField(null=True, upload_to=lizard_efcis.models.get_attachment_path, blank=True)),
                ('uploaded_by', models.CharField(max_length=200, blank=True)),
                ('uploaded_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
