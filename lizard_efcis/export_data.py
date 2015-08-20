#
import logging

from lizard_efcis import models


logger = logging.getLogger(__name__)


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


def get_csv_context(queryset, import_mapping):
    """
    Retrieve data conform the mapping.
    Not suitable for ManyToMany fields"""
    context = []
    if queryset.model.__name__ != import_mapping.tabel_naam:
        logger.error("Wrong mapping, queryset of '%s' mapped "
                     "to the table name '%s' in the mapping "
                     "'%s'." % (
                         queryset.model.__name__,
                         import_mapping.tabel_naam,
                         import_mapping.code))
        return None

    mapping_fields = retrieve_mapping_fields(import_mapping)

    headers = retrieve_headers(mapping_fields)
    context = [headers]
    for model_object in queryset:
        row = []
        for mapping_field in mapping_fields:

            value = getattr(model_object, mapping_field.get('db_field'), '')

            datatype = mapping_field.get('db_datatype')

            if datatype == 'date' or datatype == 'time':
                try:
                    row.append(value.strftime(
                        mapping_field.get('data_format')))
                except:
                    continue
            elif datatype == 'Meetnet':
                meetnetten = value.filter(code=mapping_field.get('file_field'))
                if meetnetten.exists():
                    row.append(meetnetten[0].id)
                else:
                    row.append('')
            elif datatype in models.MappingField.FOREIGNKEY_MODELS:
                row.append(getattr(
                    value, mapping_field.get('foreignkey_field'), ''))
            else:
                row.append(value)
        context.append(row)
    return context
