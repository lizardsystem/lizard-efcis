import cStringIO
import codecs
import csv
import logging

from django.contrib.gis.db.models import Model

from lizard_efcis import models


logger = logging.getLogger(__name__)


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def create_compartimentid(id):
    return '%s.%s.%s' % (id, 'monster', 'id')


def get_opnames(opnames):
    opnames_dict = {}
    for opname in opnames:
        opnames_dict[opname.id] = {
            'id': opname.id,
            'parameter': '%s;%s' % (
                opname.wns.parameter.par_code,
                opname.wns.parameter.par_oms),
            'eenheid': '%s;%s' % (
                opname.wns.eenheid.eenheid,
                opname.wns.eenheid.eenheid_oms),
            'hoedanigheid': '%s;%s' % (
                opname.wns.hoedanigheid.hoedanigheid,
                opname.wns.hoedanigheid.hoed_oms),
            'datum': opname.datum.strftime('%Y-%m-%d'),
            'tijd': opname.datum.strftime('%H:%M:%S'),
            'monsterobjectid': create_compartimentid(
                opname.wns.compartiment.id),
            'waarde': opname.waarde_n
        }
    return opnames_dict.values()


def get_compartiments(opnames):
    compartiments = {}
    for opname in opnames:
        compartimentid = create_compartimentid(
            opname.wns.compartiment.id)
        compartiment = compartiments.get(compartimentid)
        if not compartiment:
            compartiment = {
                'id': compartimentid,
                'compartiment': '%s;%s' % (
                    opname.wns.compartiment.compartiment,
                    opname.wns.compartiment.comp_oms),
                'meetobjectid': opname.locatie.loc_id,
                'waardereeks_ids': [opname.id]}
        else:
            compartiment['waardereeks_ids'].append(opname.id)
        compartiments[compartimentid] = compartiment
    return compartiments.values()


def get_locaties(opnames):
    locaties = {}
    for opname in opnames:
        locatie = locaties.get(opname.locatie.id)

        compartimentid = create_compartimentid(
            opname.wns.compartiment.id)
        if not locatie:
            locaties['opname.locatie.id'] = {
                'id': opname.locatie.loc_id,
                'locatie_naam': opname.locatie.loc_oms,
                'monsterobject_ids': [compartimentid]}
    return locaties.values()


def get_xml_context(opnames):
    context = {}
    context['meetobjecten'] = get_locaties(opnames)
    context['monsterobjecten'] = get_compartiments(opnames)
    context['waardereeksen'] = get_opnames(opnames)
    return context


def create_mapping_field(file_field, db_field):
    return {
        'db_field': db_field,
        'file_field': file_field,
        'db_datatype': 'CharField'}


def retrieve_mapping_fields(import_mapping):
    """
    Add wns-fields: Parameter, Eenheid, Hoedanigheid, Comapartiment
    Retunr mapping fileds as dictionary.
    """
    mapping_fields = import_mapping.mappingfield_set.all().values()
    wns_fields = import_mapping.mappingfield_set.filter(
        **{'db_datatype': 'WNS', 'file_field__contains': '['})
    if not wns_fields:
        return mapping_fields

    tmp_mapping = []
    for field in mapping_fields:
        if field.get('db_datatype') == 'WNS':
            additional_fields = field.get(
                'file_field', '').replace(']', '').split('[')
            if len(additional_fields) == 4:
                tmp_mapping.append(
                    create_mapping_field(additional_fields[0], 'par_code'))
                tmp_mapping.append(
                    create_mapping_field(additional_fields[1], 'eenheid'))
                tmp_mapping.append(
                    create_mapping_field(additional_fields[2], 'hoedanigheid'))
                tmp_mapping.append(
                    create_mapping_field(additional_fields[3], 'compartiment'))
            else:
                tmp_mapping.append(field)
        else:
            tmp_mapping.append(field)

    return tmp_mapping


def retrieve_headers(mapping_fields):
    headers = []
    for mapping_field in mapping_fields:
        headers.append(mapping_field.get('file_field', ''))
    return headers


import resource
def using(point=""):
    usage=resource.getrusage(resource.RUSAGE_SELF)
    return '''%s: usertime=%s systime=%s mem=%s mb
           '''%(point,usage[0],usage[1],
                (usage[2]*resource.getpagesize())/1024.0/1024.0 )


