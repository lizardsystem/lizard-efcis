import os
import csv
import glob

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from lizard_efcis.import_data import DataImport

class Command(BaseCommand):
    help = '''Import or update parameters from csv-file where row
    <parameterid>,<parametername>'''
    
    option_list = BaseCommand.option_list + (
        make_option('--f',
                    default=None,
                    help='csv-filepath with parameters.'),
    )                
        
    def handle(self, *args, **options):
        self.stdout.write('End import')
        
        data_import = DataImport()
        data_import.data_dir = os.path.join(
            settings.DATA_IMPORT_DIR, 'domain')
        data_import.create_status()
        data_import.import_status_krw('status_krw.csv')
        data_import.import_watertype('watertype.csv')
        data_import.import_waterlichaam('waterlichaam.csv')
        data_import.create_detectie()
        data_import.import_compartiment('compartiment.csv')
        data_import.import_hoedanigheid('hoedanigheid.csv')
        data_import.import_eenheid('eenheid.csv')
        data_import.import_parameter('parameter.csv')
        data_import.import_wns('wns.csv')
        
        # filepath = options.get('f', None)
        # if filepath is None:
        #     self.stdout.write('Tell me where is the csv-file with parameters.')
        #     return

        self.stdout.write('End import')
