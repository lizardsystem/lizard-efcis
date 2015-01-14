# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_hstore import hstore


ST0 = ""
ST1 = "Change of interpretation do not use"
ST2 = "Dubious taxon concept"
ST3 = "Gepubliceerd"
ST4 = "Non-taxonomic species group"
ST5 = "Preferred name"
ST6 = "Synonym"
ST7 = "TWN error do not use"

STATUS_CHOICES = (
    (ST0, ST0),
    (ST1, ST1),
    (ST2, ST2),
    (ST3, ST3),
    (ST4, ST4),
    (ST5, ST5),
    (ST6, ST6),
    (ST7, ST7)
)


class Parameter(models.Model):
    
    par_code = models.CharField(max_length=30)
    par_oms = models.CharField(
        max_length=255, 
        null=True, 
        blank=True)
    casnummer = models.CharField(
        max_length=30, null=True, blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        null=True,
        blank=True)
    
    def __unicode__(self):
        return unicode(self.par_code)

    class Meta:
        ordering = ['par_code']


class WNS(models.Model):
    
    wns_code = models.CharField(max_length=30)
    wns_oms = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    parameter = models.ForeignKey(Parameter, null=True, blank=True)
    eenheid = models.CharField(max_length=20, null=True, blank=True)
    hoedanigheid = models.CharField(
        max_length=20,
        null=True,
        blank=True)
    compartiment = models.CharField(
        max_length=10,
        null=True,
        blank=True)
    datum_status = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        null=True,
        blank=True)
    
