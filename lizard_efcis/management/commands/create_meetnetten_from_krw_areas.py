import logging

from django.core.management.base import BaseCommand

from lizard_efcis.models import Locatie
from lizard_efcis.models import Meetnet

logger = logging.getLogger(__name__)

MEETNET_NAME = "KRW Waterlichamen"


class Command(BaseCommand):
    help = '''Kopieer geimporteerde krw gebieden naar meetnetten'''

    def handle(self, *args, **options):

        krw_meetnet, created = Meetnet.objects.get_or_create(
            code=MEETNET_NAME)
        if created:
            logger.info("Created meetnet %s", krw_meetnet)
        existing_locaties = krw_meetnet.locaties.values_list('id', flat=True)

        for krw_locatie in Locatie.objects.filter(is_krw_area=True):
            # Remove possible previously created *meetnet* with the same name.
            name = krw_locatie.loc_oms.splitlines()[0]  # textfield...
            logger.info("Looking at krw locatie %s", name)
            for meetnet in Meetnet.objects.filter(code=name):
                logger.warn("Deleting accidentally created meetnet %s", meetnet)
                meetnet.locaties = []  # Not sure if it is needed, actually.
                meetnet.save()
                meetnet.delete()

            # Attach locatie to the krw meetnet
            if not krw_locatie.id in existing_locaties:
                krw_meetnet.locaties.add(krw_locatie)
                logger.info("Attached locatie %s to meetnet %s",
                            krw_locatie, krw_meetnet)
                krw_meetnet.save()
