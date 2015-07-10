# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from itertools import groupby
import datetime

from django.contrib import messages
import numpy as np

from lizard_efcis.manager import VALIDATED
from lizard_efcis.manager import UNRELIABLE
from lizard_efcis.models import Opname


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
        raise NotImplementedError


class MinMaxValidator(BaseValidator):

    def find_min_max(self, wns):
        """Return min, max tuple for the WNS."""
        return (wns.validate_min, wns.validate_max)


class StandardDeviationValidator(BaseValidator):

    def __init__(self, modeladmin, request, queryset, period_to_look_back):
        super(StandardDeviationValidator, self).__init__(
            modeladmin, request, queryset)
        self.period_to_look_back = period_to_look_back
        # period_to_look_back: number of days back we should look at values.

    def find_min_max(self, wns):
        """Return min, max tuple for the WNS."""
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=self.period_to_look_back)
        opnames_to_look_at = Opname.objects.filter(wns=wns,
                                                   validation_state=VALIDATED,
                                                   datum__gte=start_date)
        values = opnames_to_look_at.values_list('waarde_n', flat=True)
        values = [value for value in values if value is not None]
        mean = np.mean(values)
        standard_deviation = np.std(values)
        return (mean - standard_deviation, mean + standard_deviation)
