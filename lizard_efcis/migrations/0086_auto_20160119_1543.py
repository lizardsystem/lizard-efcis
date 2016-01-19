# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0085_auto_20160119_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locatie',
            name='bio_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='biologische status', to='lizard_efcis.BioStatus'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='locatie',
            name='fc_status',
            field=models.ForeignKey(related_name='locaties', verbose_name='fysisch/chemische status', to='lizard_efcis.FCStatus'),
            preserve_default=False,
        ),
    ]
