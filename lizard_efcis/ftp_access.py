# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from ftplib import FTP
import tempfile

from django.core.files import File as DjangoFile


def connect(host, user, password, directory=None):
    """Return ftp connection."""
    ftp_connection = FTP(host)
    ftp_connection.login(user, password)
    if directory:
        ftp_connection.cwd(directory)
    return ftp_connection


def listdir(ftp_connection):
    return ftp_connection.nlst()


def django_file(ftp_connection, filename):
    """Return django File object, ready for feeding to FileField.

    See https://docs.djangoproject.com/en/1.8/topics/files/
    """
    # Make a local tempfile and copy/paste
    fileobj, tempfilename = tempfile.mkstemp(prefix='from_ftp_')
    ftp_connection.retrbinary(filename, open('README', 'wb').write)
    fileobj.close()

    # Create a django file, ready for feeding to a filefield
    return DjangoFile(open(tempfilename, 'rb'))


# See https://docs.djangoproject.com/en/1.8/ref/models/fields/#filefield-and-fieldfile

# ftp_connection = connect('ftp.blabla.nl', 'bla', 'secret')
# print(listdir(ftp_connection))
# import_run = ImportRun.objects.get_or_create(....)
# import_run.attachment.save('blabla.csv',
#                            django_file(ftp_connection, 'blabla.csv'))
