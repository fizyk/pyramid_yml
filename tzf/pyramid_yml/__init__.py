# Copyright (c) 2013 - 2014 by tzf.pyramid_yml authors and contributors
# <see AUTHORS file>
#
# This module is part of tzf.pyramid_yml and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""pyramid_yml main functionality."""

import os
import logging

from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pymlconf import ConfigManager

__version__ = '1.1.0'


logger = logging.getLogger(__name__)


def includeme(configurator):
    """
    Add yaml configuration utilities.

    :param pyramid.config.Configurator configurator: pyramid's app configurator
    """
    settings = configurator.registry.settings

    # lets default it to running path
    yaml_locations = settings.get('yaml.location',
                                  settings.get('yml.location', os.getcwd()))

    configurator.add_directive('config_defaults', config_defaults)

    configurator.config_defaults(yaml_locations)

    # reading yml configuration

    if configurator.registry['config']:
        config = configurator.registry['config']
        logger.debug('Yaml config created')

        # extend settings object
        if 'configurator' in config and config.configurator:
            _extend_settings(settings, config.configurator)

        # run include's
        if 'include' in config:
            _run_includemes(configurator, config.include)

    # let's calla a convenience request method
    configurator.add_request_method(
        lambda request: request.registry['config'],
        name='config', property=True
    )


def config_defaults(
        configurator, config_locations, files=None):
    """
    Read and extends/creates configuration from yaml source.

    .. note::
        If exists, this method extends config with defaults,
        so it will not override existing values, merely add those,
        that were not defined already!

    :param pyramid.config.Configurator configurator: pyramid's app configurator
    :param list config_locations: list of yaml file locations
    :param list files: list of files to include from location
    """
    if files is None:
        files = ['config.yaml', 'config.yml']
    if not isinstance(config_locations, (list, tuple)):
        config_locations = config_locations.split(',')

    env = configurator.registry.settings.get('env', 'dev')

    file_paths = []
    for location in config_locations:
        path = _translate_config_path(location)
        current_files = files
        if os.path.isfile(path):
            path, current_files = os.path.split(path)
            current_files = [current_files]

        for config_path in [
            os.path.join(path, f) for f in _env_filenames(current_files, env)
        ]:
            if os.path.isfile(config_path):
                file_paths.append(config_path)

    config = ConfigManager(files=file_paths)

    # we could use this method both for creating and extending.
    # Hence the checks to not override
    if 'config' not in configurator.registry:
        configurator.registry['config'] = config
    else:
        config.merge(configurator.registry['config'])
        configurator.registry['config'] = config


def _translate_config_path(location):
    """
    Translate location into fullpath according asset specification.

    Might be package:path for package related paths, or simply path

    :param str location: resource location
    :returns: fullpath

    :rtype: str
    """
    # getting spec path
    package_name, filename = resolve_asset_spec(location.strip())
    if not package_name:
        path = filename
    else:
        package = __import__(package_name)
        path = os.path.join(package_path(package), filename)

    return path


def _env_filenames(filenames, env):
    """
    Extend filenames with ennv indication of environments.

    :param list filenames: list of strings indicating filenames
    :param str env: environment indicator

    :returns: list of filenames extended with environment version
    :rtype: list
    """
    env_filenames = []
    for filename in filenames:
        filename_parts = filename.split('.')
        filename_parts.insert(1, env)
        env_filenames.extend([filename, '.'.join(filename_parts)])

    return env_filenames


def _extend_settings(settings, configurator_config, prefix=None):
    """
    Extend settings dictionary with content of yaml's  configurator key.

    .. note::

        This methods changes multilayered subkeys defined
        within **configurator** into dotted keys in settings dictionary:

        .. code-block:: yaml

            configurator:
                sqlalchemy:
                    url: mysql://user:password@host/dbname

        will result in **sqlalchemy.url**: mysql://user:password@host/dbname
        key value in settings dictionary.

    :param dict settings: settings dictionary
    :param dict configurator_config: yml defined settings
    :param str prefix: prefix for settings dict key
    """
    for key in configurator_config:
        settings_key = '.'.join([prefix, key]) if prefix else key

        if hasattr(configurator_config[key], 'keys') and\
                hasattr(configurator_config[key], '__getitem__'):
            _extend_settings(
                settings, configurator_config[key], prefix=settings_key
            )
        else:
            settings[settings_key] = configurator_config[key]


def _run_includemes(configurator, includemes):
    """
    Automatically include packages defined in **include** configuration key.

    :param pyramid.config.Configurator configurator: pyramid's app configurator
    :param dict includemes: include, a list of includes or dictionary
    """
    for include in includemes:
        if includemes[include]:
            try:
                configurator.include(include, includemes[include])
            except AttributeError:
                configurator.include(include)
