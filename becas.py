#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

__title__ = 'becas'
__version__ = '1.0'
__author__ = 'Tiago Nunes'
__license__ = 'CC-BY-NC'
__copyright__ = 'Copyright 2013, Tiago Nunes, Universidade de Aveiro'
__url__ = 'http://tnunes.github.io/becas-python/'

__maintainer__ = 'Tiago Nunes'
__email__ = 'tiago.nunes@ua.pt'


__all__ = ('email', 'tool', 'timeout', 'secure',
           'SEMANTIC_GROUPS', 'EXPORT_FORMATS',
           'annotate_text', 'export_text',
           'annotate_publication', 'export_publication',
           'BecasException', 'AuthenticationRequired', 'InvalidGroups',
           'InvalidFormat', 'TooMuchText', 'TooManyRequests',
           'PublicationNotFound', 'ServiceUnavailable',
           'ConnectionError', 'SSLError', 'Timeout',)


import sys
import time
import json
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote  # NOQA

import requests  # urllib2 sucks badly, we depend on requests


# -- Configuration parameters - you can set these from your modules -----------
#: becas API authentication ``email`` parameter
email = None
#: becas API authentication ``tool`` parameter
tool = 'becas-python'

#: Seconds to wait before timing out a request
timeout = 120
#: Whether to use HTTPS or plain HTTP
secure = False


# -- Internal constants - do not touch these ----------------------------------
#: Semantic groups usable as keys of a ``groups`` :class:`dict`
SEMANTIC_GROUPS = ('SPEC', 'ANAT', 'DISO', 'PATH', 'CHED', 'ENZY',
                   'MRNA', 'PRGE', 'COMP', 'FUNC', 'PROC',)
#: Output formats available for the :func:`export_text` function
EXPORT_FORMATS = ('json', 'xml', 'a1', 'conll',)

ENDPOINTS_PREFIX = 'bioinformatics.ua.pt/becas/api/'
TEXT_ANNOTATE_ENDPOINT = ENDPOINTS_PREFIX + 'text/annotate'
TEXT_EXPORT_ENDPOINT = ENDPOINTS_PREFIX + 'text/export'
PUBMED_ANNOTATE_ENDPOINT = ENDPOINTS_PREFIX + 'pubmed/annotate/'  # + PMID
PUBMED_EXPORT_ENDPOINT = ENDPOINTS_PREFIX + 'pubmed/export/'  # + PMID

DEFAULT_HEADERS = {
    'User-Agent': 'becas-python/%s %s' % (
        __version__, requests.utils.default_user_agent()),
    'Content-Type': 'application/json',
}


# -- Exceptions ---------------------------------------------------------------
class BecasException(RuntimeError):
    '''There was an ambiguous exception that occurred while handling your
    request.'''


class AuthenticationRequired(BecasException):
    '''You need to authenticate your requests with your email and optionally a
    tool name.

    As an example, if your email address is you@example.com, you can specify it
    as follows::

      >>> import becas
      >>> becas.email = 'you@example.com'

    In case of excessive usage of the becas API, UA.PT Bioinformatics will
    attempt to contact a user at the email address provided before blocking
    access to the services.
    '''


class InvalidGroups(BecasException, ValueError):
    '''You provided an invalid groups dictionary.'''


class InvalidFormat(BecasException, ValueError):
    '''You provided an invalid export format.'''


class TooMuchText(BecasException, ValueError):
    '''You provided too much text to annotate. Try again with less text.'''


class TooManyRequests(BecasException):
    '''You performed too many requests in a short amount of time. Wait ``wait``
    seconds before trying again.'''

    def __init__(self, wait):
        self.wait = wait


class PublicationNotFound(BecasException, ValueError):
    '''The publication you requested was not found in PubMed.'''


class ServiceUnavailable(BecasException):
    '''The annotation service is currently unavailable.'''


class Timeout(BecasException):
    '''The request timed out.'''


class ConnectionError(BecasException):
    '''A Connection error occurred.'''


class SSLError(ConnectionError):
    '''An SSL error occurred.'''


