# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0014_auto_20150303_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opname',
            options={'ordering': ['wns', 'locatie', 'datum', 'tijd']},
        ),
        migrations.AlterUniqueTogether(
            name='opname',
            unique_together=set([('datum', 'tijd', 'wns', 'locatie')]),
        ),
    ]
