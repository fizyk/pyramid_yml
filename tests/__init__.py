# -*- coding: utf-8 -*-

import sys
import os
import unittest

from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path

try:
    from webtest import TestApp
except ImportError:
    pass


def config_factory(**settings):
    """Call with settings to make and configure a configurator instance.
    """

    from pyramid.config import Configurator
    from pyramid.session import UnencryptedCookieSessionFactoryConfig

    # Initialise the ``Configurator`` and setup a session factory.
    config = Configurator(settings=settings)
    # Include base.
    config.include('tzf.pyramid_yml')
    # Return the configurator instance.
    return config


def includeme_method(config):
    config.registry['includeme_method'] = True


def includeme_method2(config):
    config.registry['includeme_method2'] = True


class BaseTestCase(unittest.TestCase):

    def setUp(self, settings={'yml.location': 'tests:config'}):
        """Configure the Pyramid application."""

        self.config = config_factory(**settings)
        self.app = TestApp(self.config.make_wsgi_app())


class ConfigBaseTest(BaseTestCase):

    def test_config_creation(self):
        '''Test whether configuration gets created'''
        from pymlconf import ConfigManager
        self.failUnless('config' in self.config.registry)
        self.assertTrue(isinstance(self.config.registry['config'], ConfigManager))

    def test_reading_dev(self):
        '''Test whether dev config gets read'''
        self.assertTrue(self.config.registry[
                        'config'].key.env == 'dev', 'key.env value should be overwritten in config.dev.yml!')

    def test_setting_overwriting(self):
        '''Test whether 'configurator' key moves to settings'''
        self.assertTrue('pyramid.reload_templates' in self.config.registry.settings)
        self.assertTrue(self.config.registry.settings['pyramid.reload_templates'] == self.config.registry[
                        'config'].configurator['pyramid.reload_templates'])

    def test_settings_overwrite_complex(self):
        '''Test whether 'configurator' complex keys gets moved into settings'''
        self.assertTrue('sqlalchemy.url' in self.config.registry.settings)
        self.assertTrue(self.config.registry.settings[
                        'sqlalchemy.url'] == self.config.registry['config'].configurator['sqlalchemy']['url'])

    def test_includeme(self):
        '''Tests if includeme's options runs include action for defined data. One should be included,  the other is defined as False'''
        self.assertTrue('includeme_method' in self.config.registry, 'Included module should set a key on registry')
        self.assertTrue(self.config.registry['includeme_method'], 'Values set by included module should be True')
        self.assertTrue('includeme_method2' not in self.config.registry, 'Not included, no key on registry')


class ConfigDefaultsTest(BaseTestCase):

    def test_extend_with_defaults(self):
        '''Test whether default from extending defaults are not overriding previously created config'''

        self.assertFalse('subkey3' in self.config.registry['config'].key, 'defaults.yml is not yet included')
        self.config.config_defaults('tests:config', files=['defaults.yml'])

        self.assertFalse(self.config.registry['config'].key.subkey,
                         'defaults.yml sets to True, but it should be defined as False by config.yml')
        self.assertTrue('subkey3' in self.config.registry['config'].key, 'defaults.yml is included, key should exists')


class ConfigProdEnvTest(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self, {'env': 'prod', 'yml.location': 'tests:config'})

    def test_reading_prod(self):
        '''Test whether prod config gets read'''
        self.assertTrue(self.config.registry['config'].key.env == 'default',
                        'In this test with env=prod, config.dev.yml will not be read (would be prod if existed)')

    def test_includeme(self):
        '''Tests if includeme's options runs include action for defined data.'''
        self.assertTrue('includeme_method' in self.config.registry, 'Included module should set a key on registry')
        self.assertTrue(self.config.registry['includeme_method'], 'Values set by included module should be True')
        self.assertTrue('includeme_method2' in self.config.registry, 'Not included, no key on registry')
        self.assertTrue(self.config.registry['includeme_method2'], 'Values set by included module should be True')


class ConfigByFilenameTest(BaseTestCase):

    def setUp(self):
        # this works in relation from where the tests are being run
        BaseTestCase.setUp(self, {'env': 'prod', 'yml.location': 'tests/config'})

    def test_reading(self):
        '''Test whether config by path gets read'''
        self.assertTrue('key' in self.config.registry['config'],
                        'In this test with env=prod, config.dev.yml will not be read (would be prod if existed)')


class ConfigByFullFilenameTest(BaseTestCase):

    def setUp(self):
        # making sure we get full path to pass always, no matter where this test is being run
        package_name, filename = resolve_asset_spec('tests:config')
        __import__(package_name)
        package = sys.modules[package_name]
        path = os.path.join(package_path(package), filename)
        BaseTestCase.setUp(self, {'env': 'prod', 'yml.location': path})

    def test_reading(self):
        '''Test whether config by full path gets read'''
        self.assertTrue('key' in self.config.registry['config'],
                        'In this test with env=prod, config.dev.yml will not be read (would be prod if existed)')
