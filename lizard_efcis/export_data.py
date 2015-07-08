#

from lizard_efcis import models


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
