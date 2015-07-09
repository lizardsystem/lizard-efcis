from setuptools import setup

version = '0.2.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'Markdown',
    'celery',
    'django-celery',
    'django-compressor',
    'django-extensions',
    'django-hstore',
    'django-nose',
    'django-tls',
    'djangorestframework >= 3.0.4',
    'djangorestframework-gis >= 0.8',
    'gunicorn',
    #'lxml',
    'numpy',
    'pyproj',
    'python-memcached',
    'raven',
    'south',
    'werkzeug',
    # Maptree and wms are included for demo purposes; almost every site needs
    # them anyway.
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='lizard-efcis',
      version=version,
      description="Lizard application for Ecological"
                  " and Physico-Chemical data.",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Alexandr Seleznev',
      author_email='alexandr.seleznev@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_efcis'],
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