# -- API methods --------------------------------------------------------------
def annotate_text(text, groups=None, echo=False):
    '''Annotate text with biomedical concepts.

    :param text: text to annotate (:class:`str` or :class:`unicode`).
    :param groups: *optional* :class:`dict` of concept groups to identity.
    :param echo: *optional* flag to return ``text`` in the response.

    :return: :class:`dict` with annotation results.

    Usage::

      >>> import becas
      >>> becas.email = 'you@example.com'
      >>> results = becas.annotate_text('BRCA1 is a human caretaker gene.')

    '''

    validate_text(text)
    payload = {'text': text}
    if groups:
        validate_groups(groups)
        payload['groups'] = groups
    if echo:
        payload['echo'] = True
    validate_authentication()

    endpoint = endpoint_url('annotate_text')
    response = do_request(endpoint, payload)

    return response.json()


def export_text(text, format, groups=None):
    '''Export text annotated with biomedical concepts in JSON, XML, A1 or
    CONLL.

    :param text: text to annotate (:class:`str` or :class:`unicode`).
    :param format: output format (one of 'json', 'xml', 'a1' or 'conll').
    :param groups: *optional* :class:`dict` of concept groups to identity.

    :return: :class:`unicode` string with annotation results.

    Usage::

      >>> import becas
      >>> becas.email = 'you@example.com'
      >>> text = 'BRCA1 is a human caretaker gene.'
      >>> json_results = becas.export_text(text, 'json')
      >>> iexml_results = becas.export_text(text, 'xml')
      >>> a1_results = becas.export_text(text, 'a1')
      >>> conll_results = becas.export_text(text, 'conll')

    '''

    validate_text(text)
    validate_format(format)
    payload = {'text': text, 'format': format}
    if groups:
        validate_groups(groups)
        payload['groups'] = groups
    validate_authentication()

    endpoint = endpoint_url('export_text')
    response = do_request(endpoint, payload)

    return response.text


def annotate_publication(pmid, groups=None):
    '''Annotate PubMed publication with biomedical concepts.

    :param pmid: PMID of publication to annotate.
    :param groups: *optional* :class:`dict` of concept groups to identity.

    :return: :class:`dict` with annotation results.

    Usage::

      >>> import becas
      >>> becas.email = 'you@example.com'
      >>> results = becas.annotate_publication(23225384)

    '''

    validate_pmid(pmid)
    payload = {}
    if groups:
        validate_groups(groups)
        payload['groups'] = groups
    validate_authentication()

    endpoint = endpoint_url('annotate_publication', pmid=pmid)
    response = do_request(endpoint, payload)

    return response.json()


def export_publication(pmid, groups=None):
    '''Export PubMed publication as MEDLINE IeXML annotated with
    biomedical concepts.

    :param pmid: PMID of publication to annotate.
    :param groups: *optional* :class:`dict` of concept groups to identity.

    :return: :class:`unicode` string with IeXML annotation results.

    Usage::

      >>> import becas
      >>> becas.email = 'you@example.com'
      >>> results = becas.export_publication(23225384)

    '''

    validate_pmid(pmid)
    payload = {}
    if groups:
        validate_groups(groups)
        payload['groups'] = groups
    validate_authentication()

    endpoint = endpoint_url('export_publication', pmid=pmid)
    response = do_request(endpoint, payload)

    return response.text


# -- Helpers ------------------------------------------------------------------
def endpoint_url(endpoint, pmid=None):
    '''Return service URL for given endpoint.'''

    scheme = 'https://' if secure else 'http://'
    auth = '?tool=' + quote(tool) + '&email=' + quote(email)
    if endpoint == 'annotate_text':
        return scheme + TEXT_ANNOTATE_ENDPOINT + auth
    if endpoint == 'export_text':
        return scheme + TEXT_EXPORT_ENDPOINT + auth
    if endpoint == 'annotate_publication':
        return scheme + PUBMED_ANNOTATE_ENDPOINT + str(pmid) + auth
    if endpoint == 'export_publication':
        return scheme + PUBMED_EXPORT_ENDPOINT + str(pmid) + auth
    raise ValueError('Unknown endpoint "%s"' % endpoint)


def validate_authentication():
    '''Ensure the user has authenticated itself by providing an email
    address and tool name.'''

    if not email or not email.strip():
        raise AuthenticationRequired('Please set your email')
    if not tool or not tool.strip():
        raise AuthenticationRequired('Please set your tool name')


def validate_text(text):
    '''Validate text to annotate.'''

    if not text or not text.strip():
        raise ValueError('Invalid ``text`` parameter')


def validate_pmid(pmid):
    '''Validate PMID to annotate'''

    if not pmid or not isinstance(pmid, int) or pmid <= 0:
        raise ValueError('Invalid ``pmid`` parameter')


