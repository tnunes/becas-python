becas.py module documentation
=============================

This page contains the API documentation for **becas.py**, the single module
packaged by **becas-python** that allows you to use the becas API
programatically from your Python modules.

For instructions on how to use the becas API from a command-line tool, read
the :doc:`cli` documentation.

Comprehensive documentation about the becas API is available at its dedicated
`page <http://bioinformatics.ua.pt/becas/api>`_.


Required configuration
~~~~~~~~~~~~~~~~~~~~~~

You are required to authenticate in order to use the `becas API`_. This can be
done through the ``email`` and ``tool`` parameters, which you should set before
invoking any of the annotation functions::

  import becas
  becas.email = 'you@example.com'  # required
  becas.tool = 'your-tool-name'    # optional, defaults to 'becas-python'


Configuration parameters
~~~~~~~~~~~~~~~~~~~~~~~~

You can set these parameters from your modules to configure **becas-python**
behaviour.

.. autodata:: becas.timeout
.. autodata:: becas.secure


Constants
~~~~~~~~~

These constants are provided for your reference.

.. autodata:: becas.SEMANTIC_GROUPS
.. autodata:: becas.EXPORT_FORMATS


Functions
~~~~~~~~~

The following API client functions are available. Read more about the available
API methods in the `becas API calls reference`_.

Text annotation
^^^^^^^^^^^^^^^

.. autofunction:: becas.annotate_text
.. autofunction:: becas.export_text

Abstract annotation
^^^^^^^^^^^^^^^^^^^

.. autofunction:: becas.annotate_publication
.. autofunction:: becas.export_publication

Exceptions
~~~~~~~~~~

If something goes wrong, one of these exceptions will be raised.

.. autoexception:: becas.BecasException
   :show-inheritance:
.. autoexception:: becas.AuthenticationRequired
   :show-inheritance:
.. autoexception:: becas.InvalidGroups
   :show-inheritance:
.. autoexception:: becas.InvalidFormat
   :show-inheritance:
.. autoexception:: becas.TooMuchText
   :show-inheritance:
.. autoexception:: becas.TooManyRequests
   :show-inheritance:
.. autoexception:: becas.PublicationNotFound
   :show-inheritance:
.. autoexception:: becas.ServiceUnavailable
   :show-inheritance:
.. autoexception:: becas.ConnectionError
   :show-inheritance:
.. autoexception:: becas.SSLError
   :show-inheritance:
.. autoexception:: becas.Timeout
   :show-inheritance:

----------

This documentation was automatically generated from the `source code`_
using `sphinx`_.

**becas.py** is a rather small module. You can read the annotated source at
`GitHub`_.


.. _source code: http://github.com/tnunes/becas-python/blob/master/becas.py
.. _sphinx: http://sphinx-doc.org/
.. _becas API: http://bioinformatics.ua.pt/becas/api
.. _becas API calls reference: http://bioinformatics.ua.pt/becas/#api__api_calls
.. _GitHub: http://github.com/tnunes/becas-python/blob/master/becas.py
