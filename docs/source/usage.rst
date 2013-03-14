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


Including packages
------------------

.. note::
    This functionality is an attempt to move more core pyramid functionality into yml configuration.

    For more information see `Pyramid documentation on including packages <http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/narr/environment.html#including-packages>`_


To include other packages, and not define them in *.ini* settings file, add include: key into your yml config.

.. code-block:: yaml

    include:
        some.module: True           # Module, that'll be included
        prefixed.module: 'path'     # Module included with route_prefix
        not.included.module: False  # Module not included (helpful for overriding inherited global setting)

