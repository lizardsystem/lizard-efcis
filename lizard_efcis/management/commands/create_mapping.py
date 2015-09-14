from django.core.management.base import BaseCommand

from lizard_efcis.models import ImportMapping, MappingField


class Command(BaseCommand):
    help = '''Aanmaken import-mappings for csv-file'''

    def handle(self, *args, **options):
        self.create_ibever_opname_mapping()
        self.create_hdsr_bio_opname_mapping()
        self.create_mapping_parameter_groep_export()
        self.create_mapping_parameter_groep_n0()
        self.create_mapping_parameter_groep_n1()
        self.create_mapping_parameter_groep_n2()
        self.create_mapping_parameter()
        self.create_mapping_meetnet()
        self.create_mapping_locations()
        self.create_mapping_activiteit_bio()
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

    def create_mapping_activiteit_bio(self):
        import_mapping = {
            'code': 'activiteit-bio',
            'tabel_naam': 'Activiteit',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'activiteit',
                'file_field': 'activiteit',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'act_type',
                'file_field': 'TYPE',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'act_oms',
                'file_field': 'ACT_OMS',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'met_mafa',
                'file_field': 'MET_MAFA',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'met_mafy',
                'file_field': 'MET_MAFY',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'met_fyt',
                'file_field': 'MET_FYT',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'met_vis',
                'file_field': 'MET_VIS',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'met_fc',
                'file_field': 'MET_FC',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'met_toets',
                'file_field': 'MET_TOETS',
                'db_datatype': 'CharField'
            }
        ]
        self.create(import_mapping, mapping_fields)

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

    def create_mapping_parameter(self):
        dformat = '%d-%m-%Y'
        import_mapping = {
            'code': 'parameter',
            'tabel_naam': 'Parameter',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'id',
                'file_field': 'intern_id',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'par_code',
                'file_field': 'PAR_CODE',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'par_oms',
                'file_field': 'PAR_OMS',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'casnummer',
                'file_field': 'CASnummer',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'parametergroep',
                'file_field': 'parametergroep',
                'db_datatype': 'ParameterGroep',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'datum_status',
                'file_field': 'DATUM_STATUS',
                'db_datatype': 'date',
                'data_format': dformat
            },
            {
                'db_field': 'status',
                'file_field': 'STATUS',
                'db_datatype': 'Status',
                'foreignkey_field': 'naam'
            }
        ]
        self.create(import_mapping, mapping_fields)

    def create_mapping_parameter_groep_export(self):
        import_mapping = {
            'code': 'parametergroep-export',
            'tabel_naam': 'ParameterGroep',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
             {
                'db_field': 'id',
                'file_field': 'intern_id',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'code',
                'file_field': 'code',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'parent',
                'file_field': 'parent',
                'db_datatype': 'ParameterGroep',
                'foreignkey_field': 'code'
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

    def create_hdsr_bio_opname_mapping(self):
        dformat = '%d-%m-%Y'
        import_mapping = {
            'code': 'hdsr-bio-opnames',
            'tabel_naam': 'Opname',
            'omschrijving': 'Automatisch gegenereerde mapping.'
        }

        mapping_fields = [
            {
                'db_field': 'datum',
                'file_field': 'datum',
                'db_datatype': 'date',
                'data_format': dformat
            },
            {
                'db_field': 'waarde_n',
                'file_field': 'waarde_n',
                'db_datatype': 'float',
            },
            {
                'db_field': 'waarde_a',
                'file_field': 'waarde_a',
                'db_datatype': 'CharField'
            },
            {
                'db_field': 'locatie',
                'file_field': 'LOC_ID',
                'db_datatype': 'Locatie',
                'foreignkey_field': 'loc_id'
            },
            {
                'db_field': 'wns',
                'file_field': 'WNS_CODE',
                'db_datatype': 'WNS',
                'foreignkey_field': 'wns_code'
            },
            {
                'db_field': 'detect',
                'file_field': 'DETECT',
                'db_datatype': 'Detectiegrens',
                'foreignkey_field': 'teken'
            },
            {
                'db_field': 'activiteit',
                'file_field': 'activiteit',
                'db_datatype': 'Activiteit',
                'foreignkey_field': 'activiteit'
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
                'file_field': 'intern_id',
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
                'db_field': 'id',
                'file_field': 'intern_id',
                'db_datatype': 'CharField'
            },
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
                'db_field': 'fc_status',
                'file_field': 'STATUS_FC',
                'db_datatype': 'FCStatus',
                'foreignkey_field': 'naam'
            },
            {
                'db_field': 'bio_status',
                'file_field': 'STATUS_BIO',
                'db_datatype': 'BioStatus',
                'foreignkey_field': 'naam'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Voorgedefinieerde meetpuntgroepen',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Fysisch-chemisch meetnet',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Biologisch meetnet',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Basis',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'GBM',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Roulerend (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Zwemwater',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Projecten (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Onbekend (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'KRW (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Roulerend (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Projecten (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'KRW (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'MNLSO',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'CMNO',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'LMGBM',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'CSD (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'GROM (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'KRR Honswijk (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'LBW (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'LOP (LOP)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'OR (FC)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'NL14_01 Langbroekerw',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'CSD (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'GROM (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'KRR Honswijk (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'LBW (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'LOP (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'OR (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Overig',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'Onbekend (BIO)',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            },
            {
                'db_field': 'meetnet',
                'file_field': 'KRW Waterlichamen',
                'db_datatype': 'Meetnet',
                'foreignkey_field': 'id'
            }
        ]
        self.create(import_mapping, mapping_fields)
