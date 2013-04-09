Command-line interface
======================

This page contains the command-line interface documentation of **becas-python**
that allows you to use the becas API from a command-line tool.

For instructions on how to use the becas API programmatically from your Python
modules, read the :doc:`becas.py`.

Comprehensive documentation about the becas API is available at its dedicated
`page <http://bioinformatics.ua.pt/becas/api>`_.


Available commands
~~~~~~~~~~~~~~~~~~

Assuming you have already installed **becas-python**, running ``becas.py -h``
should print the following help message::

	$ becas.py -h
	usage: becas.py [-h]
	                
	                {annotate-text,export-text,annotate-publication,export-publication}
	                ...

	Annotate text or PubMed publications using the becas API.

	positional arguments:
	  {annotate-text,export-text,annotate-publication,export-publication}
	    annotate-text       annotate text as JSON with concept metadata
	    export-text         export text in a chosen format
	    annotate-publication
	                        annotate PubMed publication as JSON with concept
	                        metadata
	    export-publication  export PubMed publication in MEDLINE IeXML

	optional arguments:
	  -h, --help            show this help message and exit

As you can see, all methods exposed by the API are available as commands:

* annotate-text
* export-text
* annotate-publication
* export-publication


Authentication parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

You are required to authenticate in order to use the `becas API`_. This can be
done through the ``--email`` and ``--tool`` parameters. Only the `email`
parameter is mandatory. If you ommit the `tool` parameter, it defaults to
becas-python.


Optional parameters
~~~~~~~~~~~~~~~~~~~

All commands accept the following optional arguments::

	optional arguments:
	  -h, --help            show this help message and exit
	  -g GROUPS, --groups GROUPS
	                        semantic groups to use for annotation as a comma
	                        separated list (e.g. PRGE,DISO,ANAT). Available
	                        groups: (SPEC, ANAT, DISO, PATH, CHED, ENZY, MRNA,
	                        PRGE, COMP, FUNC, PROC)
	  -o FILE, --output-file FILE
	                        file to save annotation results to
	  --secure              access the service securely through HTTPS
	  --timeout TIMEOUT     seconds to wait before timing out a request


If you ommit the ``--groups`` parameter, all semantic groups will be
used for annotation.

By default, annotation results are printed to STDOUT. You can use the
``--output-file`` parameter to save results to a file.


Using the tool
~~~~~~~~~~~~~~

You can use the command-line tool to automatically annotate text and PubMed
publications with biomedical concepts.

Text annotation
^^^^^^^^^^^^^^^

The **text annotation endpoint** of the API is available through the
``annotate-text`` command::

	$ becas.py annotate-text -h
	usage: becas.py annotate-text [-h] --email EMAIL [--tool TOOL]
	                              (-f FILE | -t TEXT | -i) [-g GROUPS] [-o FILE]
	                              [--secure] [--timeout TIMEOUT]

	Annotate text with biomedical concepts using the becas API.

	optional arguments:
	  -h, --help            show this help message and exit
	  -g GROUPS, --groups GROUPS
	                        semantic groups to use for annotation as a comma
	                        separated list (e.g. PRGE,DISO,ANAT). Available
	                        groups: (SPEC, ANAT, DISO, PATH, CHED, ENZY, MRNA,
	                        PRGE, COMP, FUNC, PROC)
	  -o FILE, --output-file FILE
	                        file to save annotation results to
	  --secure              access the service securely through HTTPS
	  --timeout TIMEOUT     seconds to wait before timing out a request

	client authentication:
	  --email EMAIL         Email address to use in API authentication
	  --tool TOOL           Tool name to use in API authentication (default:
	                        becas-python)

	input selection:
	  -f FILE, --file FILE  text file to annotate
	  -t TEXT, --text TEXT  plain text to annotate
	  -i, --stdin           read text from STDIN

Input text can be piped in through STDIN, specified directly in the
command-line or read from a text file.

For example, to annotate a text file with biomedical concepts and save
JSON results to another file you could do::

	$ becas.py annotate-text --email "you@example.com" \
	                         -f my_text_file.txt -o my_annotations.json



