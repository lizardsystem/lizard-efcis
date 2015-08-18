import logging

from django.core.management.base import BaseCommand

from lizard_efcis.models import FTPLocation
from lizard_efcis import ftp_access

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Debug info voor de eerste FTP locatie"

    def handle(self, *args, **options):
        ftp_location = FTPLocation.objects.all()[0]
        print(ftp_access.debug_info(ftp_location))
