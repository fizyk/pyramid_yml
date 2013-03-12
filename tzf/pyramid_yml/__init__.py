# -*- coding: utf-8 -*-
import os
import sys
import logging

from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pymlconf import ConfigManager

__version__ = '0.0.1'


logger = logging.getLogger(__name__)


def includeme(configurator, routing_package=None):
    '''
        Adds rotues defined in config into pyramid app

        :param pyramid.config.Configurator configurator: pyramid's app configurator
    '''

    settings = configurator.registry.settings

    # lets default it to running path
    yml_location = settings.get('yml.location', os.getcwd())

    # getting spec path
    package_name, filename = resolve_asset_spec(yml_location)
    if not package_name:
        path = filename
    else:
        __import__(package_name)
        package = sys.modules[package_name]
        path = os.path.join(package_path(package), filename)

    # reading yml configuration
    configurator.registry['config'] = ConfigManager(
        files=[
            os.path.join(path, 'config.yml'),
            os.path.join(path, 'config.{env}.yml'.format(env=settings.get('env', 'dev')))
        ])

    if configurator.registry['config']:
        logger.debug('Yaml config created')

    # let's calla a convenience request method
    configurator.add_request_method(lambda request: request.registry['config'], name='config', property=True)
