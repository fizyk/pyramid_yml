# -*- coding: utf-8 -*-

import unittest

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
        self.assertTrue(self.config.registry['config'].key.env == 'dev', 'key.env value should be overwritten in config.dev.yml!')

    def test_setting_overwriting(self):
        '''Test whether 'configurator' key moves to settings'''
        self.assertTrue('pyramid.reload_templates' in self.config.registry.settings)
        self.assertTrue(self.config.registry.settings['pyramid.reload_templates'] == self.config.registry['config'].configurator['pyramid.reload_templates'])

    def test_settings_overwrite_complex(self):
        '''Test whether 'configurator' complex keys gets moved into settings'''
        self.assertTrue('sqlalchemy.url' in self.config.registry.settings)
        self.assertTrue(self.config.registry.settings['sqlalchemy.url'] == self.config.registry['config'].configurator['sqlalchemy']['url'])


class ConfigProdEnvTest(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self, {'env': 'prod', 'yml.location': 'tests:config'})

    def test_reading_prod(self):
        '''Test whether prod config gets read'''
        self.assertTrue(self.config.registry['config'].key.env == 'default',
                        'In this test with env=prod, config.dev.yml will not be read (would be prod if existed)')


class ConfigByFilenameTest(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self, {'env': 'prod', 'yml.location': 'tests/config'})

    def test_reading(self):
        '''Test whether prod config gets read'''
        self.assertTrue('key' in self.config.registry['config'],
                        'In this test with env=prod, config.dev.yml will not be read (would be prod if existed)')
