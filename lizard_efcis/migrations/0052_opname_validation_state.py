# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0051_auto_20150703_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='opname',
            name='validation_state',
            field=models.IntegerField(default=4, help_text="(TODO) Alleen opnames met status 'Gevalideerd' zijn voor iedereen zichtbaar", verbose_name='validatiestatus', choices=[(1, 'Gevalideerd'), (2, 'Gevalideerd - niet tonen'), (3, 'Onbetrouwbaar'), (4, 'Niet gevalideerd')]),
            preserve_default=True,
        ),
    ]
