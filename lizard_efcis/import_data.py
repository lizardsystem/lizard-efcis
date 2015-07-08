from datetime import datetime
import csv
import logging
import os

from django.conf import settings
from django.db import models as django_models
from django.db import IntegrityError
from django.db.models import ManyToManyField
from django.core.exceptions import ValidationError

from lxml.etree import XMLSyntaxError

from lizard_efcis import models
from lizard_efcis import utils
from lizard_efcis.umaquo_xml_parser import Parser

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
        self.log = False
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
        self.import_parametergroep('parameter.csv')
        self.import_parameter('parameter.csv')
        self.import_wns('wns.csv')
        self.import_csv('meetnet.csv', 'meetnet')
        self.import_csv('locaties_met_meetnet.csv', 'locaties')
        self.import_csv('hdsr_biologie.csv', 'activiteit-bio')

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
                fl = float(floatstr.replace(',', '.'))
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

    def _get_wns(self, parameter, eenheid, hoedanigheid, compartiment):
        options = {
            'parameter__iexact': parameter,
            'eenheid__iexact': eenheid,
            'hoedanigheid__iexact': hoedanigheid,
            'compartiment__iexact': compartiment}
        try:
            return models.WNS.objects.get(**options)
        except models.WNS.DoesNotExist:
            logger.error("WNS %s[%s][%s][%s] niet aanwezig." % (
                parameter,
                eenheid,
                hoedanigheid,
                compartiment
            ))
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
            logger.warn(
                "Activiteit {} does not exist.".format(activiteit))
            return None

    def _get_detect(self, teken):
        detectiegrenzen = models.Detectiegrens.objects.filter(
            teken__iexact=teken)
        if detectiegrenzen.exists():
            return detectiegrenzen[0]
        else:
            return None

    def _get_foreignkey_inst(
            self, val_raw, datatype, foreignkey_field, log=False):
        class_inst = django_models.get_model('lizard_efcis', datatype)
        inst = None
        try:
            if datatype == 'WNS' and foreignkey_field == 'wns_oms':
                if self.log:
                    logger.info("get wns %s %s" % (
                        datatype, ''.join(val_raw.split(' '))))
                inst = class_inst.objects.get(
                    wns_oms__iexact=''.join(val_raw.split(' ')))
            else:
                inst = class_inst.objects.get(
                    **{foreignkey_field: val_raw})
        except Exception as ex:
            if self.log:
                logger.error(
                    '{0}, Value: "{1}"'.format(ex.message, val_raw))
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
                    "Failed status or already exsists, "
                    "status '{}'.".format(status))

        logger.info(
            'End status creating: created={}.'.format(created))

    def import_status_krw(self, filename):
        logger.info("Import status_krw.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Interrupted import status_krw, "
                "unknown file '{}'.".format(filepath))
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
        logger.info('End status_krw import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def import_watertype(self, filename):
        logger.info("Import watertype.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted import watertype, "
                        "unknown file '{}'.".format(filepath))
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
        logger.info('End watertype import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def import_waterlichaam(self, filename):
        logger.info("Import waterlichaam.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted import waterlichaam, "
                        "unknown file '{}'.".format(filepath))
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
        logger.info('End waterlichaam import: updated={0}, '
                    'created={1}.'.format(updated, created))

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
        logger.info('End detectie creating: updated={0}, '
                    'created={1}.'.format(updated, created))

    def import_compartiment(self, filename):
        logger.debug("Import compartiment.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted import compartiment, "
                        "unknown file '{}'.".format(filepath))
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
        logger.info('End compartiment import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def import_hoedanigheid(self, filename):
        logger.info("Import hoedanigheid.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted hoedanigheid, unknown "
                        "file '{}'.".format(filepath))
            return

        updated = 0
        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            # skip first line with headers
            reader.next()
            for row in reader:
                try:
                    hd = models.Hoedanigheid.objects.get(
                        hoedanigheid=row[0])
                    updated = updated + 1
                except models.Hoedanigheid.DoesNotExist:
                    hd = models.Hoedanigheid(hoedanigheid=row[0])
                    created = created + 1
                hd.hoed_oms = row[1]
                hd.hoedanigheidgroep = row[2]
                hd.datum_status = self._datestr_to_date(row[3])
                hd.status = self._get_status(row[4])
                hd.save()
        logger.info('End heodanigheid import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def import_eenheid(self, filename):
        logger.info("Import eenheid.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted import eenheid, "
                        "unknown file '{}'.".format(filepath))
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
        logger.info('End eenheid import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def _get_parametergroep(self, code):
        parametergroep = None
        if code:
            groeps = models.ParameterGroep.objects.filter(code=code)
            if groeps.exists():
                parametergroep = groeps[0]
        return parametergroep

    def import_parametergroep(self, filename):
        logger.info("Import parametergroep.")
        mapping_codes = [
            'parametergroep-n0',
            'parametergroep-n1',
            'parametergroep-n2'
        ]
        for mapping_code in mapping_codes:
            if not models.ImportMapping.objects.filter(
                    code=mapping_code).exists():
                logger.info(
                    'De mapping code {} is niet gevonden. '
                    'Gebruik eerst management command '
                    '"create_mapping".'.format(mapping_code))
                return

            self.import_csv(filename, mapping_code)
        logger.info("Einde import parametergroep.")

    def import_parameter(self, filename):
        logger.info("Import parameter.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted import parameter, "
                        "unknown file '{}'.".format(filepath))
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

                par_groep2 = self._get_parametergroep(row[5])
                par_groep1 = self._get_parametergroep(row[4])
                par_groep0 = self._get_parametergroep(row[3])

                par.par_oms = row[1]
                par.casnummer = row[2]
                if par_groep2:
                    par.parametergroep = par_groep2
                elif par_groep1:
                    par.parametergroep = par_groep1
                elif par_groep0:
                    par.parametergroep = par_groep0
                else:
                    par.parametergroep = None
                par.datum_status = self._datestr_to_date(row[6])
                par.status = self._get_status(row[7])

                par.save()
        logger.info('End parameter import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def import_wns(self, filename):
        logger.info("Import wns.")
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn("Interrupted import WNS, "
                        "unknown file '{}'.".format(filepath))
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
        logger.info('End WNS import: updated={0}, '
                    'created={1}.'.format(updated, created))

    def set_data(self, inst, mapping, row, headers):
        """Set values to model instance. """
        for mapping_field in mapping:
            value = None
            datatype = mapping_field.db_datatype
            val_raw = row[headers.index(mapping_field.file_field)].strip(' "')
            if datatype == 'date':
                try:
                    value = datetime.strptime(
                        val_raw, mapping_field.data_format)
                except:
                    continue
            elif datatype == 'time':
                try:
                    value = datetime.strptime(
                        val_raw, mapping_field.data_format)
                except:
                    continue
            elif datatype == 'float':
                value = self._str_to_float(val_raw)
            elif datatype in models.MappingField.FOREIGNKEY_MODELS:
                # omit spaces
                val_space_omitted = val_raw
                if val_space_omitted:
                    # val_space_omitted = val_space_omitted.replace(' ', '')
                    val_space_omitted = val_space_omitted.strip(' ')
                value = self._get_foreignkey_inst(
                    val_space_omitted,
                    datatype,
                    mapping_field.foreignkey_field)
                if value is None:
                    if self.log:
                        logger.error("Value is None.")
                    continue
            else:
                if val_raw == '':
                    val_raw = None
                value = val_raw

            if isinstance(
                inst._meta.get_field(mapping_field.db_field),
                ManyToManyField
            ):
                inst.save()
                values = list(inst._meta.get_field(
                    mapping_field.db_field).value_from_object(inst))
                values.append(value)
                setattr(inst, mapping_field.db_field, values)
            else:
                if self.log:
                    logger.info("setattr %s, %s, %s." % (
                        mapping_field.db_field, value, type(value)))
                setattr(inst, mapping_field.db_field, value)

    def save_action_log(self, import_run, message):
        import_run.action_log = utils.add_text_to_top(
                import_run.action_log,
                message)
        import_run.save(force_update=True, update_fields=['action_log'])

    def check_csv(self, import_run, datetime_format, ignore_duplicate_key=True):
        """TODO create separate function per validation."""
        filepath = import_run.attachment.path
        mapping_code = import_run.import_mapping.code
        mapping = import_run.import_mapping
        is_valid = True

        logger.info("File check {}.".format(filepath))

        # Check or mapping contains fields
        mapping_fields = mapping.mappingfield_set.all()
        if mapping_fields.count() <= 0:
            message = "%s: %s %s.\n" % (
                datetime.now().strftime(datetime_format),
                "Geen veld in mapping",
                mapping_code)
            self.save_action_log(import_run, message)
            is_valid = False

        # Check delimeter
        if not mapping.scheiding_teken or len(mapping.scheiding_teken) > 1:
            message = "%s: %s %s.\n" % (
                datetime.now().strftime(datetime_format),
                "Scheidingsteken moet 1-character string zijn i.p.v.",
                mapping.scheiding_teken)
            self.save_action_log(import_run, message)
            is_valid = False

        if not is_valid:
            return is_valid

        # check headers
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            headers = reader.next()
            if not headers:
                message = "%s: %s %s.\n" % (
                    datetime.now().strftime(datetime_format),
                    "Bestand is leeg",
                    filepath)
                self.save_action_log(import_run, message)
                is_valid = False
            if headers and len(headers) <= 1:
                message = "%s: %s %s.\n" % (
                    datetime.now().strftime(datetime_format),
                    "Scheidingsteken is onjuist of het header bevat "
                    "alleen 1 veld",
                    headers[0])
                self.save_action_log(import_run, message)
                is_valid = False

        if not is_valid:
            return is_valid

        # check data integrity
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            headers = reader.next()
            for mapping_field in mapping_fields:
                if mapping_field.file_field not in headers:
                    message = "%s: %s %s.\n" % (
                        datetime.now().strftime(datetime_format),
                        "CSV-header bevat geen veld",
                        mapping_field.file_field)
                    self.save_action_log(import_run, message)
                    is_valid = False
            counter = 0
            for row in reader:
                counter += 1
                if len(row) != len(headers):
                    message = "%s: regelnr.: %s, %d.\n" % (
                        datetime.now().strftime(datetime_format),
                        "Aantal kolommen komt niet overeen "
                        "met het aantal headers",
                        reader.line_num)
                    self.save_action_log(import_run, message)
                    is_valid = False
                inst = django_models.get_model(
                    'lizard_efcis',
                    mapping.tabel_naam)()
                self.set_data(inst, mapping_fields, row, headers)
                if hasattr(inst.__class__, 'activiteit') and not hasattr(inst, 'activiteit'):
                    setattr(inst, 'activiteit', import_run.activiteit)
                try:
                    inst.full_clean()
                except ValidationError as e:
                    message = "%s:  regelnr.: %d, Foutmeldingen - %s\n" % (
                        datetime.now().strftime(datetime_format),
                        reader.line_num,
                        ", ".join(["%s: %s" % (k, ", ".join(v)) for k, v in e.message_dict.iteritems()])
                    )
                    self.save_action_log(import_run, message)
                    is_valid = False

            message = "%s: %s %d.\n" % (
                datetime.now().strftime(datetime_format),
                "Aantal rijen",
                counter)
            self.save_action_log(import_run, message)
        return is_valid

    def import_csv(self, filename, mapping_code,
                   activiteit=None, ignore_duplicate_key=True):
        logger.info("Import {}.".format(mapping_code))
        mapping = models.ImportMapping.objects.get(code=mapping_code)
        mapping_fields = mapping.mappingfield_set.all()
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.isfile(filepath):
            logger.warn(
                "Stop import {0}, dit is geen file '{1}'.".format(
                    mapping_code, filepath))
            return

        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            # read headers
            headers = reader.next()
            for row in reader:
                inst = django_models.get_model('lizard_efcis',
                                               mapping.tabel_naam)()
                if activiteit and hasattr(inst.__class__, 'activiteit'):
                    inst.activiteit = activiteit
                try:
                    self.set_data(inst, mapping_fields, row, headers)
                    created = created + 1
                except IntegrityError as ex:
                    if ignore_duplicate_key:
                        continue
                    else:
                        logger.error(ex.message)
                        break
        logger.info(
            'End import: created={}.'.format(created))

    def manual_import_csv(self, import_run, datetime_format, ignore_duplicate_key=True):

        is_imported = False
        filepath = import_run.attachment.path
        mapping = import_run.import_mapping
        activiteit = import_run.activiteit
        mapping_fields = mapping.mappingfield_set.all()

        created = 0
        with open(filepath, 'rb') as f:
            reader = csv.reader(f, delimiter=str(mapping.scheiding_teken))
            # read headers
            headers = reader.next()
            count = 0
            for row in reader:
                count += 1
                inst = django_models.get_model('lizard_efcis',
                                               mapping.tabel_naam)()
                try:
                    self.set_data(inst, mapping_fields, row, headers)
                    if mapping.tabel_naam == 'Opname':
                        setattr(inst, 'import_run', import_run)
                        setattr(inst, 'activiteit', activiteit)
                    inst.save()
                    created += 1
                except IntegrityError as ex:
                    if ignore_duplicate_key:
                        if self.log:
                            logger.error(ex.message)
                            message = "%s: %s.\n" % (
                                datetime.now().strftime(datetime_format),
                                ex.message
                            )
                            self.save_action_log(import_run, message)
                        continue
                    else:
                        logger.error(ex.message)
                        message = "%s: %s.\n" % (
                            datetime.now().strftime(datetime_format),
                            ex.message
                        )
                        self.save_action_log(import_run, message)
                        break
                except Exception as ex:
                    logger.error("%s." % ex.message)
                    message = "%s: %s.\n" % (
                        datetime.now().strftime(datetime_format),
                        ex.message
                    )
                    self.save_action_log(import_run, message)
                    break
        is_imported = True
        message = "%s: Created %d objects.\n" % (
            datetime.now().strftime(datetime_format),
            created
        )
        self.save_action_log(import_run, message)
        return is_imported

    def check_xml(self, import_run, datetime_format, ignore_dublicate_key=True):

        filepath = import_run.attachment.path
        activiteit = import_run.activiteit
        counter = 0
        is_valid = True
        umaquo_parser = None
        try:
            umaquo_parser = Parser(filepath)
            umaquo_parser.parse()
        except XMLSyntaxError as ex:
            message = "%s:  Foutmeldingen - %s\n" % (
                datetime.now().strftime(datetime_format),
                ex.message
            )
            self.save_action_log(import_run, message)
            return False

        if umaquo_parser.waardereekstijden <= 0:
            message = "%s: Geen waaardereekstijden gevonden, gezocht met '%s'\n" % (
                datetime.now().strftime(datetime_format),
                umaquo_parser.WAARDEREEKSTIJD_XPATH
            )
            self.save_action_log(import_run, message)
            is_valid = False
            return is_valid

        for waardereekstijd in umaquo_parser.waardereekstijden.values():
            print (umaquo_parser.get_locatie_id(waardereekstijd))
            counter += 1
            tijdserie = umaquo_parser.get_tijdserie(waardereekstijd)
            opname = models.Opname()
            opname.datum = datetime.strptime(
                tijdserie[0], '%Y-%m-%d')
            opname.tijd = datetime.strptime(
                tijdserie[1], '%H:%M:%S')
            opname.waarde_n = tijdserie[2]
            opname.wns = self._get_foreignkey_inst(
                umaquo_parser.get_wns_oms(waardereekstijd),
                'WNS',
                'wns_oms')
            opname.locatie = self._get_foreignkey_inst(
                umaquo_parser.get_locatie_id(waardereekstijd),
                'Locatie',
                'loc_id')
            opname.activiteit = activiteit
            print (umaquo_parser.get_locatie_id(waardereekstijd))
            try:
                opname.full_clean()
            except ValidationError as e:
                message = "%s:  regelnr.: %d, Foutmeldingen - %s\n" % (
                    datetime.now().strftime(datetime_format),
                    waardereekstijd.sourceline,
                    ", ".join(["%s: %s" % (k, ", ".join(v)) for k, v in e.message_dict.iteritems()])
                )
                self.save_action_log(import_run, message)
                is_valid = False

        message = "%s: %s %d.\n" % (
            datetime.now().strftime(datetime_format),
            "Aantal rijen",
            counter)
        self.save_action_log(import_run, message)
        return is_valid

    def manual_import_xml(self, import_run, datetime_format, ignore_dublicate_key=True):

        is_imported = False
        filepath = import_run.attachment.path
        activiteit = import_run.activiteit
        created = 0
        umaquo_parser = Parser(filepath)
        umaquo_parser.parse()
        for waardereekstijd in umaquo_parser.waardereekstijden.values():
            tijdserie = umaquo_parser.get_tijdserie(waardereekstijd)
            opname = models.Opname()
            opname.datum = datetime.strptime(
                        tijdserie[0], '%Y-%m-%d')
            opname.tijd = datetime.strptime(
                        tijdserie[1], '%H:%M:%S')
            opname.waarde_n = tijdserie[2]
            opname.wns = self._get_foreignkey_inst(
                umaquo_parser.get_wns_oms(waardereekstijd),
                'WNS',
                'wns_oms')
            opname.locatie = self._get_foreignkey_inst(
                umaquo_parser.get_locatie_id(waardereekstijd),
                'Locatie',
                'loc_id')
            opname.activiteit = activiteit
            try:
                opname.save()
                created += 1
            except IntegrityError as ex:
                if ignore_duplicate_key:
                    if self.log:
                        logger.error(ex.message)
                        message = "%s: %s.\n" % (
                            datetime.now().strftime(datetime_format),
                            ex.message)
                        self.save_action_log(import_run, message)
                        continue
                    else:
                        logger.error(ex.message)
                        message = "%s: %s.\n" % (
                            datetime.now().strftime(datetime_format),
                            ex.message)
                        self.save_action_log(import_run, message)
                        break
            except Exception as ex:
                logger.error("%s." % ex.message)
                message = "%s: %s.\n" % (
                    datetime.now().strftime(datetime_format),
                    ex.message
                )
                self.save_action_log(import_run, message)
                break
        is_imported = True
        message = "%s: Created %d objects.\n" % (
            datetime.now().strftime(datetime_format),
            created
        )
        self.save_action_log(import_run, message)
        return is_imported
