# Copyright (c) 2013 - 2014 by tzf.pyramid_yml authors and contributors
# <see AUTHORS file>
#
# This module is part of tzf.pyramid_yml and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Module behind pconfig commandline entrypoint."""

import argparse
import sys
import textwrap

from pyramid.paster import bootstrap

_INDENT = '  '


def print_config():  # pragma: no cover
    """Print config entry function."""
    description = """\
        Print the deployment settings for a Pyramid application.  Example:
        'psettings deployment.ini'
    """
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(description)
    )
    parser.add_argument(
        'config_uri', type=str, help='an integer for the accumulator'
    )
    parser.add_argument(
        '-k', '--key',
        dest='key',
        metavar='PREFIX',
        type=str,
        action='store',
        help=(
            "Tells script to print only specified"
            " config tree provided by dotted name"
        )
    )
    args = parser.parse_args(sys.argv[1:])

    config_uri = args.config_uri
    env = bootstrap(config_uri)
    config, closer = env['registry']['config'], env['closer']

    try:
        print(printer(slice_config(config, args.key)))
    except KeyError:
        print(
            'Sorry, but the key path {0}, does not exists in Your config!'
            .format(args.key)
        )
    finally:
        closer()


def printer(data, depth=0):
    """
    Prepare data for printing.

    :param data: a data value that will be processed by method
    :param int depth: recurrency indicator, to maintain proper indent

    :returns: string with formatted config
    :rtype: str
    """
    indent = _INDENT * depth
    config_string = '' if not depth else ':\n'
    if isinstance(data, dict):
        for key, val in data.items():
            line = '{0}{1}'.format(indent, key)
            values = printer(val, depth + 1)
            if not values.count('\n'):
                values = ': {0}'.format(values.lstrip())

            line = '{line}{values}'.format(line=line, values=values)
            config_string += '{0}\n'.format(line)

    elif isinstance(data, list):
        for elem in data:
            config_string += '{0} - {1}\n'.format(indent, elem)
    else:
        config_string = '{0}{1} ({2})'.format(
            indent, data, data.__class__.__name__
        )

    return config_string.rstrip('\n')


def slice_config(config, key):
    """
    Slice config for printing as defined in key.

    :param ConfigManager config: configuration dictionary
    :param str key: dotted key, by which config should be sliced for printing

    :returns: sliced config
    :rtype: dict
    """
    if key:
        keys = key.split('.')
        for k in keys:
            config = config[k]

    return config
