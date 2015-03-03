import os
import csv
import glob
import time
from datetime import datetime

from django.db import IntegrityError
from django.conf import settings
from django.db import models as django_models
from lizard_efcis import models

import logging
logger = logging.getLogger(__name__)

class DataImport(object):
    help = '''
    Import or update data for models:
    status_krw, watertype, waterlichaam, wns, parameter, eenheid,
    hoedanigheid, coompartiment.
    The import files are in data/domain

    Create initial values for status and detectiegrens models.

    Expect decimals compared with a point.
    '''
    
    def __init__(self):
        self.data_dir = os.path.join(
            settings.DATA_IMPORT_DIR, 'domain')
        inserted_id = []

    def import_domain_data(self):
        self.create_status()
        self.import_status_krw('status_krw.csv')
        self.import_watertype('watertype.csv')
        self.import_waterlichaam('waterlichaam.csv')
        self.create_detectie()
        self.import_compartiment('compartiment.csv')
        self.import_hoedanigheid('hoedanigheid.csv')
        self.import_eenheid('eenheid.csv')
        self.import_parameter('parameter.csv')
        self.import_wns('wns.csv')

    def _datestr_to_date(self, datestr):
        dt = None
        try:
            if datestr:
                dt = datetime.strptime(
                    datestr,
                    settings.IMPORT_DATE_FORMAT).date()
        except ValueError as err:
            logger.debug(err.message)
        except TypeError as err:
            logger.debug(err.message)
        return dt

    def _str_to_float(self, floatstr):
        fl = None
        try:
            if floatstr:
                fl = float(floatstr.replace(',','.'))
        except ValueError as err:
            logger.debug(err.message)
        except:
            logger.debug("THE rest")
        return fl

    def _remove_leading_quotes(self, quotedstr):
        
        if not isinstance(quotedstr, str):
            return quotedstr

        newstr = quotedstr.strip('"')
        
        return newstr
            

    def _get_status(self, status):
        statuses = models.Status.objects.filter(
            naam__iexact=status)
        if statuses.exists():
            return statuses[0]
        return None

    def _get_parameter(self, parameter):
        parameters = models.Parameter.objects.filter(
            par_code__iexact=parameter)
        if parameters.exists():
            return parameters[0]
        return None

    def _get_eenheid(self, eenheid):
        eenheden = models.Eenheid.objects.filter(
            eenheid__iexact=eenheid)
        if eenheden.exists():
            return eenheden[0]
        return None

    def _get_hoedanigheid(self, hoedanigheid):
        hoedanigheden = models.Hoedanigheid.objects.filter(
           hoedanigheid__iexact=hoedanigheid)
        if hoedanigheden.exists():
            return hoedanigheden[0]
        return None

    def _get_compartiment(self, compartiment):
        compartiments = models.Compartiment.objects.filter(
            compartiment__iexact=compartiment)
        if compartiments.exists():
            return compartiments[0]
        return None

    def _get_locatie(self, locid):
        locations = models.Locatie.objects.filter(
            loc_id__iexact=locid)
        if locations.exists():
            return locations[0]
        else:
            logger.warn("Location {} does not exist.".format(locid))
            return None

    def _get_activiteit(self, activiteit):
        activiteiten = models.Activiteit.objects.filter(
            activiteit__iexact=activiteit)
        if activiteiten.exists():
            return activiteiten[0]
        else:
            logger.warn("Activiteit {} does not exist.".format(activiteit))
            return None

    def _get_detect(self, teken):
        detectiegrenzen = models.Detectiegrens.objects.filter(
            teken__iexact=teken)
        if detectiegrenzen.exists():
            return detectiegrenzen[0]
        else:
            #logger.warn("Detectiegrens {} does not exist.".format(teken))
            return None

    def _get_wns(self, wnsoms) :
        wnses = models.WNS.objects.filter(
            wns_oms__iexact=wnsoms )
        if wnses.exists():
            return wnses[0]
        else:
            logger.warn("WNS {} does not exist.".format(wnsoms))
            return None

    def _get_foreignkey_inst(
            self, val_raw, datatype, foreignkey_field):
        class_inst = django_models.get_model('lizard_efcis', datatype)
        inst = None
        try:
            inst = class_inst.objects.get(
            **{foreignkey_field: val_raw})
        except Exception as ex:
            logger.error('{0}, Value: "{1}"'.format(ex.message, val_raw))
        return inst
        
    def create_status(self):
        logger.info("Create status.")
        created = 0
        for status in models.Status.STATUS_LIST:
            try:
                models.Status(naam=status).save()
                created = created + 1
            except:
                logger.debug(
                    "Failed status or already exsists, status '{}'.".format(status))

        logger.info('End status creating: created={}.'.format(created))
        
    def import_status_krw(self, filename):
        logger.info("Import status_krw.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import status_krw, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    status_krw = models.StatusKRW.objects.get(code=row[0])
                    updated = updated + 1
                except models.StatusKRW.DoesNotExist:
                    status_krw = models.StatusKRW(code=row[0])
                    created = created + 1
                status_krw.omschrijving = row[1]
                status_krw.datum_begin = self._datestr_to_date(row[2])
                status_krw.datum_eind = self._datestr_to_date(row[3])
                status_krw.datum_status = row[4]
                status_krw.save()
        logger.info(
            'End status_krw import: updated={0}, created={1}.'.format(updated, created))

    def import_watertype(self, filename):
        logger.info("Import watertype.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import watertype, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    watertype = models.Watertype.objects.get(code=row[0])
                    updated = updated + 1
                except models.Watertype.DoesNotExist:
                    watertype = models.Watertype(code=row[0])
                    created = created + 1
                watertype.omschrijving = row[1]
                watertype.groep = row[2]
                watertype.datum_begin = self._datestr_to_date(row[3])
                watertype.datum_eind = self._datestr_to_date(row[4])
                watertype.datum_status = row[5]
                watertype.save()
        logger.info(
            'End watertype import: updated={0}, created={1}.'.format(updated, created))

    def import_waterlichaam(self, filename):
        logger.info("Import waterlichaam.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import waterlichaam, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    wl = models.Waterlichaam.objects.get(wl_code=row[0])
                    updated = updated + 1
                except models.Waterlichaam.DoesNotExist:
                    wl = models.Waterlichaam(wl_code=row[0])
                    created = created + 1
                wl.wl_naam = row[1]
                wl.wl_type = row[2]
                wl.wl_oms = row[3]
                wl.status = row[4]
                wl.save()
        logger.info(
            'End waterlichaam import: updated={0}, created={1}.'.format(updated, created))

    def create_detectie(self):
        logger.info("Create detectie.")
        updated = 0
        created = 0
        detect_list = [
            ['<', 'onder detectiegrens'],
            ['>', 'boven detectiegrens']
        ]
        for row in detect_list:
            try:
                detect = models.Detectiegrens.objects.get(teken=row[0])
                updated = updated + 1
            except models.Detectiegrens.DoesNotExist:
                detect = models.Detectiegrens(teken=row[0])
                created = created + 1
            detect.omschrijving = row[1]
            detect.save()
        logger.info(
            'End detectie creating: updated={0}, created={1}.'.format(updated, created))
    
    def import_compartiment(self, filename):
        logger.debug("Import compartiment.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import compartiment, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    comp = models.Compartiment.objects.get(compartiment=row[0])
                    updated = updated + 1
                except models.Compartiment.DoesNotExist:
                    comp = models.Compartiment(compartiment=row[0])
                    created = created + 1
                comp.comp_oms = row[1]
                comp.compartimentgroep = row[2]
                comp.datum_status = self._datestr_to_date(row[3])
                comp.status = self._get_status(row[4])
                comp.save()
        logger.info(
            'End compartiment import: updated={0}, created={1}.'.format(updated, created))

    def import_hoedanigheid(self, filename):
        logger.info("Import hoedanigheid.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted hoedanigheid, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    hd = models.Hoedanigheid.objects.get(hoedanigheid=row[0])
                    updated = updated + 1
                except models.Hoedanigheid.DoesNotExist:
                    hd = models.Hoedanigheid(hoedanigheid=row[0])
                    created = created + 1
                hd.hoed_oms = row[1]
                hd.hoedanigheidgroep = row[2]
                hd.datum_status = self._datestr_to_date(row[3])
                hd.status = self._get_status(row[4])
                hd.save()
        logger.info(
            'End heodanigheid import: updated={0}, created={1}.'.format(updated, created))

    def import_eenheid(self, filename):
        logger.info("Import eenheid.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import eenheid, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    eenheid = models.Eenheid.objects.get(eenheid=row[0])
                    updated = updated + 1
                except models.Eenheid.DoesNotExist:
                    eenheid = models.Eenheid(eenheid=row[0])
                    created = created + 1
                
                eenheid.eenheid_oms = row[1]
                eenheid.dimensie = row[2]
                eenheid.omrekenfactor = self._str_to_float(row[3])
                eenheid.eenheidgroep = row[4]
                eenheid.datum_status = self._datestr_to_date(row[5])
                eenheid.status = self._get_status(row[6])
                eenheid.save()
        logger.info(
            'End eenheid import: updated={0}, created={1}.'.format(updated, created))

    def import_parameter(self, filename):
        logger.info("Import parameter.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import parameter, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    par = models.Parameter.objects.get(par_code=row[0])
                    updated = updated + 1
                except models.Parameter.DoesNotExist:
                    par = models.Parameter(par_code=row[0])
                    created = created + 1
                
                par.par_oms = row[1]
                par.casnummer = row[2]
                par.parametergroep0 = row[3]
                par.parametergroep1 = row[4]
                par.parametergroep2 = row[5]
                par.datum_status = self._datestr_to_date(row[6])
                par.status = self._get_status(row[7])
                par.save()
        logger.info(
            'End parameter import: updated={0}, created={1}.'.format(updated, created))

    def import_wns(self, filename):
        logger.info("Import wns.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import WNS, unknown file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    wns = models.WNS.objects.get(wns_code=row[0])
                    updated = updated + 1
                except models.WNS.DoesNotExist:
                    wns = models.WNS(wns_code=row[0])
                    created = created + 1
                
                wns.wns_oms = row[1]
                wns.parameter = self._get_parameter(row[2])
                wns.eenheid = self._get_eenheid(row[3])
                wns.hoedanigheid = self._get_hoedanigheid(row[4])
                wns.compartiment = self._get_compartiment(row[5])
                wns.datum_status = self._datestr_to_date(row[6])
                wns.status = self._get_status(row[7])
                wns.save()
        logger.info(
            'End WNS import: updated={0}, created={1}.'.format(updated, created))

    def set_data(self, inst, mapping, row, headers):
        """Set values to model instance. """
        for mapping_field in mapping:
            value = None
            datatype = mapping_field.db_datatype
            val_raw = row[headers.index(mapping_field.file_field)].strip(' "')
            if datatype == 'date':
                try:
                    value = datetime.strptime(val_raw, mapping_field.data_format)
                except:
                    continue
            elif datatype == 'time':
                try:
                    value = datetime.strptime(val_raw, mapping_field.data_format)
                except:
                    continue
            elif datatype == 'float':
                value = self._str_to_float(val_raw)
            elif datatype in models.MappingField.FOREIGNKEY_MODELS:
                # omit spaces
                val_space_omitted = val_raw
                if val_space_omitted:
                    val_space_omitted = val_space_omitted.replace(' ', '')
                value = self._get_foreignkey_inst(
                    val_space_omitted,
                    datatype,
                    mapping_field.foreignkey_field)
                if value is None:
                    continue
            else:
                value = val_raw
                
            setattr(inst, mapping_field.db_field, value)


    def validate_csv(self, filename, mapping_code, ignore_dublicate_key=True):
        roles = {
            '001': 'Het bestand bestaat niet. "{}"',
            '002': 'Bestand is leeg. "{}"',
            '003': 'Scheidingsteken moet 1-character string zijn. mapping_code: "{0}, scheiding_teken: "{1}"',
            '004': 'Scheidingsteken is onjuist of het header bevat alleen 1-veld. scheiding_teken: "{0}", header: "{1}"',
            '005': 'Mapping bestaat niet. "{}"',
            '006': 'Mapping bevat het veld.',
            '007': 'Mappingsveld komt niet voor in csv-header. "{}"',
            '008': 'Data Integritei: melding: {}',
            '009': ''}
        result = []
        logger.info("Validatie {}.".format(filename))
        #001
        code = "001"
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrup validatie, is not a file '{}'.".format(
                    filepath))
            result.append({code: roles[code].format(filepath)})
        #005
        code = "005"
        mappings = models.ImportMapping.objects.filter(code=mapping_code)
        mapping = None
        if mappings.exists():
            mapping = mappings[0]
        else:
            result.append({code: roles[code].format(mapping_code)})
            
        if result:
            return result

        #006
        code = "006"
        mapping_fields = mapping.mappingfield_set.all()
        if mapping_fields.count() <= 0:
            result.append({code: roles[code]})
        #003
        code = "003"
        if not mapping.scheiding_teken or len(mapping.scheiding_teken) > 1:
            result.append({code: roles[code].format(mapping_code, mapping.scheiding_teken)})
        
        if result:
            return result
        
        #002, 004
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            headers = reader.next()
            code = "002"
            if not headers:
                result.append({code: roles[code].format(filepath)})
            code = "004"
            if headers and len(headers) <= 1:
                result.append({code: roles[code].format(mapping.scheiding_teken, headers[0])})
                
        if result:
            return result

        #007, 008
        code = "007"
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            headers = reader.next()
            for mapping_field in mapping_fields:
                if mapping_field.file_field not in headers:
                    result.append({code: roles[code].format(mapping_field.file_field)})
            for row in reader:
                code = "008"
                val_raw = row[headers.index(mapping_field.file_field)].strip(' "')
                # omit spaces
                val_raw = val_raw.replace(' ', '')
                inst = self._get_foreignkey_inst(
                    val_raw,
                    mapping_field.db_datatype,
                    mapping_field.foreignkey_field)
                if inst is None:
                    result.append({code: "{0} '{1}' niet aanwezig in domain-tabel.".format(
                        mapping_field.db_datatype, val_raw)})
                try:
                    inst = django_models.get_model('lizard_efcis', mapping.tabel_naam)()
                    self.set_data(inst, mapping_fields, row, headers)
                    inst.validate_unique()
                except Exception as ex:
                    if not ignore_dublicate_key:
                        result.append({code: ex.message()})
        
    def import_csv(self, filename, mapping_code, activiteit=None, ignore_dublicate_key=True):
        logger.info("Import {}.".format(mapping_code))
        mapping = models.ImportMapping.objects.get(code=mapping_code)
        mapping_fields = mapping.mappingfield_set.all()
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrup import {0}, is not a file '{1}'.".format(
                    mapping_code, filepath))
            return
        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            # read headers
            headers = reader.next()
            for row in reader:
                inst = django_models.get_model('lizard_efcis', mapping.tabel_naam)()
                self.set_data(inst, mapping_fields, row, headers)
                if activiteit and hasattr(inst.__class__, 'activiteit'):
                    inst.activiteit = activiteit
                try:
                    saved = inst.save()
                    if saved:
                        created = created + 1
                except IntegrityError as ex:
                    if ignore_dublicate_key:
                        continue
                    else:
                        logger.error(ex.message)
                        break
        logger.info(
            'End import: created={}.'.format(created))
