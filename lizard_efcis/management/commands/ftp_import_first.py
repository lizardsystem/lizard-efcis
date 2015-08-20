import logging

from django.core.management.base import BaseCommand

from lizard_efcis.models import FTPLocation
from lizard_efcis import ftp_access

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import the first available file per FTP connection"

    def handle(self, *args, **options):
        for ftp_location in FTPLocation.objects.all():
            print(ftp_access.handle_first_file(ftp_location))
