# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt
# -*- coding: utf-8 -*-
from django.db.models.manager import Manager
from tls import request

# Validation states. They're not in models.py to prevent circular imports.
VALIDATED = 1
VALIDATED_HIDDEN = 2
UNRELIABLE = 3
NOT_VALIDATED = 4
VALIDATION_CHOICES = (
    (VALIDATED, "Gevalideerd"),
    (VALIDATED_HIDDEN, "Gevalideerd - niet tonen"),
    (UNRELIABLE, "Onbetrouwbaar"),
    (NOT_VALIDATED, "Niet gevalideerd"))


def should_filter_opnames():
    """Return whether we should filter opnames on validation state."""
    try:
        user = request.user
    except RuntimeError:
        # We don't have a local request object.
        return
    if user is not None and user.is_staff:
        # Everyone with staff status can be assumed to be a maintainer. We
        # don't need to filter out opnames for them.
        return
    return True


class FilteredOpnamesManager(Manager):
    """Object manager that filters out not-validated opnames.

    Maintainers of the site can still see the opnames in other states, though.

    Quick assumption: everyone with staff status is a maintainer.

    """
    use_for_related_fields = True

    def get_queryset(self):
        """Return base queryset, but filtered for validation state.
        """
        queryset = super(FilteredOpnamesManager, self).get_queryset()
        if should_filter_opnames():
            return queryset.filter(validation_state=VALIDATED)
        else:
            return queryset
