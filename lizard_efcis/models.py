# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import datetime

from django.contrib.gis.db import models


class Status(models.Model):

    ST1 = "Change of interpretation do not use"
    ST2 = "Dubious taxon concept"
    ST3 = "Gepubliceerd"
    ST4 = "Non-taxonomic species group"
    ST5 = "Preferred name"
    ST6 = "Synonym"
    ST7 = "TWN error do not use"
    STATUS_LIST = [ST1, ST2, ST3, ST4, ST5, ST6, ST7]

    naam = models.CharField(unique=True, max_length=50)

    def __unicode__(self):
        return '{}'.format(self.naam)


class Meetnet(models.Model):
    net_oms = models.TextField(null=True, blank=True)


class StatusKRW(models.Model):

    code = models.CharField(max_length=5, unique=True)
    omschrijving = models.TextField(null=True, blank=True)
    datum_begin = models.DateField(null=True, blank=True)
    datum_eind = models.DateField(null=True, blank=True)
    datum_status = models.CharField(
        max_length=5,
        null=True,
        blank=True)

    def __unicode__(self):
        return '{}'.format(self.code)


class Watertype(models.Model):

    GROEP1 = "zout"
    GROEP2 = "zoet"

    GROEP_CHOICES = (
        (GROEP1, GROEP1),
        (GROEP2, GROEP2),
    )

    code = models.CharField(max_length=5, unique=True)
    omschrijving = models.TextField(null=True, blank=True)
    groep = models.CharField(max_length=10, choices=GROEP_CHOICES)
    datum_begin = models.DateField(null=True, blank=True)
    datum_eind = models.DateField(null=True, blank=True)
    datum_status = models.CharField(
        max_length=5,
        null=True,
        blank=True)

    def __unicode__(self):
        return '{}'.format(self.code)


class Waterlichaam(models.Model):

    wl_code = models.CharField(max_length=20)
    wl_naam = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    wl_type = models.CharField(
        max_length=10,
        null=True,
        blank=True)
    wl_oms = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=100,
        null=True,
        blank=True)

    def __unicode__(self):
        return '{}'.format(self.wl_code)


class Locatie(models.Model):

    loc_id = models.CharField(
        max_length=50,
        help_text="Locatiecode",
        unique=True)
    loc_oms = models.TextField(
        null=True,
        blank=True,
        help_text="Locatieomschrijving")
    geo_punt1 = models.PointField(srid=4326, null=True, blank=True)
    geo_punt2 = models.PointField(srid=4326, null=True, blank=True)
    waterlichaam = models.ForeignKey(
        Waterlichaam,
        blank=True,
        null=True)
    watertype = models.ForeignKey(
        Watertype,
        null=True,
        blank=True,
        help_text="KRW Watertype")
    status_krw = models.ForeignKey(
        StatusKRW,
        null=True,
        blank=True,
        help_text="Status KRW Watertype")
    meetnet = models.ForeignKey(Meetnet, null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return '{}'.format(self.loc_oms)

    def __str__(self):
        return self.loc_oms


class ParameterGroep(models.Model):

    code = models.CharField(
        unique=True,
        max_length=255
    )
    parent = models.ForeignKey(
        'lizard_efcis.ParameterGroep',
        null=True)

    def __unicode__(self):
        return self.code


class Parameter(models.Model):

    par_code = models.CharField(max_length=30)
    par_oms = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    casnummer = models.CharField(
        max_length=30, null=True, blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)
    parametergroep = models.ForeignKey(ParameterGroep, null=True)

    def __unicode__(self):
        return unicode(self.par_code)

    class Meta:
        ordering = ['par_code']


class Eenheid(models.Model):

    eenheid = models.CharField(max_length=20, unique=True)
    eenheid_oms = models.TextField(null=True, blank=True)
    dimensie = models.CharField(
        max_length=20,
        null=True,
        blank=True)
    omrekenfactor = models.FloatField(null=True, blank=True)
    eenheidgroep = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.eenheid)


class Hoedanigheid(models.Model):

    hoedanigheid = models.CharField(max_length=20, unique=True)
    hoed_oms = models.TextField(null=True, blank=True)
    hoedanigheidgroep = models.CharField(
        max_length=30,
        null=True,
        blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.hoedanigheid)


class Compartiment(models.Model):

    compartiment = models.CharField(max_length=20, unique=True)
    comp_oms = models.TextField(null=True, blank=True)
    compartimentgroep = models.CharField(
        max_length=30,
        null=True,
        blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.compartiment)


