# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0025_auto_20150508_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opname',
            options={'ordering': ['wns_id', 'locatie_id', 'datum', 'tijd'], 'verbose_name': 'opname', 'verbose_name_plural': 'opnames'},
        ),
        migrations.AlterField(
            model_name='opname',
            name='activiteit',
            field=models.ForeignKey(related_name='opnames', to='lizard_efcis.Activiteit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opname',
            name='locatie',
            field=models.ForeignKey(related_name='opnames', to='lizard_efcis.Locatie'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='opname',
            name='wns',
            field=models.ForeignKey(related_name='opnames', to='lizard_efcis.WNS'),
            preserve_default=True,
        ),
    ]
