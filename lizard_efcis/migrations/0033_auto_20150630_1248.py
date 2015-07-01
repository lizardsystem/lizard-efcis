# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0032_wns_wns_oms_space_less'),
    ]

    operations = [
        migrations.AddField(
            model_name='opname',
            name='import_run',
            field=models.ForeignKey(blank=True, to='lizard_efcis.ImportRun', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importmapping',
            name='tabel_naam',
            field=models.CharField(help_text='Import tabel', max_length=255, choices=[('Opname', 'Opname'), ('Locatie', 'Locatie'), ('ParameterGroep', 'ParameterGroep'), ('Meetnet', 'Meetnet'), ('Activiteit', 'Activiteit'), ('WNS', 'WNS')]),
            preserve_default=True,
        ),
    ]
