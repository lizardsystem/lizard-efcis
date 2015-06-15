# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import os
from datetime import datetime

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.conf import settings

from lizard_efcis import utils


def get_attachment_path(instance, filename):
    dt = datetime.now()
    prefix = "{0}_{1}".format(
        dt.date().isoformat(),
        dt.time().isoformat()
    )
    return os.path.join(
        settings.UPLOAD_DIR,
        "{0}_{1}".format(prefix, filename))


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

    class Meta:
        ordering = ['naam'] 
        verbose_name = "status"
        verbose_name_plural = "statussen"

    def __unicode__(self):
        return self.naam


class Meetnet(models.Model):
    code = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True)

    class Meta:
        ordering = ['id']
        unique_together = (('code', 'parent'))
        verbose_name = "meetnet"
        verbose_name_plural = "meetnetten"

    @property
    def meetnet_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'children': self.children,
            'text': self.code
        }

    @property
    def children(self):
        """ Get recursive all children as dict. """
        children = Meetnet.objects.filter(parent=self)
        return [child.meetnet_dict for child in children]

    def __unicode__(self):
        return self.code


class StatusKRW(models.Model):

    code = models.CharField(max_length=50, unique=True)
    omschrijving = models.TextField(null=True, blank=True)
    datum_begin = models.DateField(null=True, blank=True)
    datum_eind = models.DateField(null=True, blank=True)
    datum_status = models.CharField(
        max_length=5,
        null=True,
        blank=True)

    class Meta:
        ordering = ['code']
        verbose_name = "KRW status"
        verbose_name_plural = "KRW statussen"

    def __unicode__(self):
        return self.code


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
        return self.code


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

    class Meta:
        ordering = ['wl_code']
        verbose_name = "waterlichaam"
        verbose_name_plural = "waterlichamen"

    def __unicode__(self):
        return self.wl_code


class Locatie(models.Model):

    loc_id = models.CharField(
        max_length=50,
        help_text="Locatiecode",
        unique=True)
    loc_oms = models.TextField(
        null=True,
        blank=True,
        help_text="Locatieomschrijving")
    x1 = models.FloatField(null=True, blank=True)
    y1 = models.FloatField(null=True, blank=True)
    x2 = models.FloatField(null=True, blank=True)
    y2 = models.FloatField(null=True, blank=True)
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
    meetnet = models.ManyToManyField(Meetnet, null=True, blank=True)
    status_fc = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    status_bio = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        if self.x1 is not None and self.y1 is not None:
            self.geo_punt1 = Point(
                utils.rd_to_wgs84(self.x1, self.y1))
        else:
            self.geo_punt1 = None

        if self.x2 is not None and self.y2 is not None:
            self.geo_punt2 = Point(
                utils.rd_to_wgs84(self.x2, self.y2))
        else:
            self.geo_punt2 = None

        super(Locatie, self).save(*args, **kwargs)

    class Meta:
        ordering = ['loc_id']
        verbose_name = "locatie"
        verbose_name_plural = "locaties"

    def __unicode__(self):
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

    @property
    def children_id_list(self):
        result = [self.id]
        children = ParameterGroep.objects.filter(parent=self)
        for child in children:
            result.append(child.parametergroep_dict['id'])
        return result

    @property
    def parametergroep_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'children': self.children,
            'text': self.code
        }

    @property
    def children(self):
        """ Get recursive all children as dict. """
        children = ParameterGroep.objects.filter(parent=self)
        results = []
        for child in children:
            results.append(child.parametergroep_dict)
        return results

    class Meta:
        ordering = ['code']
        verbose_name = "parametergroep"
        verbose_name_plural = "parametergroepen"


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
        return self.par_code

    class Meta:
        ordering = ['par_code']
        verbose_name = "parameter"
        verbose_name_plural = "parameters"


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
        return self.eenheid

    class Meta:
        ordering = ['eenheid']
        verbose_name = "eenheid"
        verbose_name_plural = "eenheden"


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
        return self.hoedanigheid

    class Meta:
        ordering = ['hoedanigheid']
        verbose_name = "hoedanigheid"
        verbose_name_plural = "hoedanigheden"


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
        return self.compartiment

    class Meta:
        ordering = ['compartiment']
        verbose_name = "compartiment"
        verbose_name_plural = "compartimenten"


