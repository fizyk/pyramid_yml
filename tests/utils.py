# -*- coding: utf-8 -*-


def config_factory(**settings):
    """Call with settings to make and configure a configurator instance.
    """
    from pyramid.config import Configurator
    # Initialise the ``Configurator`` and setup a session factory.
    config = Configurator(settings=settings)
    # Include base.
    config.include('tzf.pyramid_yml')
    # Return the configurator instance.
    return config


# dunno why it is here, but I will get know
def includeme_method(config):
    config.registry['includeme_method'] = True


def includeme_method2(config):
    config.registry['includeme_method2'] = True
