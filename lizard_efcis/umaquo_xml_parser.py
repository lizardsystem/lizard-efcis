from lxml import etree


class Parser(object):

    WAARDEREEKSTIJD_XPATH = '//gml:FeatureCollection/gml:featureMembers/umam:WaardeReeksTijd'
    MONSTER_OBJECT_XPATH = '//gml:FeatureCollection/gml:featureMembers/umam:MonsterObject'

    DATUM_XPATH = 'umam:reekswaarde/umam:TijdWaarde/umam:beginTijd/umam:DatumTijdDataType/umam:datum'
    TIJD_XPATH = 'umam:reekswaarde/umam:TijdWaarde/umam:beginTijd/umam:DatumTijdDataType/umam:tijd'
    NUMERIEKE_WAARDE_XPATH = 'umam:reekswaarde/umam:TijdWaarde/umam:numeriekeWaarde/umam:WaardeDataType/umam:getalswaarde'

    def __init__(self, filepath, *args, **kwargs):
        self.namespaces = {
            'gml': 'http://www.opengis.net/gml',
            'umam': 'http://www.aquo.nl/umam2013',
            'xlink': 'http://www.w3.org/1999/xlink',
        }
        self.filepath = filepath
        self.monsterobjects = {}
        self.waardereekstijden = {}

    def parse(self):
        tree = None
        parser = etree.XMLParser(ns_clean=True)
        tree = etree.parse(self.filepath, parser)

        for monsterobject in tree.xpath(
                Parser.MONSTER_OBJECT_XPATH,
                namespaces=self.namespaces):
            monsterobjectid = monsterobject.get(
                '{%s}id' % self.namespaces.get('gml'))
            self.monsterobjects[monsterobjectid] = monsterobject
        for reeks in tree.xpath(
                Parser.WAARDEREEKSTIJD_XPATH,
                namespaces=self.namespaces):
            waardereekstijdid = reeks.get(
                '{%s}id' % self.namespaces.get('gml'))
            self.waardereekstijden[waardereekstijdid] = reeks

    def get_text_part(self, text, partindex):
        text_parts = text.split(';')
        if len(text_parts) > partindex:
            return text_parts[0]
        return text

    def get_compartiment(self, monsterobject):
        """
        Retrieve first part of the text of
        first compartiment-element.
        Arguments:
           monsterobject - etree xml-objects found
           by tag 'umam:MonsterObject'
        """
        compartiments = monsterobject.xpath(
            'umam:compartiment',
            namespaces=self.namespaces)
        if compartiments:
            return self.get_text_part(compartiments[0].text, 0)
        return None

    def get_eenheid(self, waardereekstijd):
        """
        Retrieve first part of the text of
        first eenheid-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        eenheden = waardereekstijd.xpath(
            'umam:eenheid',
            namespaces=self.namespaces)
        if eenheden:
            return self.get_text_part(eenheden[0].text, 0)
        return None

    def get_hoedanigheid(self, waardereekstijd):
        """
        Retrieve first part of the text of
        first hoedanigheid-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        hoedanigheden = waardereekstijd.xpath(
            'umam:hoedanigheid',
            namespaces=self.namespaces)
        if hoedanigheden:
            return self.get_text_part(hoedanigheden[0].text, 0)
        return None

    def get_parameter(self, waardereekstijd):
        """
        Retrieve first part of the text of
        first parameter-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        parameters = [parameter for parameter in waardereekstijd.iterdescendants(
            '{%s}parameter' % self.namespaces['umam'])]
        parameter_values = []
        for parameter in parameters:
            parameter_values = [child.text.strip() for child in parameter.iterdescendants()]
            break
        for value in parameter_values:
            if value:
                return self.get_text_part(value, 0)
        return None

    def get_hoortbijmonsterobject_id(self, waardereekstijd):
        """
        Retrieve related monsterobjectid of first
        hoortBijMonsterObject-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        hoortbijmonsterobjects = waardereekstijd.xpath(
            'umam:hoortBijMonsterObject',
            namespaces=self.namespaces)
        if hoortbijmonsterobjects:
            monsterobjectid = hoortbijmonsterobjects[0].get(
                '{%s}href' % self.namespaces.get('xlink'))
            monsterobjectid = monsterobjectid.replace('#', '')
            return monsterobjectid
        return None

    def get_hoortbijmeetobject_id(self, monsterobject):
        """
        Retrieve related meetobjectid of first
        hoortBijMeetObject-element.
        Meetobejctsid is a locatieId.
        Arguments:
           monsterobject - etree xml-objects found
           by tag 'umam:MonsterObjects'
        """
        hoortbijmeetobjects = monsterobject.xpath(
            'umam:hoortBijMeetObject',
            namespaces=self.namespaces)
        if hoortbijmeetobjects:
            meetobjectid = hoortbijmeetobjects[0].get(
                '{%s}href' % self.namespaces.get('xlink'))
            meetobjectid = meetobjectid.replace('#', '')
            return meetobjectid
        return None

    def get_tijdserie(self, waardereekstijd):
        """
        Retrieve tijdserie [datum, tijd, waarde].
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        datum = waardereekstijd.xpath(
            Parser.DATUM_XPATH,
            namespaces=self.namespaces)[0].text
        tijd = waardereekstijd.xpath(
            Parser.TIJD_XPATH,
            namespaces=self.namespaces)[0].text
        waarde = waardereekstijd.xpath(
            Parser.NUMERIEKE_WAARDE_XPATH,
            namespaces=self.namespaces)[0].text
        return [datum, tijd, waarde]

    def get_wns_oms(self, waardereekstijd):
        parameter = self.get_parameter(waardereekstijd)
        eenheid = self.get_eenheid(waardereekstijd)
        hoedanigheid = self.get_hoedanigheid(waardereekstijd)

        monsterobjectid = self.get_hoortbijmonsterobject_id(waardereekstijd)
        compartiment = self.get_compartiment(
            self.monsterobjects.get(monsterobjectid))

        return '%s[%s][%s][%s]' % (
            parameter,
            eenheid,
            hoedanigheid,
            compartiment)

    def get_locatie_id(self, waardereekstijd):
        monsterobjectid = self.get_hoortbijmonsterobject_id(
            waardereekstijd)
        meetobjectid = self.get_hoortbijmeetobject_id(
                self.monsterobjects.get(monsterobjectid))
        return meetobjectid

    def print_wns(self):
        for waardereekstijd in self.waardereekstijden.values():
            parameter = self.get_parameter(waardereekstijd)
            eenheid = self.get_eenheid(waardereekstijd)
            hoedanigheid = self.get_hoedanigheid(waardereekstijd)

            monsterobjectid = self.get_hoortbijmonsterobject_id(waardereekstijd)
            compartiment = self.get_compartiment(
                self.monsterobjects.get(monsterobjectid))

            meetobjectid = self.get_hoortbijmeetobject_id(
                self.monsterobjects.get(monsterobjectid))
            print ('%s[%s][%s][%s], %s, %s' % (
                parameter,
                eenheid,
                hoedanigheid,
                compartiment,
                meetobjectid,
                ', '.join(self.get_tijdserie(waardereekstijd))
            ))
