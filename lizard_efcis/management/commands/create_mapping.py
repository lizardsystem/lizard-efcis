from django.core.management.base import BaseCommand

from lizard_efcis.models import ImportMapping, MappingField


class Command(BaseCommand):
    help = '''Aanmaken import-mappings for csv-file'''

    def handle(self, *args, **options):
        self.create_ibever_loc_mapping()
        self.create_ibever_opname_mapping()
        self.create_mapping_parameter_groep_n0()
        self.create_mapping_parameter_groep_n1()
        self.create_mapping_parameter_groep_n2()
        self.create_mapping_meetnet()
        self.stdout.write('Einde import')

    def add_mapping_fields(self, imp_mapping, mapping_fields):
        try:
            for mapping_fields_dict in mapping_fields:
                mapping_field = MappingField(
                    mapping=imp_mapping,
                    **mapping_fields_dict)
                mapping_field.save()
                imp_mapping.mappingfield_set.add(mapping_field)
        except Exception as ex:
            # Rollback
            ImportMapping.objects.filter(code=imp_mapping.code).delete()
            self.stderr.write(ex.message)

    def create(self, import_mapping, mapping_fields):
        try:
            imp_mapping = ImportMapping.objects.get(
                code=import_mapping['code'])
            self.stdout.write(
                'Mapping {} bestaat al.'.format(import_mapping['code']))
        except ImportMapping.DoesNotExist:
            imp_mapping = ImportMapping(**import_mapping)
            imp_mapping.save()
            self.add_mapping_fields(imp_mapping, mapping_fields)
            self.stdout.write(
                "Mapping {} aangemaakt.".format(import_mapping['code']))

    def create_mapping_parameter_groep_n0(self):
        import_mapping = {
            'code': 'parametergroep-n0',
            'tabel_naam': 'ParameterGroep',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'code',
                'file_field': 'parametergroup0',
                'db_datatype': 'CharField'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_mapping_parameter_groep_n1(self):
        import_mapping = {
            'code': 'parametergroep-n1',
            'tabel_naam': 'ParameterGroep',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'code',
                'file_field': 'parametergroup1',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'parent',
                'file_field': 'parametergroup0',
                'db_datatype': 'ParameterGroep',
                'foreignkey_field': 'code'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_mapping_parameter_groep_n2(self):
        import_mapping = {
            'code': 'parametergroep-n2',
            'tabel_naam': 'ParameterGroep',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'code',
                'file_field': 'parametergroup2',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'parent',
                'file_field': 'parametergroup1',
                'db_datatype': 'ParameterGroep',
                'foreignkey_field': 'code'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_ibever_loc_mapping(self):

        import_mapping = {
            'code': 'iBever-locaties',
            'tabel_naam': 'Locatie',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }
        mapping_fields = [
            {
                'db_field': 'loc_id',
                'file_field': 'mpn_mpnident',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'loc_oms',
                'file_field': 'mpn_mpnomsch',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'x1',
                'file_field': 'mpn_mrfxcoor',
                'db_datatype': 'float'
            },
            {
                'db_field': 'y1',
                'file_field': 'mpn_mrfycoor',
                'db_datatype': 'float'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_ibever_opname_mapping(self):
        dformat = '%d-%m-%Y'
        tformat = '%H:%M:%S'
        import_mapping = {
            'code': 'iBever-opnames',
            'tabel_naam': 'Opname',
            'omschrijving': 'Automatisch gegenereerde mapping.',
        }
        mapping_fields = [
            {
                'db_field': 'datum',
                'file_field': 'mwa_mwadtmb',
                'db_datatype': 'date',
                'data_format': dformat
            },
            {
                'db_field': 'tijd',
                'file_field': 'mwa_mwatijdb',
                'db_datatype': 'time',
                'data_format': tformat
            },
            {
                'db_field': 'waarde_n',
                'file_field': 'mwa_mwawrden',
                'db_datatype': 'float',
            },
            {
                'db_field': 'waarde_a',
                'file_field': 'mwa_mwawrdea',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'locatie',
                'file_field': 'mpn_mpnident',
                'db_datatype': 'Locatie',
                'foreignkey_field': 'loc_id'
            },
            {
                'db_field': 'wns',
                'file_field': 'wns_osmomsch',
                'db_datatype': 'WNS',
                'foreignkey_field': 'wns_oms'
            },
            {
                'db_field': 'detect',
                'file_field': 'mrsinovs_domafkrt',
                'db_datatype': 'Detectiegrens',
                'foreignkey_field': 'teken'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_mapping_meetnet(self):
        import_mapping = {
            'code': 'meetnet',
            'tabel_naam': 'Meetnet',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'id',
                'file_field': 'id',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'code',
                'file_field': 'code',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'parent',
                'file_field': 'parent_id',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_mapping_locations(self):
        import_mapping = {
            'code': 'locaties',
            'tabel_naam': 'Locatie',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'loc_id',
                'file_field': 'LOC_ID',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'loc_oms',
                'file_field': 'LOC_OMS',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'x1',
                'file_field': 'X1_COORD',
                'db_datatype': 'float'
            },
            {
                'db_field': 'y1',
                'file_field': 'Y1_COORD',
                'db_datatype': 'float'
            },
            {
                'db_field': 'x2',
                'file_field': 'X2_COORD',
                'db_datatype': 'float'
            },
            {
                'db_field': 'y2',
                'file_field': 'Y2_COORD',
                'db_datatype': 'float'
            },
            {
                'db_field': 'waterlichaam',
                'file_field': 'WATERLICHAAM',
                'db_datatype': 'Waterlichaam',
                'foreignkey_field': 'code'
            },
            {
                'db_field': 'watertype',
                'file_field': 'WATERTYPE',
                'db_datatype': 'Watertype',
                'foreignkey_field': 'code'
            },
            {
                'db_field': 'status_krw',
                'file_field': 'STATUS_KRW',
                'db_datatype': 'StatusKRW',
                'foreignkey_field': 'code'
            },
            {
                'db_field': 'metnet',
                'file_field': '',
                'db_datatype': 'StatusKRW',
                'foreignkey_field': 'code'
            }
        ]
        self.create(import_mapping, mapping_fields)
