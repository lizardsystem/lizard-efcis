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

MEETNET_NAME = "KRW Waterlichamen"


class Command(BaseCommand):
    help = '''Importeren krw json file als locaties'''

    def handle(self, *args, **options):
        if not len(args) == 1:
            logger.error("Pass one argument: the krw .json file")
            sys.exit(1)
        geojson_file = args[0]
        geojson_contents = json.loads(open(geojson_file).read())
        features = geojson_contents['features']

        krw_meetnet, created = Meetnet.objects.get_or_create(
            code=MEETNET_NAME)

        for feature in features:
            geometry = feature['geometry']
            geojson_geometry = json.dumps(geometry)
            area = GEOSGeometry(geojson_geometry)
            if isinstance(area, Polygon):
                area = MultiPolygon(area)
            name = feature['properties']['OWMNAAM']
            loc_id = feature['properties']['OWMIDENT']
            logger.info("Found location %s (%s)", name, loc_id)
            locatie, created = Locatie.objects.get_or_create(loc_id=loc_id)
            locatie.loc_oms = name
            locatie.area = area
            locatie.is_krw_area = True
            locatie.meetnet = [krw_meetnet]
            locatie.save()
