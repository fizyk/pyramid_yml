# -*- coding: utf-8 -*-

from pymlconf import ConfigManager


def test_config_creation(base_app):
    '''Test whether configuration gets created'''
    assert 'config' in base_app.config.registry
    assert isinstance(base_app.config.registry['config'], ConfigManager)


def test_reading_dev(base_app):
    '''Test whether dev config gets read
       key.env value should be overwritten in config.dev.yml!
    '''
    assert base_app.config.registry['config'].key.env == 'dev'


def test_setting_overwriting(base_app):
    '''Test whether 'configurator' key moves to settings'''
    assert 'pyramid.reload_templates' in base_app.config.registry.settings
    assert (base_app.config.registry.settings['pyramid.reload_templates']
            ==
            base_app
            .config
            .registry['config'].configurator['pyramid.reload_templates'])


def test_settings_overwrite_complex(base_app):
    '''Test whether 'configurator' complex keys gets moved into settings'''
    assert ('sqlalchemy.url' in base_app.config.registry.settings)
    assert (base_app.config.registry.settings['sqlalchemy.url']
            ==
            base_app
            .config
            .registry['config'].configurator['sqlalchemy']['url'])


def test_includeme(base_app):
    '''Tests if includeme's options runs include action for defined data.
       One should be included,  the other is defined as False'''
    # key.env value should be overwritten in config.dev.yml!
    assert ('includeme_method' in base_app.config.registry)
    # Values set by included module should be True
    assert (base_app.config.registry['includeme_method'])
    # Not included, no key on registry
    assert ('includeme_method2' not in base_app.config.registry)
