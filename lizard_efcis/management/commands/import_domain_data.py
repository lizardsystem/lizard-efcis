import os

from optparse import make_option

from django.core.management.base import BaseCommand
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
        #data_import.import_domain_data()
        data_import.import_csv('meetnet.csv', 'meetnet')
        self.stdout.write('End import')
