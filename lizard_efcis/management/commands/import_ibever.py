import os
import csv
import glob

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from lizard_efcis.import_data import DataImport
from lizard_efcis.models import Activiteit

class Command(BaseCommand):
    help = '''Import Location, Opname from ibever csv-file'''
    
    option_list = BaseCommand.option_list + (
        make_option('--f',
                    default=None,
                    help='not implemented'),
    )                
        
    def handle(self, *args, **options):
        self.stdout.write('End import')
        
        data_import = DataImport()
        data_import.data_dir = os.path.join(
            settings.DATA_IMPORT_DIR, 'ibever')
        
        activiteiten = Activiteit.objects.filter(activiteit='import ibever')
        if activiteiten.exists():
            activiteit = activiteiten[0]
        else:
            activiteit = Activiteit(activiteit='import ibever')
            activiteit.save()
        data_import.import_locaties_from_ibever('ibever.csv')
        data_import.import_hist_opname_ibever('ibever.csv', activiteit)
        
        self.stdout.write('End import')
