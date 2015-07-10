# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from itertools import groupby

from django.contrib import messages

from lizard_efcis.manager import VALIDATED
from lizard_efcis.manager import UNRELIABLE


class BaseValidator(object):

    def __init__(self, modeladmin, request, queryset):
        self.modeladmin = modeladmin
        self.request = request
        self.queryset = queryset
        self.n_textual_opnames = 0
        self.n_validated = 0
        self.n_unreliable = 0

    def validate(self):
        """Actual validation method you need to call from the admin."""
        selected_opnames = list(self.queryset.order_by('wns'))

        def _key(opname):
            return opname.wns

        for wns, opnames in groupby(selected_opnames, _key):
            minimum, maximum = self.find_min_max(wns)
            if minimum is None or maximum is None:
                messages.warning(self.request,
                                 "Min/Max niet ingesteld voor %s" % wns)
                continue
            for opname in opnames:
                if opname.waarde_n is None:
                    self.n_textual_opnames += 1
                    continue
                if minimum <= opname.waarde_n <= maximum:
                    opname.validation_state = VALIDATED
                    opname.save()
                    self.n_validated += 1
                else:
                    opname.validation_state = UNRELIABLE
                    opname.save()
                    self.n_unreliable += 1

        if self.n_validated:
            messages.success(self.request,
                             "%s zijn valide" % self.n_validated)
        if self.n_unreliable:
            messages.error(self.request,
                           "%s zijn onbetrouwbaar" % self.n_unreliable)
        if self.n_textual_opnames:
            messages.warning(self.request,
                             "%s zijn niet numeriek" % self.n_textual_opnames)

    def find_min_max(self, wns):
        """Return min, max tuple for the WNS."""
        return (0, 0)


class MinMaxValidator(BaseValidator):

    def find_min_max(self, wns):
        """Return min, max tuple for the WNS."""
        return (wns.validate_min, wns.validate_max)
