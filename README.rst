lizard-efcis
==========================================

The restframework app that contains the actual EFCIS data.


Note on 'meetnetten' hierarchy: it should be max 5 levels deep.




Sources
-----------------------------------------

Opname-list source::

    root url:

    /api

    opnames source:

    /api/opnames?locatie=NL14-20001&page=1&page_size=1000&start_date=1-1-2014&end_date=31-1-2014

    QUERY_PARAMS opname:
    locatie => location id, case-insensitive
    page => pagenumber
    page_size => items per page
    start_date => date from
    end_date => date to
    par_code => parameter code, case-insensitive

    parametergroeps:

    /api/parametergroeps/

    lines:

    /api/lines/

    locaties:

    api/locaties/?page=4&page_size=2

Import
----------------------------------------------

Create mappings for dataimports::

    $ bin/django create_mapping

Import domain data::

    $ bin/django import_domain_data

Import ibever data::

    $ bin/django import_ibever --mapping='iBever-opnames'
    $ bin/django import_hdsr_bio --mapping='hdsr-bio-opnames'
    
