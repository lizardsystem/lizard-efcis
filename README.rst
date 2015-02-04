lizard-efcis
==========================================

Introduction

Usage, etc.


Post-nensskel project setup TODO
--------------------------------

Here are some instructions on what to do after you've created the project with
nensskel.

- Fill in a short description on https://github.com/nens/lizard-efcis if you
  haven't done so already.

- Use the same description in the ``setup.py``'s "description" field.

- Fill in your username and email address in the ``setup.py``, see the
  ``TODO`` fields.

- Check https://github.com/nens/lizard-efcis/settings/collaboration if the teams
  "Nelen & Schuurmans" and "Nelen & Schuurmans pull only" have access.

- Add a new jenkins job at
  http://buildbot.lizardsystem.nl/jenkins/view/sites/newJob. Job name should
  be "lizard-efcis", make the project a copy of the existing "wro" (for
  instance) project. On the next page, change the "github project" to
  ``https://github.com/nens/lizard-efcis/`` and
  "repository url" fields to ``git@github.com:nens/lizard-efcis.git``. The rest
  of the settings should be OK.

- The project is prepared to be translated with Lizard's
  `Transifex <http://translations.lizard.net/>`_ server. For details about
  pushing translation files to and fetching translation files from the
  Transifex server, see the ``nens/translations`` `documentation
  <https://github.com/nens/translations/blob/master/README.rst>`_.

Later on, before releasing the site, adjust ``fabfile.cfg`` to point at the
correct server and configure raven/sentry and gaug.es in the django settings.


Initial setup
--------------------------------

Initially, there's no ``buildout.cfg``. You need to make that a symlink to the
correct configuration. On your development machine, that is
``development.cfg`` (and ``staging.cfg`` or ``production.cfg``, for instance
on the server)::

    $ ln -s development.cfg buildout.cfg

Then run bootstrap and buildout, as usual::

    $ python bootstrap.py
    $ bin/buildout

Set up a database (and yes, set up an admin user when asked)::
    
    $ bin/django dbshell
      => CREATE extention hstore;
    $ bin/django syncdb
    $ bin/django migrate

And import two fixtures. The background_maps sets up a couple of lizard-map
defaults. Democontent gives you an initial homepage and a link to an example
WMS layer::

    $ bin/django loaddata background_maps
    $ bin/django loaddata democontent

Start the server::

    $ bin/django runserver

SOURCES
-----------------------------------------

Opname-list source:

    /api/opnames?locatie=NL14-20001&page=1&page_size=1000&startdatetime=1-1-2014T12:00:00&enddatetime=31-1-2014T00:00:00


Import
----------------------------------------------

Import doamain data::

    $ bin/django import_domain_data

Import ibever data::

    $ bin/django import_ibever

