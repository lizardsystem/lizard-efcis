# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib import admin

from lizard_efcis import models


class MappingFieldInlineAdmin(admin.TabularInline):
    model = models.MappingField
    # list_display = ['mapping']


class ImportMappingAdmin(admin.ModelAdmin):
    inlines = [MappingFieldInlineAdmin]


admin.site.register(models.ImportMapping, ImportMappingAdmin)
admin.site.register(models.Locatie)
