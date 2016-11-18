# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_meetstatus_omschrijving(apps, schema_editor):
    MeetStatus = apps.get_model('lizard_efcis', 'MeetStatus')
    for row in MeetStatus.objects.all():
        if row.naam == "FC-A BIO-A":
            row.omschrijving = "Fysisch-chemisch actief & Biologisch actief"
        elif row.naam == "FC-A BIO-BG":
            row.omschrijving = "Fysisch-chemisch actief & Biologisch buiten gebruik"
        elif row.naam == "FC-A BIO-NB":
            row.omschrijving = "Fysisch-chemisch actief & Biologisch niet bemeten"
        elif row.naam == "FC-BG BIO-A":
            row.omschrijving = "Fysisch-chemisch buiten gebruik & Biologisch actief"
        elif row.naam == "FC-NB BIO-A":
            row.omschrijving = "Fysisch-chemisch niet bemeten & Biologisch actief"
        elif row.naam == "FC-BG BIO-BG":
            row.omschrijving = "Fysisch-chemisch buiten gebruik & Biologisch buiten gebruik"
        elif row.naam == "FC-NB BIO-BG":
            row.omschrijving = "Fysisch-chemisch niet bemeten & Biologisch buiten gebruik"
        elif row.naam == "FC-BG BIO-NB":
            row.omschrijving = "Fysisch-chemisch buiten gebruik & Biologisch niet bemeten"
        else:
            continue
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lizard_efcis', '0092_meetstatus_omschrijving'),
    ]

    operations = [ migrations.RunPython(set_meetstatus_omschrijving) ]
