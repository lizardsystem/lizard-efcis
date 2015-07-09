# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0057_auto_20150709_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locatie',
            name='area',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
