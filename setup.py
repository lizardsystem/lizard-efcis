from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-celery',
    'django-compressor',
    'django-extensions',
    'django-nose',
    'gunicorn',
    'python-memcached',
    'raven',
    'south',
    'werkzeug',
    'djangorestframework',
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
      description="Lizard application for Ecological and Physico-Chemical data.",
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
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
