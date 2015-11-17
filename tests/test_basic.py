"""Basic tests."""

from pymlconf import ConfigManager


def test_config_creation(base_config):
    """Test whether configuration gets created."""
    assert 'config' in base_config.registry
    assert isinstance(base_config.registry['config'], ConfigManager)


def test_reading_dev(base_config):
    """
    Test whether dev config gets read.

    key.env value should be overwritten in config.dev.yml!
    """
    assert base_config.registry['config'].key.env == 'dev'


def test_setting_overwriting(base_config):
    """Test whether 'configurator' key moves to settings."""
    assert 'pyramid.reload_templates' in base_config.registry.settings
    assert base_config.registry.settings['pyramid.reload_templates'] ==\
        base_config.registry['config'].\
        configurator['pyramid.reload_templates']


def test_settings_overwrite_complex(base_config):
    """Test whether 'configurator' complex keys gets moved into settings."""
    assert ('sqlalchemy.url' in base_config.registry.settings)
    assert base_config.registry.settings['sqlalchemy.url'] ==\
        base_config.\
        registry['config'].configurator['sqlalchemy']['url']


def test_includeme(base_config):
    """
    Test if includeme's options runs include action for defined data.

    One should be included,  the other is defined as False
    """
    # key.env value should be overwritten in config.dev.yml!
    assert ('includeme_method' in base_config.registry)
    # Values set by included module should be True
    assert (base_config.registry['includeme_method'])
    # Not included, no key on registry
    assert ('includeme_method2' not in base_config.registry)
