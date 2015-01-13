# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_hstore import hstore


class Status(models.Model):

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']


class Parameter(models.Model):

    code = models.CharField(max_length=30)
    description = models.CharField(max_length=255, null=True, blank=True)
    cas_number = models.CarField(max_length=30, null=True, blank=True)
    date_status = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)
    
    
    
