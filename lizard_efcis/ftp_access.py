# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from ftplib import FTP
import tempfile

from django.core.files import File as DjangoFile

from lizard_efcis.models import FTPLocation

DIR_IMPORTED_CORRECTLY = 'VERWERKT'


def connect(ftp_location):
    """Return ftp connection."""
    ftp_connection = FTP(ftp_location.hostname)
    ftp_connection.login(ftp_location.username, ftp_location.password)
    if ftp_location.directory:
        ftp_connection.cwd(ftp_location.directory)
    return ftp_connection


def listdir(ftp_connection):
    return sorted(ftp_connection.nlst())


def importable_filenames(ftp_connection):
    # Idea: separate retryable_filenames for those with an attached error
    # report?
    filenames = listdir(ftp_connection)
    return [filename for filename in filenames
            if filename.startswith('iBever_')
            and filename.endswith('.txt')]


def django_file(ftp_connection, filename):
    """Return django File object, ready for feeding to FileField.

    See https://docs.djangoproject.com/en/1.8/topics/files/
    """
    # Make a local tempfile and copy/paste
    fileobj, tempfilename = tempfile.mkstemp(prefix='from_ftp_',
                                             suffix='.csv')
    ftp_connection.retrbinary(filename, open('README', 'wb').write)
    fileobj.close()

    # Create a django file, ready for feeding to a filefield
    return DjangoFile(open(tempfilename, 'rb'))


def debug_info(ftp_location):
    """Return string with information about the FTP connection."""
    output = []
    output.append("Looking at %s" % ftp_location)
    ftp_connection = connect(ftp_location)
    output.append("Directory contents:")
    for filename in listdir(ftp_connection):
        output.append("    - %s" % filename)
    output.append("Importable csv files:")
    for filename in importable_filenames(ftp_connection):
        output.append("    - %s" % filename)

    return '\n'.join(output)


# See https://docs.djangoproject.com/en/1.8/ref/models/fields/#filefield-and-fieldfile

# ftp_connection = connect('ftp.blabla.nl', 'bla', 'secret')
# print(listdir(ftp_connection))
# import_run = ImportRun.objects.get_or_create(....)
# import_run.attachment.save('blabla.csv',
#                            django_file(ftp_connection, 'blabla.csv'))
