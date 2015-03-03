import os
import csv
import glob

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from lizard_efcis.import_data import DataImport
from lizard_efcis.models import Activiteit, ImportMapping

class Command(BaseCommand):
    help = '''Import parameter-groeps.'''
        
    def handle(self, *args, **options):
        self.stdout.write('Start import')
        mapping_codes = [
            'parametergroep-n0',
            'parametergroep-n1',
            'parametergroep-n2'
        ]
        for mapping_code in mapping_codes:
            if not ImportMapping.objects.filter(code=mapping_code).exists():
                self.stdout.write(
                    'De mapping code {} is niet gevonden. '
                    'Gebruik eerst management command "create_mapping".'.format(mapping_code))
                return
            data_import = DataImport()
            data_import.data_dir = os.path.join(
                settings.DATA_IMPORT_DIR, 'domain')

            data_import.import_csv('parameter.csv', mapping_code, ignore_dublicate_key=True)
        
        self.stdout.write('Einde import')
