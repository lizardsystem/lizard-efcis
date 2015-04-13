from django.core.management.base import BaseCommand

from lizard_efcis import models


class Command(BaseCommand):
    help = '''Delete all efcis data.'''

    def handle(self, *args, **options):
        self.stdout.write('Start deleting efcis-data.')
        models.Activiteit.objects.all().delete()
        models.Compartiment.objects.all().delete()
        models.Detectiegrens.objects.all().delete()
        models.Eenheid.objects.all().delete()
        models.Hoedanigheid.objects.all().delete()
        models.ImportMapping.objects.all().delete()
        models.Locatie.objects.all().delete()
        models.Meetnet.objects.all().delete()
        models.MappingField.objects.all().delete()
        models.Opname.objects.all().delete()
        models.Parameter.objects.all().delete()
        models.ParameterGroep.objects.all().delete()
        models.Status.objects.all().delete()
        models.StatusKRW.objects.all().delete()
        models.Waterlichaam.objects.all().delete()
        models.Watertype.objects.all().delete()
        models.WNS.objects.all().delete()
