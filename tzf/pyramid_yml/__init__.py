# -*- coding: utf-8 -*-
import os
import sys
import logging

from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pymlconf import ConfigManager

__version__ = '0.2.0'


logger = logging.getLogger(__name__)


def includeme(configurator, routing_package=None):
    '''
        Adds rotues defined in config into pyramid app

        :param pyramid.config.Configurator configurator: pyramid's app configurator
    '''

    settings = configurator.registry.settings

    # lets default it to running path
    yml_location = settings.get('yml.location', os.getcwd())

    configurator.add_directive('config_defaults',
                               config_defaults)

    configurator.config_defaults(yml_location, files=[
                                 'config.yml',
                                 'config.{env}.yml'.format(env=settings.get('env', 'dev'))])

    # reading yml configuration

    if configurator.registry['config']:
        logger.debug('Yaml config created')

        # extend settings object
        if 'configurator' in configurator.registry['config']:
            _extend_settings(settings, configurator.registry['config'].configurator)

        # run include's
        if 'include' in configurator.registry['config']:
            _run_includemes(configurator, configurator.registry['config'].include)

    # let's calla a convenience request method
    configurator.add_request_method(lambda request: request.registry['config'], name='config', property=True)


def config_defaults(configurator, config, files=['config.yml']):
    '''
        Reads and extends/creates configuration from yaml source.

        .. note::
            If exists, this method extends config with defaults, so it will not override existing values,
            merely add those, that were not defined already!

        :param pyramid.config.Configurator configurator: pyramid's app configurator
        :param string config: yaml file locations
        :param list files: list of files to include from location
    '''

    # getting spec path
    package_name, filename = resolve_asset_spec(config)
    if not package_name:
        path = filename
    else:
        __import__(package_name)
        package = sys.modules[package_name]
        path = os.path.join(package_path(package), filename)

    config = ConfigManager(files=[os.path.join(path, f) for f in files])

    # we could use this method both for creating and extending. Hence the checks to not override
    if not 'config' in configurator.registry:
        configurator.registry['config'] = config
    else:
        config.merge(configurator.registry['config'])
        configurator.registry['config'] = config


def _extend_settings(settings, configurator_config, prefix=None):
    '''
        Extends settings dictionary with yml'settings defined in configurator: key

        :param dict settings: settings dictionary
        :param dict configurator_config: yml defined settings
        :param str prefix: prefix for settings dict key
    '''
    for key in configurator_config:
        settings_key = '.'.join([prefix, key]) if prefix else key

        if hasattr(configurator_config[key], 'keys') and hasattr(configurator_config[key], '__getitem__'):
            _extend_settings(settings, configurator_config[key], prefix=settings_key)
        else:
            settings[settings_key] = configurator_config[key]


def _run_includemes(configurator, includemes):
    '''
        Runs configurator.include() for packages defined in include key in yaml configuration

        :param pyramid.config.Configurator configurator: pyramid's app configurator
        :param dict includemes: include, a list of includes or dictionary
    '''

    for include in includemes:
        if includemes[include]:
            try:
                configurator.include(include, includemes[include])
            except AttributeError:
                configurator.include(include)
