"""Fake includeme methods."""


def includeme_method(config):
    """Set **includeme_method** key on registry."""
    config.registry['includeme_method'] = True


def includeme_method2(config):
    """Set **includeme_method2** key on registry."""
    config.registry['includeme_method2'] = True