The **text export endpoint** of the API, which allows you to export results
in JSON, XML, A1 or CoNLL, is available through the ``export-text`` command::

	$ becas.py export-text -h
	usage: becas.py export-text [-h] --email EMAIL [--tool TOOL]
	                            (-f FILE | -t TEXT | -i) --format
	                            {json,xml,a1,conll} [-g GROUPS] [-o FILE]
	                            [--secure] [--timeout TIMEOUT]

	Export text annotated with biomedical concepts in a chosen format using the
	becas API.

	optional arguments:
	  -h, --help            show this help message and exit
	  -g GROUPS, --groups GROUPS
	                        semantic groups to use for annotation as a comma
	                        separated list (e.g. PRGE,DISO,ANAT). Available
	                        groups: (SPEC, ANAT, DISO, PATH, CHED, ENZY, MRNA,
	                        PRGE, COMP, FUNC, PROC)
	  -o FILE, --output-file FILE
	                        file to save annotation results to
	  --secure              access the service securely through HTTPS
	  --timeout TIMEOUT     seconds to wait before timing out a request

	client authentication:
	  --email EMAIL         Email address to use in API authentication
	  --tool TOOL           Tool name to use in API authentication (default:
	                        becas-python)

	input selection:
	  -f FILE, --file FILE  text file to annotate
	  -t TEXT, --text TEXT  plain text to annotate
	  -i, --stdin           read text from STDIN

	output selection:
	  --format {json,xml,a1,conll}
	                        output format

You can, for example, easily export standoff annotation in A1 format using
a command similar to::

	$ becas.py export-text --email "you@example.com" \
	                       --format a1 -f my_text_file.txt -o my_annotations.a1

Abstract annotation
^^^^^^^^^^^^^^^^^^^

The **abstract annotation endpoint** of the API is exposed by the
``annotate-publication`` command::

	$ becas.py annotate-publication -h
	usage: becas.py annotate-publication [-h] --email EMAIL [--tool TOOL] -p PMID
	                                     [-g GROUPS] [-o FILE] [--secure]
	                                     [--timeout TIMEOUT]

	Annotate PubMed publications with biomedical concepts using the becas API.

	optional arguments:
	  -h, --help            show this help message and exit
	  -g GROUPS, --groups GROUPS
	                        semantic groups to use for annotation as a comma
	                        separated list (e.g. PRGE,DISO,ANAT). Available
	                        groups: (SPEC, ANAT, DISO, PATH, CHED, ENZY, MRNA,
	                        PRGE, COMP, FUNC, PROC)
	  -o FILE, --output-file FILE
	                        file to save annotation results to
	  --secure              access the service securely through HTTPS
	  --timeout TIMEOUT     seconds to wait before timing out a request

	client authentication:
	  --email EMAIL         Email address to use in API authentication
	  --tool TOOL           Tool name to use in API authentication (default:
	                        becas-python)

	input selection:
	  -p PMID, --pmid PMID  PMID of publication to annotate

To annotate a publication and save results as JSON you would do::

	$ becas.py annotate-publication --email "you@example.com" \
	                                --pmid 23225384 -o 23225384.json



The **abstract export endpoint** of the API, allowing export of annotated
publications in MEDLINE IeXML format, is reachable through the
``export-publication`` command::

	$ becas.py export-publication -h
	usage: becas.py export-publication [-h] --email EMAIL [--tool TOOL] -p PMID
	                                   [-g GROUPS] [-o FILE] [--secure]
	                                   [--timeout TIMEOUT]

	Export PubMed publications annotated with biomedical concepts using the becas
	API.

	optional arguments:
	  -h, --help            show this help message and exit
	  -g GROUPS, --groups GROUPS
	                        semantic groups to use for annotation as a comma
	                        separated list (e.g. PRGE,DISO,ANAT). Available
	                        groups: (SPEC, ANAT, DISO, PATH, CHED, ENZY, MRNA,
	                        PRGE, COMP, FUNC, PROC)
	  -o FILE, --output-file FILE
	                        file to save annotation results to
	  --secure              access the service securely through HTTPS
	  --timeout TIMEOUT     seconds to wait before timing out a request

	client authentication:
	  --email EMAIL         Email address to use in API authentication
	  --tool TOOL           Tool name to use in API authentication (default:
	                        becas-python)

	input selection:
	  -p PMID, --pmid PMID  PMID of publication to annotate

You can export an annotated document using a command like::

	$ becas.py export-publication --email "you@example.com" \
	                              --pmid 23225384 -o 23225384.xml


----------

If you need to use becas functionality programmatically from Python code,
take a look at the :doc:`becas.py`.


.. _becas API: http://bioinformatics.ua.pt/becas/api
