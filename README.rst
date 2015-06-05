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
    




[IMPORTANT] Necessary for Boxplot!
----------------------------------------------

First, as usual, update aptitude::

    $ sudo apt-get update

Then install pl/python and numpy::

    $ sudo apt-get install postgresql-plpython-9.3 python-numpy

Become user postgres::

    $ sudo su postgres

And create the language extension for our database::

    $ createlang plpythonu efcis_site

In postgres, create a new type 'boxplot_values'::

    DROP TYPE boxplot_values CASCADE;
    CREATE TYPE boxplot_values AS (
        min       numeric,
        q1        numeric,
        median    numeric,
        q3        numeric,
        max       numeric,
        p10       numeric,
        p90       numeric,
        mean      numeric
    );



Create a new boxplot function::

    CREATE OR REPLACE FUNCTION _final_boxplot(strarr numeric[])
       RETURNS boxplot_values AS
    $$
        import numpy as np
        x = strarr
        a = eval(str(x))
        
        a.sort()
        i = len(a)
        
        p10 = np.percentile(a, 10)
        p90 = np.percentile(a, 90)
        mean = np.mean(a)
        min = a[0]
        max = a[-1]
        #median = a[i/2]
        median = np.median(a)
        #q1 = a[i/4]
        #q3 = a[i*3/4]
        q1 = np.percentile(a, 25)
        q3 = np.percentile(a, 75)
        
        return (min, q1, median, q3, max, p10, p90, mean)
    $$
    LANGUAGE 'plpythonu' IMMUTABLE;

Create a boxplot aggregate::
    
    CREATE AGGREGATE boxplot(numeric) (
      SFUNC=array_append,
      STYPE=numeric[],
      FINALFUNC=_final_boxplot,
      INITCOND='{}'
    );


Example query::

    SELECT locatie_id,
              (boxplot(waarde_n::numeric)).*
       FROM lizard_efcis_opname
       WHERE waarde_n IS NOT NULL AND locatie_id=648
       GROUP BY locatie_id


To only fetch for summer::

    SELECT
        locatie_id,
        (boxplot(waarde_n::numeric)).*
    FROM 
        lizard_efcis_opname
    WHERE 
        waarde_n IS NOT NULL
    AND 
        EXTRACT(MONTH FROM DATE(datum)) > 4
    AND 
        EXTRACT(MONTH FROM DATE(datum)) < 10
    GROUP BY 
        locatie_id




For debugging, in '/etc/postgresql/9.3/main/postgresql.conf' set this to 'all'::

    log_statement = 'all'

And keep an eye on the postgres log::

    $ tail -f /var/log/postgresql/postgresql-9.3-main.log
        