# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

KRW_SCORE_MAPPING = {
    # Copied to ensure that future migrations keep working
    'voldoet': 0.9,
    'voldoet niet': 0.1,
    'zeer goed': 0.9,
    'goed': 0.7,
    'matig': 0.5,
    'ontoereikend': 0.3,
    'slecht': 0.1,
}


def fill_krw_scores(apps, schema_editor):
    # Improved non-save() using version from step 0076.
    Opname = apps.get_model("lizard_efcis", "Opname")
    for key, value in KRW_SCORE_MAPPING.items():
        for opname in Opname.objects.filter(waarde_a__iexact=key):
            print("Re-saving opname %s (waarde_a=%s)" % (opname, opname.waarde_a))
            opname.waarde_krw = KRW_SCORE_MAPPING[opname.waarde_a.lower()]
            opname.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0076_auto_20150914_1548'),
    ]

    operations = [
    ]