def validate_groups(groups):
    '''Validate semantic groups.'''

    if not isinstance(groups, dict):
        raise InvalidGroups('If specified, ``groups`` must be a dictionary')

    valid = False
    for group, value in groups.items():
        if group not in SEMANTIC_GROUPS:
            raise InvalidGroups('Unknown group ``%s``' % group)
        if type(value) is not bool:
            raise InvalidGroups(
                'Invalid value ``%s`` for group ``%s``. Must be boolean'
                % (value, group))
        if value:
            valid = True
    if not valid:  # no "true" groups for annotation
        raise InvalidGroups('No ``groups`` selected for annotation.'
                            ' At least one group must be true')


def validate_format(format):
    '''Validate export format.'''

    if format not in EXPORT_FORMATS:
        raise InvalidFormat('Unknown format ``%s``' % format)


def do_request(endpoint, payload):
    '''Perform a POST request to one of the becas API endpoints.'''

    # Throttle requests to perform at most two per second
    delay = 0.5
    current = time.time()
    wait = do_request.previous + delay - current
    if wait > 0:
        time.sleep(wait)
        do_request.previous = current + wait
    else:
        do_request.previous = current
    try:
        res = requests.post(endpoint,
                            data=json.dumps(payload),
                            headers=DEFAULT_HEADERS,
                            timeout=timeout,
                            verify=False)  # SSL certificate validation fails
                                           # in systems without proper CAs
                                           # installed, so we disable
                                           # client validation
    except requests.exceptions.Timeout as e:
        raise Timeout(e)
    except requests.exceptions.SSLError as e:
        raise SSLError(e)
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(e)
    except Exception as e:
        raise BecasException(e)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if res.status_code == 404:
            raise PublicationNotFound(res.json()['error'])
        if res.status_code == 413:
            raise TooMuchText(res.json()['error'])
        if res.status_code == 429:
            raise TooManyRequests(wait=res.headers['Retry-After'])
        if res.status_code == 502:
            raise ServiceUnavailable()
        if res.status_code == 503:
            raise ServiceUnavailable(res.json()['error'])
        raise BecasException(e)

    return res

do_request.previous = 0  # time of last request


# -- Command line interface ---------------------------------------------------
def argparser():
    '''Return ArgumentParser to parse command-line options.'''

    import argparse
    description = 'Annotate text or PubMed publications using the becas API.'
    ap = argparse.ArgumentParser(description=description)
    # API method selection
    subparsers = ap.add_subparsers()
    #  Text methods
    text_annotate_parser = subparsers.add_parser(
        'annotate-text',
        help='annotate text as JSON with concept metadata',
        description=('Annotate text with biomedical concepts using the '
                     'becas API.'))
    text_annotate_parser.set_defaults(func=cli_annotate_text)
    text_export_parser = subparsers.add_parser(
        'export-text',
        help='export text in a chosen format',
        description=('Export text annotated with biomedical concepts in a '
                     ' chosen format using the becas API.'))
    text_export_parser.set_defaults(func=cli_export_text)
    for text_parser in (text_annotate_parser, text_export_parser):
        add_auth_options(text_parser)
        input_group = text_parser.add_argument_group('input selection')
        text_input = input_group.add_mutually_exclusive_group(required=True)
        text_input.add_argument('-f', '--file', type=argparse.FileType('rt'),
                                dest='file', metavar='FILE',
                                help='text file to annotate')
        text_input.add_argument('-t', '--text', dest='text', metavar='TEXT',
                                help='plain text to annotate')
        text_input.add_argument('-i', '--stdin', action='store_true',
                                dest='stdin', help='read text from STDIN')
    output_group = text_export_parser.add_argument_group('output selection')
    output_group.add_argument('--format', required=True, dest='format',
                              choices=EXPORT_FORMATS, help='output format')
    #  Publication methods
    publication_annotate_parser = subparsers.add_parser(
        'annotate-publication',
        help='annotate PubMed publication as JSON with concept metadata',
        description=('Annotate PubMed publications with biomedical concepts '
                     'using the becas API.'))
    publication_annotate_parser.set_defaults(func=cli_annotate_publication)
    publication_export_parser = subparsers.add_parser(
        'export-publication',
        help='export PubMed publication in MEDLINE IeXML',
        description=('Export PubMed publications annotated with biomedical '
                     'concepts using the becas API.'))
    publication_export_parser.set_defaults(func=cli_export_publication)
    for publication_parser in (
            publication_annotate_parser, publication_export_parser):
        add_auth_options(publication_parser)
        input_group = publication_parser.add_argument_group('input selection')
        input_group.add_argument('-p', '--pmid', type=int, required=True,
                                 dest='pmid', metavar='PMID',
                                 help='PMID of publication to annotate')
    for parser in (text_annotate_parser, text_export_parser,
                   publication_annotate_parser, publication_export_parser):
        add_common_options(parser)
    return ap


