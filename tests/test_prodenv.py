"""Tests pyramid_yaml with setting environment."""


def test_reading_prod(prod_config):
    """Test whether prod config gets read."""
    # In this test with env=prod,
    # config.dev.yml will not be read (would be prod if existed
    assert prod_config.registry['config'].key.env == 'default'


def test_include(prod_config):
    """Test if includemes options runs include action for defined data."""
    # Included module should set a key on registry
    assert 'includeme_method' in prod_config.registry
    # Values set by included module should be True
    assert prod_config.registry['includeme_method'] is True
    # Not included, no key on registry
    assert 'includeme_method2' in prod_config.registry
    # Values set by included module should be True
    assert prod_config.registry['includeme_method2'] is True
