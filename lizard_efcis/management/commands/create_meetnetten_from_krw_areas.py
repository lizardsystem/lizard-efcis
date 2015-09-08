import json
import logging
import sys

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon

from lizard_efcis.models import Locatie
from lizard_efcis.models import Meetnet

logger = logging.getLogger(__name__)

MEETNET_NAME = "Toetsresultaten KRW"



class Command(BaseCommand):
    help = '''Kopieer geimporteerde krw gebieden naar meetnetten'''

    def handle(self, *args, **options):

        base_krw_meetnet, created = Meetnet.objects.get_or_create(
            code=MEETNET_NAME)
        if created:
            logger.info("Created meetnet %s", base_krw_meetnet)

        for krw_locatie in Locatie.objects.filter(is_krw_area=True):
            # Create meetnet with the same name.
            name = krw_locatie.loc_oms.splitlines()[0]  # textfield...
            logger.info("Looking at krw locatie %s", name)
            meetnet, created = Meetnet.objects.get_or_create(
                code=name)
            meetnet.parent = base_krw_meetnet
            if created:
                logger.info("Created krw area as meetnet %s", meetnet)

            # Find locations within the area and assign them to the meetnet.
            existing_locaties = meetnet.locaties.values_list('id', flat=True)
            matching_locaties = Locatie.objects.filter(
                geo_punt1__within=krw_locatie.area).exclude(
                    id=krw_locatie.id).exclude(
                        id__in=existing_locaties).values_list('id', flat=True)
            logger.info("Found %s new locaties within the area", len(matching_locaties))
            meetnet.locaties.add(*matching_locaties)
            meetnet.save()
