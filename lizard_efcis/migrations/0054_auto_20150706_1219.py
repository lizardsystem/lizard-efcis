# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def everything_is_validated(apps, schema_editor):
    """Set all opnames as validated."""
    Opname = apps.get_model("lizard_efcis", "Opname")
    hardcoded_value = 1  # VALIDATED
    # Not importing from manager.py to keep migrations working.
    Opname.objects.all().update(validation_state=hardcoded_value)


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0053_auto_20150706_1209'),
    ]

    operations = [
        migrations.RunPython(everything_is_validated)
    ]
