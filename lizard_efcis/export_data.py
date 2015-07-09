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
                         
    mapping_fields = import_mapping.mappingfield_set.all()
    context.append(mapping_fields.values_list('file_field', flat=True))
    for model_object in queryset:
        row = []
        for mapping_field in mapping_fields:
            value = getattr(model_object, mapping_field.db_field, '')

            datatype = mapping_field.db_datatype

            if datatype == 'date' or datatype == 'time':
                try:
                    row.append(value.strftime(mapping_field.data_format))
                except:
                    continue
            elif datatype in models.MappingField.FOREIGNKEY_MODELS:
                row.append(getattr(value, mapping_field.foreignkey_field, ''))
            else:
                row.append(value)
        context.append(row)
    return context
        
