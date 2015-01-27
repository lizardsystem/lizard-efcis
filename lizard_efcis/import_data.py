import os
import csv
import glob
import datetime

from django.conf import settings

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
            dt = datetime.datetime.strptime(
                datestr, settings.IMPORT_DATE_FORMAT).date()
        except ValueError as err:
            logger.warn(err.message)
        except TypeError as err:
            logger.warn(err.message)
        return dt

    def _str_to_float(self, floatstr):
        fl = None
        try:
            fl = float(floatstr)
        except ValueError as err:
            logger.warn(err.message)
        except:
            logger.warn("THE rest")
        return fl

    def _remove_leading_quotes(self, quotedstr):
        
        if not isinstance(quotedstr, str):
            return quotedstr

        newstr = quotedstr.strip()
        if newstr[:1] == '"':
            newstr = newstr.replace('"', '', 1)
        
        if newstr[len(newstr)-1:] == '"':
            newstr = ''.join(reversed(newstr))
            newstr = newstr.replace('"', '', 1)
            newstr = ''.join(reversed(newstr))
        
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
            logger.warn("Detectiegrens {} does not exist.".format(teken))
            return None

    def _get_wns(self, wnsoms) :
        wnses = models.WNS.objects.filter(
            wns_oms__iexact=wnsoms )
        if wnses.exists():
            return wnses[0]
        else:
            logger.warn("WNS {} does not exist.".logger(wnsoms))
            return None
    
    def create_status(self):
        logger.info("Create status.")
        created = 0
        for status in models.Status.STATUS_LIST:
            try:
                models.Status(naam=status).save()
                created = created + 1
            except:
                logger.warn(
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
            ['<', 'onder detectiegrans'],
            ['>', 'boven detectiegrans'],
            ['-', '']
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

    def import_locaties_from_ibever(self, filename):
        logger.info("import locaties from iBever.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import hist opname iBever '{}'.".format(filepath))
            return
        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # read headers
            headers = reader.next()
            for row in reader:
                try:
                    location = models.Locatie()
                    location.loc_id = self._remove_leading_quotes(row[headers.index('mpn_mpnident')])
                    location.loc_oms = self._remove_leading_quotes(row[headers.index('mpn_mpnomsch')])
                    location.save()
                    created = created + 1
                except:
                    logger.warn("Locatie not created {}.".format(row[headers.index('mpn_mpnident')]))
            logger.info(
                'End Location import: created={}.'.format(created))

    def import_hist_opname_ibever(self, filename, activiteit):
        logger.info("Import ibever.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import hist opname iBever '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # read headers
            headers = reader.next()
            for row in reader:
                try:
                    opname = models.Opname()
                    opname.moment = datetime.datetime.now()

                    waarde_n = self._remove_leading_quotes(row[headers.index('mwa_mwawrden')]).replace(',','.')
                    waarde_a = self._remove_leading_quotes(row[headers.index('mwa_mwawrdea')]).replace(',','.')
                    locatie = self._remove_leading_quotes(row[headers.index('mpn_mpnident')])

                    opname.waarde_n = self._str_to_float(waarde_n)
                    opname.waarde_a = self._str_to_float(waarde_a)
                    opname.activiteit = activiteit
                    opname.wns = self._get_wns(self._remove_leading_quotes(row[headers.index('wns_osmomsch')]))
                    opname.locatie = self._get_locatie(locatie)
                    opname.detect = self._get_detect(self._remove_leading_quotes(row[headers.index('mrsinovs_domafkrt')]))
                    opname.save()
                    created = created + 1
                except:
                    logger.warn("Could not create opname object." )
        logger.info(
            'End iBever import: created={1}.'.format(created))
