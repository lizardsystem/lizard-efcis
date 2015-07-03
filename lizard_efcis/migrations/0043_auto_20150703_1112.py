# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0042_auto_20150702_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='WNSStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naam', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['naam'],
                'verbose_name': 'WNS status',
                'verbose_name_plural': 'WNS statussen',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['naam'], 'verbose_name': 'TWN status', 'verbose_name_plural': 'TWN statussen'},
        ),
        migrations.AddField(
            model_name='wns',
            name='wns_status',
            field=models.ForeignKey(verbose_name='WNS status', blank=True, to='lizard_efcis.WNSStatus', null=True),
            preserve_default=True,
        ),
    ]
