# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0021_auto_20150319_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activiteit',
            options={'ordering': ['activiteit'], 'verbose_name': 'activiteit', 'verbose_name_plural': 'activiteit'},
        ),
        migrations.AlterModelOptions(
            name='compartiment',
            options={'ordering': ['compartiment'], 'verbose_name': 'compartiment', 'verbose_name_plural': 'compartimenten'},
        ),
        migrations.AlterModelOptions(
            name='detectiegrens',
            options={'verbose_name': 'detectiegrens', 'verbose_name_plural': 'detectiegrenzen'},
        ),
        migrations.AlterModelOptions(
            name='eenheid',
            options={'ordering': ['eenheid'], 'verbose_name': 'eenheid', 'verbose_name_plural': 'eenheden'},
        ),
        migrations.AlterModelOptions(
            name='hoedanigheid',
            options={'ordering': ['hoedanigheid'], 'verbose_name': 'hoedanigheid', 'verbose_name_plural': 'hoedanigheden'},
        ),
        migrations.AlterModelOptions(
            name='importmapping',
            options={'ordering': ['tabel_naam'], 'verbose_name': 'importmapping', 'verbose_name_plural': 'importmappings'},
        ),
        migrations.AlterModelOptions(
            name='locatie',
            options={'ordering': ['loc_id'], 'verbose_name': 'locatie', 'verbose_name_plural': 'locaties'},
        ),
        migrations.AlterModelOptions(
            name='mappingfield',
            options={'ordering': ['db_field'], 'verbose_name': 'mappingveld', 'verbose_name_plural': 'mappingvelden'},
        ),
        migrations.AlterModelOptions(
            name='meetnet',
            options={'ordering': ['id'], 'verbose_name': 'meetnet', 'verbose_name_plural': 'meetnetten'},
        ),
        migrations.AlterModelOptions(
            name='opname',
            options={'ordering': ['wns', 'locatie', 'datum', 'tijd'], 'verbose_name': 'opname', 'verbose_name_plural': 'opnames'},
        ),
        migrations.AlterModelOptions(
            name='parameter',
            options={'ordering': ['par_code'], 'verbose_name': 'parameter', 'verbose_name_plural': 'parameters'},
        ),
        migrations.AlterModelOptions(
            name='parametergroep',
            options={'ordering': ['code'], 'verbose_name': 'parametergroep', 'verbose_name_plural': 'parametergroepen'},
        ),
        migrations.AlterModelOptions(
            name='statuskrw',
            options={'ordering': ['code'], 'verbose_name': 'KRW status', 'verbose_name_plural': 'KRW statussen'},
        ),
        migrations.AlterModelOptions(
            name='waterlichaam',
            options={'ordering': ['wl_code'], 'verbose_name': 'waterlichaam', 'verbose_name_plural': 'waterlichamen'},
        ),
        migrations.AlterModelOptions(
            name='wns',
            options={'verbose_name': 'waarnemingssoort (WNS)', 'verbose_name_plural': 'waarnemingssoorten (WNS)'},
        ),
    ]
