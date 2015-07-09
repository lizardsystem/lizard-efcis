# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0056_auto_20150708_1015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importmapping',
            options={'ordering': ['tabel_naam', 'code'], 'verbose_name': 'importmapping', 'verbose_name_plural': 'importmappings'},
        ),
        migrations.AddField(
            model_name='locatie',
            name='area',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