class Detectiegrens(models.Model):

    teken = models.CharField(max_length=5, unique=True)
    omschrijving = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.teken)


class Activiteit(models.Model):

    T0 = ""
    T1 = "Meting"
    T2 = "Toetsing"

    TYPE_CHOICES = (
        (T0, T0),
        (T1, T1),
        (T2, T2)
    )

    activiteit = models.CharField(max_length=50, unique=True)
    act_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=T1)
    uitvoerende = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    act_oms = models.TextField(null=True, blank=True)
    met_mafa = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    met_mafy = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    met_fyt = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    met_vis = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    met_fc = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    met_toets = models.CharField(
        max_length=255,
        null=True,
        blank=True)

    def __unicode__(self):
        return '{}'.format(self.activiteit)


class WNS(models.Model):

    wns_code = models.CharField(max_length=30, unique=True)
    wns_oms = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    parameter = models.ForeignKey(Parameter, null=True, blank=True)
    eenheid = models.ForeignKey(Eenheid, null=True, blank=True)
    hoedanigheid = models.ForeignKey(
        Hoedanigheid,
        null=True,
        blank=True)
    compartiment = models.ForeignKey(
        Compartiment,
        null=True,
        blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)

    def __unicode__(self):
        return '{}'.format(self.wns_code)

    def __str__(self):
        return self.wns_code


class Opname(models.Model):

    datum = models.DateField()
    tijd = models.TimeField(null=True, blank=True)
    waarde_n = models.FloatField(null=True, blank=True)
    waarde_a = models.CharField(
        max_length=30,
        null=True,
        blank=True)
    activiteit = models.ForeignKey(Activiteit)
    wns = models.ForeignKey(WNS)
    locatie = models.ForeignKey(Locatie)
    detect = models.ForeignKey(
        Detectiegrens,
        null=True,
        blank=True)

    class Meta:
        unique_together = ((
            'datum',
            'tijd',
            'wns',
            'locatie')
        )
        ordering = ['wns', 'locatie', 'datum', 'tijd']

    @property
    def moment(self):
        if self.tijd:
            return datetime.datetime(
                self.datum.year,
                self.datum.month,
                self.datum.day,
                self.tijd.hour,
                self.tijd.minute,
                self.tijd.second)
        else:
            return datetime.datetime(
                self.datum.year,
                self.datum.month,
                self.datum.day)


class ImportMapping(models.Model):

    tabellen = [
        ('Opname', 'Opname'),
        ('Locatie', 'Locatie'),
        ('ParameterGroep', 'ParameterGroep')
    ]
    code = models.CharField(max_length=50, unique=True)
    omschrijving = models.TextField(null=True, blank=True)
    tabel_naam = models.CharField(
        max_length=255,
        choices=tabellen,
        help_text="Import tabel")
    scheiding_teken = models.CharField(
        max_length=3,
        default=";",
        help_text="Veld scheidingsteken.")

    class Meta:
        ordering = ['tabel_naam']

    def __unicode__(self):
        return self.code


class MappingField(models.Model):

    FOREIGNKEY_MODELS = [
        'WNS',
        'Locatie',
        'Detectiegrens',
        'ParameterGroep'
    ]
    type_choices = [
        ('CharField', 'CharField'),
        ('float', 'float'),
        ('date', 'date'),
        ('time', 'time'),
        (FOREIGNKEY_MODELS[0], FOREIGNKEY_MODELS[0]),
        (FOREIGNKEY_MODELS[1], FOREIGNKEY_MODELS[1]),
        (FOREIGNKEY_MODELS[2], FOREIGNKEY_MODELS[2]),
        (FOREIGNKEY_MODELS[3], FOREIGNKEY_MODELS[3])
    ]

    db_field = models.CharField(max_length=255)
    file_field = models.CharField(max_length=255)
    db_datatype = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=type_choices,
        help_text='DataType of Foreign-Tabelnaam b.v. float, Locatie')
    foreignkey_field = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='{0} {1}'.format(
            'Veldnaam van de Foreign tabel, meestal id of code.',
            'Wordt gebruik in combinatie met foreign_key,'))
    mapping = models.ForeignKey(ImportMapping)
    data_format = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="b.v. %d-%m-%Y voor de datum.")

    def __unicode__(self):
        return '{0}-{1}'.format(self.db_field, self.file_field)

    class Meta:
        ordering = ['db_field']
