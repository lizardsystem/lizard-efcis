import os

from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from lizard_efcis.import_data import DataImport
from lizard_efcis.models import ImportMapping


class Command(BaseCommand):
    help = '''Valideer data volgens de mapping.'''

    option_list = BaseCommand.option_list + (
        make_option('--mapping',
                    default=None,
                    help='mapping code'),
    )

    def handle(self, *args, **options):
        self.stdout.write('Start validatie.')
        mapping_code = options.get('mapping', None)
        if not mapping_code:
            self.stdout.write('Geef een mapping code.')
            return
        if not ImportMapping.objects.filter(code=mapping_code).exists():
            self.stdout.write(
                'De mapping code {} is niet gevonden.'.format(mapping_code))
            return
        data_import = DataImport()
        data_import.data_dir = os.path.join(
            settings.DATA_IMPORT_DIR, 'ibever')

        result = data_import.validate_csv('ibever.csv', mapping_code)
        if result:
            for k, v in result.iteritems():
                print k, v
        self.stdout.write('Einde validatie')
