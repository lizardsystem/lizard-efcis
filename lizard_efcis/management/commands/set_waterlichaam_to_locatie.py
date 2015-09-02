from optparse import make_option
import csv

from django.core.management.base import BaseCommand

from lizard_efcis.models import Locatie, Waterlichaam


class Command(BaseCommand):
    help = '''Set waterlichaam to locatie.'''

    option_list = BaseCommand.option_list + (
        make_option('--f',
                    default=None,
                    help='filepath'),
    )

    def handle(self, *args, **options):
        print 'Start import'
        filepath = options.get('f', None)
        if not filepath:
            print 'Geef een file.'
            return
        counter = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    if row[0] and row[1]:
                        waterlichaam = Waterlichaam.objects.get(wl_code=row[1])
                        locatie = Locatie.objects.get(loc_id=row[0])
                        locatie.waterlichaam = waterlichaam
                        locatie.save()
                        counter += 1
                    else:
                        print "locatie ne/of waterlichaam niet ingevuld. regel: %d" % reader.line_num
                except Waterlichaam.DoesNotExist:
                    print "Waterlichaam '%s' niet gevonden. regel: %d" % (row[1], reader.line_num)
                except Locatie.DoesNotExist:
                    print "Locatie '%s' niet gevonden. regel: %d" % (row[0], reader.line_num)
        print 'Einde import, geimporteerd %d' % counter