def get_csv_context(queryset, import_mapping):
    """
    Retrieve data conform the mapping.
    Not suitable for ManyToMany fields"""

    import datetime
    th1 = datetime.datetime.now()
    
    # if queryset.model.__name__ != import_mapping.tabel_naam:
    #     logger.error("Wrong mapping, queryset of '%s' mapped "
    #                  "to the table name '%s' in the mapping "
    #                  "'%s'." % (
    #                      queryset.model.__name__,
    #                      import_mapping.tabel_naam,
    #                      import_mapping.code))
    #     raise StopIteration
    t1_mf = datetime.datetime.now()
    mapping_fields = retrieve_mapping_fields(import_mapping)
    t2_mf = datetime.datetime.now()
    print("RETRIEVE MAPPING FIELDS: %f" % (t2_mf - t1_mf).total_seconds())
    headers = retrieve_headers(mapping_fields)
    # Add headers for extra fields
    extra_field_headers, extra_field_values = import_mapping.extra_field_lists()
    if extra_field_headers:
        headers.extend(extra_field_headers)

    context = [headers]
    count = 0
    print(using("External FOR START"))
    full_fieldnames = [mappingfield.full_fieldname() for mappingfield in import_mapping.mappingfield_set.all()]
    print(full_fieldnames)
    result = queryset.values(*full_fieldnames)
    print(using("BEFORE File WRITTEN: to tmp"))
    # import pdb; pdb.set_trace()
    # with open('/tmp/result.txt', 'wb') as f:
    #     for row in result.iterator():
    #         f.write(repr(row))
    # print(using("File WRITTEN: to tmp"))
    # del queryset
    # print(using("After queryset deletion"))
    for model_object in result.iterator():
        if count == 0:
            print(using("External FOR START"))
            count += 1
        elif count == 10000:
            count = 0
        else:
            count+=1
        row = []
        t1 = datetime.datetime.now()
        for mapping_field in mapping_fields:
            value_out = ''
            if hasattr(model_object, mapping_field.get('db_field')):
                value = getattr(model_object, mapping_field.get('db_field'), '')
            else:
                value = "Fout in mapping db_field: '%s' bestaat niet." % mapping_field.get('db_field')
            datatype = mapping_field.get('db_datatype')
            if datatype == 'date' or datatype == 'time':
                try:
                    tf1 = datetime.datetime.now()
                    value_out = value.strftime(
                        mapping_field.get('data_format'))
                    tf2 = datetime.datetime.now()
                   # print("DATE TIME: %f" % (tf2 - tf1).total_seconds())
                except:
                    value_out = ''
            elif value and datatype in models.MappingField.FOREIGNKEY_MODELS:
                if type(value).__name__ == 'ManyRelatedManager':
                    tm1 = datetime.datetime.now()
                    meetnetten = value.filter(
                        code=mapping_field.get('file_field'))
                    if meetnetten.exists():
                        value = meetnetten[0]
                    tm2 = datetime.datetime.now()
                    #print("MANU2Many: %f" % (th2 - th1).total_seconds() )
                foreign_fields = mapping_field.get('foreignkey_field', '').split('__')
                # Used only 2 fields separated with '__'
                tk1 = datetime.datetime.now()
                if len(foreign_fields) >= 2:
                    
                    if hasattr(value, foreign_fields[0]):
                        value = getattr(value, foreign_fields[0])
                    foreignkey_field = foreign_fields[1]
                else:
                    foreignkey_field = foreign_fields[0]
                if hasattr(value, foreignkey_field):
                    value_out = getattr(value, foreignkey_field, '')
                else:
                    value_out = ''
                tk2 = datetime.datetime.now()
                #print("FOREIGN VALUE: %f" % (tk2 - tk1).total_seconds())
            else:
                value_out = value

            if isinstance(value_out, int):
                value_out = str(value_out)
            if isinstance(value_out, float):
                value_out = str(value_out)
            if isinstance(value_out, Model):
                value_out = "Fout in mapping: wijst naar compleet item i.p.v. veld"
            if value_out is None:
                value_out = ''
            row.append(value_out)
        t2 = datetime.datetime.today()
        #print("RETRIEVE 1 RECORD: %f" % (t2 - t1).total_seconds())
        # Add values for extra fields
        t_ef1 = datetime.datetime.today()
        for extra_field_value in extra_field_values:
            row.append(extra_field_value)
        t_ef2 = datetime.datetime.today()
        #print("EXTRA FIELDS: %f" % (t_ef2 - t_ef1).total_seconds())
        context.append(row)
    th2 = datetime.datetime.now()
    print("----TOTAL DURATION %f----" % (th2 - th1).total_seconds() )
    return context
