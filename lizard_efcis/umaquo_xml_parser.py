import os
from lxml import etree


namespaces = {
    'gml': 'http://www.opengis.net/gml',
    'umam': 'http://www.aquo.nl/umam2013'
}

filename = '/mnt/hgfs/VMWEB/efcis.xml'

compartiment_xpath = '//gml:FeatureCollection/gml:featureMembers/umam:FysiekMonster/umam:compartiment'
waardenreeks_xpath = '//gml:FeatureCollection/gml:featureMembers/umam:WaardeReeksTijd'

#parser = etree.XMLParser(ns_clean=True)
#tree = etree.parse(filepath, parser)
#waardereeksen = tree.xpath(waardenreeks_xpath, namespaces)
#wardereeks1 = waardereeksen[0].text


class FeatureCollection(object):
    
    def __init__(self, *args, **kwargs):
        self.ns = 'gml'
        self.name = 'FeatureCollection'
        self.namespaces = {
            'gml': 'http://www.opengis.net/gml',
            'umam': 'http://www.aquo.nl/umam2013',
            'xlink': 'http://www.w3.org/1999/xlink',
        }
        self.id = ''
        self.featureMemebers = []

    def element_name(self):
        return '%s:%s' % (self.ns, self.name)

    def id_attr_name(self):
        return '%s:id' % self.gml


class FeatureMembers(object):

    def __init__(self, *args, **kwargs):
        self.ns = 'gml' 
        self.name = 'featureMembers'
        self.tagname = '%s:%s' % (self.ns, self.name)


class Parser(object):

    def __init__(self, filepath, *args, **kwargs):
        self.namespaces = {
            'gml': 'http://www.opengis.net/gml',
            'umam': 'http://www.aquo.nl/umam2013',
            'xlink': 'http://www.w3.org/1999/xlink',
        }
        self.filepath = filepath
        self.meetobjects = {}
        self.fysiekmonsters = {}
        self.monsterobjects = {}
        self.waardereekstijden = {}

    def check_file(self):
        if not os.path.isfile(self.filepath):
            return (False, "%s - is geen bestand")
        return (True, '')

    def parse(self):
        tree = None
        try:
            parser = etree.XMLParser(ns_clean=True)
            tree = etree.parse(self.filepath, parser)
        except Exception as ex:
            return (False, ex.message)

        
        for meetobject in tree.xpath('//umam:MeetObject', namespaces=self.namespaces):
            self.meetobjects.update({
                meetobject.get('{%s}id' % self.namespaces.get('gml')): meetobject})
        for fysiekmonster in tree.xpath('//umam:FysiekMonster', namespaces=self.namespaces):
            self.fysiekmonsters.update({
                fysiekmonster.get('{%s}id' % self.namespaces.get('gml')): fysiekmonster})
        for monsterobject in tree.xpath('//umam:MonsterObject', namespaces=self.namespaces):
            self.monsterobjects.update({
                monsterobject.get('{%s}id' % self.namespaces.get('gml')): monsterobject})
        for reeks in tree.xpath('//umam:WaardeReeksTijd', namespaces=self.namespaces):
            self.waardereekstijden.update({
                reeks.get('{%s}id' % self.namespaces.get('gml')): reeks})

    def get_text_part(self, text, partindex):
        text_parts = text.split(';')
        if len(text_parts) > partindex:
            return text_parts[0]
        return text
            
    def get_compartiment(self, monsterobject):
        """
        Retrieve text of first compartiment-element.
        Arguments:
           monsterobject - etree xml-objects found
           by tag 'umam:MonsterObject'
        """
        compartiments = monsterobject.xpath(
            'umam:compartiment',
            namespaces=self.namespaces)
        for compartiment in compartiments:
            return self.get_text_part(compartiment.text, 0)
        return None

    def get_eenheid(self, waardereekstijd):
        """
        Retrieve text of firts eenheid-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        eenheden = waardereekstijd.xpath(
            'umam:eenheid',
            namespaces=self.namespaces)
        for eenheid in eenheden:
            return self.get_text_part(eenheid.text, 0)
        return None

    def get_hoedanigheid(self, waardereekstijd):
        """
        Retrieve text of firts hoedanigheid-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        hoedanigheden = waardereekstijd.xpath(
            'umam:hoedanigheid',
            namespaces=self.namespaces)
        for hoedanigheid in hoedanigheden:
            return self.get_text_part(hoedanigheid.text, 0)
        return None

    def get_parameter(self, waardereekstijd):
        """
        Retrieve text of firts parameter-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        parameters =  [parameter for parameter in waardereekstijd.iterdescendants(
            '{%s}parameter' % namespaces['umam'])]
        parameter_values = []
        for parameter in parameters:
            parameter_values = [child.text.strip() for child in parameter.iterdescendants()]
            break
        for value in parameter_values:
            if value:
                return self.get_text_part(value, 0)
        return None

    def get_hoortbijmonstrobject_id(self, waardereekstijd):
        """
        Retrieve related monsterobjectid of firts 
        hoortBijMonsterObject-element.
        Arguments:
           waardereekstijd - etree xml-objects found
           by tag 'umam:WaardereeksTijd'
        """
        hoortbijmonsterobjects = waardereekstijd.xpath(
            'umam:hoortBijMonsterObject',
            namespaces=self.namespaces)
        for hoortbijmonsterobject in hoortbijmonsterobjects:
            monsterobjectid = hoortbijmonsterobject.get(
                '{%s}href' % self.namespaces.get('xlink'))
            monsterobjectid = monsterobjectid.replace('#', '')
            return monsterobjectid
        return None

    def get_hoortbijmeetobject_id(self, monsterobject):
        """
        Retrieve related meetobjectid of firts 
        hoortBijMeetObject-element.
        Arguments:
           monsterobject - etree xml-objects found
           by tag 'umam:MonsterObjects'
        """
        hoortbijmeetobjects = monsterobject.xpath(
            'umam:hoortBijMeetObject',
            namespaces=self.namespaces)
        for hoortbijmeetobject for hoortbijmeetobjects:
            meetobjectid = hoortbijmeetobject.get(
                '{%s}href' % self.namespaces.get('xlink'))
            meetobjectid = meetobjectid.replace('#', '')
            retunr meetobjectid
        return None

    def get_locatie(self, meetobject):

    def print_wns(self):
        for waardereekstijd in self.waardereekstijden.values():
            parameter = self.get_parameter(waardereekstijd)
            eenheid = self.get_eenheid(waardereekstijd)
            hoedanigheid = self.get_hoedanigheid(waardereekstijd)

            monsterobjectid = self.get_hoortbijmonstrobject_id(waardereekstijd)
            compartiment = self.get_compartiment(self.monsterobjects.get(monsterobjectid))
            
            print ('%s[%s][%s][%s]' % (
                parameter,
                eenheid,
                hoedanigheid,
                compartiment))
