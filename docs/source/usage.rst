Usage
=====

To use **tzf.pyramid_yml** in your pyramid app, add config.include('') directive.

.. code-block:: python

    config.inlude('tzf.pyramid_yml')

Configuration
-------------

No you need to add **yml.location** into you app's setting.ini file.

.. code-block:: ini

    [app:main]
        # ....
        yml.location = my.package:config
        # ....

.. note::
    This configuration option works on the same principle, as defining pyramid assets. Can be package asset path, or pathname only.

.. note::
    You do not have to define this option, it defaults to the place you start your app from (usually, same place you keep you .ini files)


Pyramid settings in yaml config
-------------------------------

You can use yml config to define global settings for 3rd party packages, that requires configuration in one place (and not in your code), and use config inheritance, as well as structures.

Every keys placed within configuration: key in yml config, will be copied into pyramid's setting dictionary.

.. code-block:: yaml

    configurator:
        sqlalchemy.url: 'connection:url'

or

.. code-block:: yaml

    configurator:
        sqlalchemy:
            url: 'connection:url'

will become:

..code-block:: python

    config.registry.settings['sqlalchemy.url']

.. warning::
    all **pyramid.*** settings should still be defined in ini settings file, as these are processed on application start