def add_auth_options(parser):
    '''Add API authentication options to a ArgumentParser.'''

    auth_group = parser.add_argument_group('client authentication')
    auth_group.add_argument('--email', dest='email', required=True,
                            help='Email address to use in API authentication')
    auth_group.add_argument('--tool', dest='tool', default=tool,
                            help=('Tool name to use in API authentication '
                                  '(default: %s)' % tool))


def add_common_options(parser):
    '''Add common API options to a ArgumentParser.'''

    import argparse
    parser.add_argument('-g', '--groups', dest='groups',
                        help=('semantic groups to use for annotation as a '
                              'comma separated list (e.g. PRGE,DISO,ANAT). '
                              'Available groups: (%s)'
                              % ', '.join(SEMANTIC_GROUPS)))
    parser.add_argument('-o', '--output-file', type=argparse.FileType('wt'),
                        dest='output_file', metavar='FILE',
                        help='file to save annotation results to')
    parser.add_argument('--secure', action='store_true', dest='secure',
                        default=secure,
                        help='access the service securely through HTTPS')
    parser.add_argument('--timeout', type=int, dest='timeout',
                        default=timeout,
                        help='seconds to wait before timing out a request')


def setup_common_cli_args(args):
    '''Validate and set common command-line arguments.'''

    global email, tool, timeout, secure
    email = args.email
    tool = args.tool
    timeout = args.timeout
    secure = args.secure
    groups = None
    if args.groups:
        groups = {}
        for group in args.groups.split(','):
            groups[group] = True
        try:
            validate_groups(groups)
        except InvalidGroups as e:
            argparser().error(e)
    return groups


def validate_cli_text(text, err_msg):
    '''Validate text input from command-line.'''

    try:
        validate_text(text)
    except ValueError:
        argparser().error(err_msg)


def get_cli_text(args):
    '''Read text from the chosen input medium.'''

    if args.stdin:
        text = sys.stdin.read()
        validate_cli_text(text, 'Got no text from STDIN')
    elif args.file:
        text = args.file.read()
        validate_cli_text(text, '`%s` file is empty or non-textual'
                                % args.file.name)
    else:
        text = args.text
        validate_cli_text(text, 'Got empty --text argument')
    return text


def handle_annotation_results(results, output_file):
    '''Print annotation results to STDOUT or to a file.'''

    results = json.dumps(results) if isinstance(results, dict) else results
    if output_file:
        output_file.write(results.encode('utf-8'))
        output_file.close()
    else:
        sys.stdout.write(results)
        sys.stdout.flush()


def cli_annotate_text(args):
    '''Annotate text from the command-line.'''

    groups = setup_common_cli_args(args)
    text = get_cli_text(args)
    try:
        results = annotate_text(text, groups)
    except ValueError as e:
        argparser().error(e)
    handle_annotation_results(results, args.output_file)


def cli_export_text(args):
    '''Export annotated text from the command-line.'''

    groups = setup_common_cli_args(args)
    text = get_cli_text(args)
    try:
        results = export_text(text, args.format, groups)
    except ValueError as e:
        argparser().error(e)
    handle_annotation_results(results, args.output_file)


def cli_annotate_publication(args):
    '''Annotate PubMed publication from the command-line.'''

    groups = setup_common_cli_args(args)
    try:
        results = annotate_publication(args.pmid, groups)
    except ValueError as e:
        argparser().error(e)
    handle_annotation_results(results, args.output_file)


def cli_export_publication(args):
    '''Export annotated PubMed publication from the command-line.'''

    groups = setup_common_cli_args(args)
    try:
        results = export_publication(args.pmid, groups)
    except ValueError as e:
        argparser().error(e)
    handle_annotation_results(results, args.output_file)


def main():
    '''Command-line interface entry point.'''

    parser = argparser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write('Manually interrupted by ^C. Aborting.\n')
