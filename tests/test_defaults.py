"""Tests extending config with defaults."""


def test_extend_with_defaults(base_config):
    """
    Test whether default from extending defaults.

    are not overriding previously created config
    """
    # defaults.yml is not yet included
    assert not ('subkey3' in base_config.registry['config'].key)

    base_config.config_defaults('tests:config', files=['defaults.yaml'])
    # defaults.yml sets to True,
    # but it should be defined as False by config.yml
    assert not base_config.registry['config'].key.subkey
    # defaults.yml is included, key should exists
    assert 'subkey3' in base_config.registry['config'].key
