#!/usr/bin/env python

'''
becas-python - becas API client for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**becas-python** is the official Python client for the becas API.

**becas** is a biomedical concept annotator available through an HTTP API.

This package allows usage of the becas API from a command-line tool or
programatically from Python modules.

:copyright: (c) 2013, Tiago Nunes, Universidade de Aveiro
:license: Creative Commons Attribution-Noncommercial


Resources
^^^^^^^^^

* `Documentation <http://tnunes.github.io/becas-python/>`_
* `Issue Tracker <http://github.com/tnunes/becas-python/issues>`_
* `Code <http://github.com/tnunes/becas-python>`_
* `becas API documentation <http://bioinformatics.ua.pt/becas/api>`_
* `About becas <http://bioinformatics.ua.pt/becas/about>`_

'''


import sys
from distutils.core import setup


if sys.version_info < (2, 7):
    raise NotImplementedError('Sorry, you need Python 2.7 or '
                              'Python 3.x to use `becas-python`.')


setup(name='becas',
      version='1.0.1',
      description='becas API client for Python.',
      long_description=__doc__,
      author='Tiago Nunes',
      author_email='tiago.nunes@ua.pt',
      license='CC-BY-NC',
      url='http://tnunes.github.io/becas-python/',
      install_requires=['requests'],
      py_modules=['becas'],
      scripts=['becas.py'],
      platforms='any',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3'],
      )
