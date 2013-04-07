==============================
becas-python: becas API client
==============================

**becas-python** is the official `becas`_ API client for Python.

`becas`_ *is a biomedical concept annotator available through an* `HTTP API`_.
*It identifies  biomedical concepts in text and PubMed
publications. You can learn more about becas in its* `about page`_.


.. _installation:

Installation
------------

Using pip
^^^^^^^^^

The preferred method of installation is through ``pip``, and you are
encouraged to use a virtualenv::

	$ pip install becas

The only hard dependency, `requests`_, will be automatically installed.

Using easy_install
^^^^^^^^^^^^^^^^^^

If you really must, and you probably *don't*, you can also use ``easy_install``::

	$ easy_install becas

Manually
^^^^^^^^

In case you want to install manually, you can either:

* `Download`_ or clone the `GitHub repository`_, ``cd`` into it and run::

	$ python setup.py install

**__or__**

* Download `becas.py`_ and place it in your project folder.


If you install manually, you should install `requests`_ on your own.


Usage
-----

**becas-python** can be used programatically or through a command-line interface.


Command-line interface
^^^^^^^^^^^^^^^^^^^^^^

To use becas as a command-line tool check the :doc:`cli` documentation.

.. toctree::

   cli


Programatically
^^^^^^^^^^^^^^^

Learn how to use becas from your Python programs in the :doc:`becas.py`:

.. toctree::

   becas.py


License
-------

Both **becas-python** and **becas** are free to use under the `Creative Commons
Attribution-NonCommercial license`_.


.. _becas: http://bioinformatics.ua.pt/becas/
.. _about page: http://bioinformatics.ua.pt/becas/about
.. _HTTP API: http://bioinformatics.ua.pt/becas/api
.. _requests: http://python-requests.org
.. _Download: http://github.com/tnunes/becas-python/archive/master.zip
.. _GitHub repository: http://github.com/tnunes/becas-python
.. _becas.py: http://raw.github.com/tnunes/becas-python/master/becas.py
.. _Creative Commons Attribution-NonCommercial license: http://creativecommons.org/licenses/by-nc/3.0/
