# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0011_auto_20150303_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterGroep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=255)),
                ('parent', models.ForeignKey(to='lizard_efcis.ParameterGroep', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
