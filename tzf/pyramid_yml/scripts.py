# -*- coding: utf-8 -*-
import optparse
import sys
import textwrap

from pyramid.paster import bootstrap
from pymlconf import ConfigDict, ConfigManager, ConfigList


def print_config():

    description = """\
        Print the deployment settings for a Pyramid application.  Example:
        'psettings deployment.ini'
    """
    usage = "usage: %prog config_uri"
    parser = optparse.OptionParser(
        usage=usage,
        description=textwrap.dedent(description)
    )
    parser.add_option(
        '-k', '--key',
        dest='key',
        metavar='PREFIX',
        type='string',
        action='store',
        help=("Tells script to print only specified config tree provided by dotted name")
    )

    options, args = parser.parse_args(sys.argv[1:])
    if not len(args) >= 1:
        print('You must provide at least one argument')
        return 2

    config_uri = args[0]
    env = bootstrap(config_uri)
    config, closer = env['registry']['config'], env['closer']
    key = options.key
    if key:
        keys = key.split('.')
        for k in keys:
            config = config[k]

    printer(config)
    closer()


def printer(data, depth=0):
    ident = '  ' * depth
    if isinstance(data, dict):
        for k, v in data.items():
            if not isinstance(v, (list, dict)):
                print('{0}{1}: {2} ({3})'.format(ident, k, v, v.__class__.__name__))
            else:
                print('{0}{1}:'.format(ident, k))
                printer(v, depth + 1)
    elif isinstance(data, list):
        for el in data:
            print('{0} - {1}'.format(ident, el))
    else:
        print('{0}{1} ({2})'.format(ident, data, data.__class__.__name__))
