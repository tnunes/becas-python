#!/usr/bin/env python

'''
becas-python - becas API client for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# Author: Tiago Nunes <tiago.nunes@ua.pt>
# Copyright: Copyright 2013, Tiago Nunes, Universidade de Aveiro
# License: Creative Commons Attribution + Noncommercial (cc-by-nc)


import sys
from distutils.core import setup


if sys.version_info < (2, 7):
    raise NotImplementedError('Sorry, you need Python 2.7 or '
                              'Python 3.x to use `becas-python`.')

try:
    import requests  # NOQA
except ImportError:
    print('`becas-python` requires `requests` to be installed.')
    sys.exit(1)

import becas


setup(name='becas',
      version=becas.__version__,
      description='becas API client for Python.',
      long_description=becas.__doc__,
      author=becas.__author__,
      author_email=becas.__email__,
      license=becas.__license__,
      url=becas.__url__,
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