class Detectiegrens(models.Model):

    teken = models.CharField(max_length=5, unique=True)
    omschrijving = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.teken

    class Meta:
        verbose_name = "detectiegrens"
        verbose_name_plural = "detectiegrenzen"


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
        return self.activiteit

    class Meta:
        ordering = ['activiteit']
        verbose_name = "activiteit"
        verbose_name_plural = "activiteit"


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
        return self.wns_code

    class Meta:
        verbose_name = "waarnemingssoort (WNS)"
        verbose_name_plural = "waarnemingssoorten (WNS)"


class Opname(models.Model):

    datum = models.DateField(
        db_index=True)
    tijd = models.TimeField(
        null=True,
        blank=True,
        db_index=True)
    waarde_n = models.FloatField(
        null=True,
        blank=True,
        db_index=True)
    waarde_a = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True)
    activiteit = models.ForeignKey(
        Activiteit,
        related_name='opnames')
    wns = models.ForeignKey(
        WNS,
        related_name='opnames',
        db_index=True)
    locatie = models.ForeignKey(
        Locatie,
        related_name='opnames',
        db_index=True)
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
        ordering = ['wns_id', 'locatie_id', 'datum', 'tijd']
        verbose_name = "opname"
        verbose_name_plural = "opnames"

    
class ImportMapping(models.Model):

    tabellen = [
        ('Opname', 'Opname'),
        ('Locatie', 'Locatie'),
        ('ParameterGroep', 'ParameterGroep'),
        ('Meetnet', 'Meetnet'),
        ('Activiteit', 'Activiteit')
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
        verbose_name = "importmapping"
        verbose_name_plural = "importmappings"

    def __unicode__(self):
        return self.code


class ImportRun(models.Model):
    AUTO = "Automatisch"
    MANUAL = "Handmatig"

    TYPE_CHOICES = (
        (AUTO, AUTO),
        (MANUAL, MANUAL)
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True)
    type_run = models.CharField(
        choices=TYPE_CHOICES,
        default=MANUAL,
        max_length=20)
    attachment = models.FileField(
        upload_to=settings.UPLOAD_DIR,
        blank=True,
        null=True)
    uploaded_by = models.CharField(
        max_length=200,
        blank=True)
    uploaded_date = models.DateTimeField(
        blank=True, 
        null=True)
    import_mapping = models.ForeignKey(
        ImportMapping,
        blank=True,
        null=True)
    action_log = models.TextField(
        null=True,
        blank=True)
    validated = models.BooleanField(default=False)
    imported = models.BooleanField(default=False)
    activiteit = models.ForeignKey(
        Activiteit,
        blank=True,
        null=True)

    def can_run_any_action(self):
        """Check fields of import_run."""
        can_run = True
        messages = []
        if not self.import_mapping:
            messages.append("geen mapping")
            can_run = False
        if not self.attachment:
            messages.append("geen bestand")
            can_run = False
        if self.attachment and not os.path.isfile(self.attachment.path):
            messages.append(
                "het bestand '%s' is niet "
                "aanwezig." % self.attachment.path)
            can_run = False
        if not self.activiteit:
            messages.append("geen activiteit")
            can_run = False
        return (can_run, messages)


class MappingField(models.Model):

    FOREIGNKEY_MODELS = [
        'WNS',
        'Locatie',
        'Detectiegrens',
        'ParameterGroep',
        'Meetnet',
        'StatusKRW',
        'Waterlichaam',
        'Watertype',
        'Activiteit'
    ]

    type_choices = [
        ('CharField', 'CharField'),
        ('float', 'float'),
        ('date', 'date'),
        ('time', 'time'),
    ] + [(foreignkey_model, foreignkey_model) for
         foreignkey_model in FOREIGNKEY_MODELS]

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
        verbose_name = "mappingveld"
        verbose_name_plural = "mappingvelden"
