Usage
=====

To use **tzf.pyramid_yml** in your pyramid app, add config.include('') directive.

.. code-block:: python

    config.inlude('tzf.pyramid_yml')

Now you need to add **yml.location** into you application's setting.ini file.

.. code-block:: ini

    [app:main]
        # ....
        yml.location = my.package:config
        env = dev # default value is dev
        # ....

This settings key can be a **path** or **list of paths** allowing you to keep
configurations for production environment separately.

.. note::
    This configuration option works on the same principle, as defining pyramid
    assets. Can be package asset path, or pathname only.

Path can point to directory or to exact file. In the latter case, pyramid_yml
will try to inject env part into the filename, and trying to read from both
main config, and env one, like. So effectively setting
*my.package:config/application.yml* will result in
*/path/to/my/package/config/config.yml* and */path/to/my/package/config/config.env.yml*
from which pyramid_yml will try to read configuration.

.. note::
    You do not have to define any of these options:

    * **yml.location** defaults to the place you start your app from (usually, same place you keep your .ini files)
    * **env** defaults to dev

Yaml configuration files
------------------------

tzf.pyramid_yml will read two yaml configuration files:
*config.yml* and *config.{env}.yml* (config.dev.yml in this case) from yml.location.
The second one will overwrite the values from the first file,
but all keys and values defined in first, and not in second, will stay the same:

.. code-block:: yaml

    # config.yml
    key:
        subkey: value
        subkey2: value2


.. code-block:: yaml

    #config.dev.yml
    key:
        subkey2: overwritten
        another:
            deep:
                subkey: 1

These two files will result in this config dictionary:

.. code-block:: python

    {'key': {'subkey': 'value'
            'subkey2': 'overwritten'
            'another': {'deep': {'subkey': 1}}
            }
    }

Access to configuration
-----------------------

Configuration will be accessible on request object under config attribute:
**request.object**. It's a ConfigManager instance, meaning,
that all keys can be accessed as regular dictionary keys or as attributes.


Pyramid settings in yaml config
-------------------------------

You can use yml config to define global settings for 3rd party packages,
that requires configuration in one place (and not in your code), and use
config inheritance, as well as structures.

Every keys placed within configuration: key in yml config, will be copied
into pyramid's setting dictionary.

.. code-block:: yaml

    configurator:
        sqlalchemy.url: 'connection:url'

or

.. code-block:: yaml

    configurator:
        sqlalchemy:
            url: 'connection:url'

will become:

.. code-block:: python

    config.registry.settings['sqlalchemy.url']

.. warning::
    all **pyramid.*** settings should still be defined in ini settings file,
    as these are processed on application start


Including packages
------------------

.. note::
    This functionality is an attempt to move more core pyramid functionality
    into yml configuration.

    For more information see `Pyramid documentation on including packages
    <http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/narr/environment.html#including-packages>`_


To include other packages, and not define them in *.ini* settings file, add include:
key into your yml config.

.. code-block:: yaml

    include:
        some.module: True           # Module, that'll be included
        prefixed.module: 'path'     # Module included with route_prefix
        not.included.module: False  # Module not included (helpful for overriding inherited global setting)

pconfig - command line tool
---------------------------

tzf.pyramid_yml provides a command line, `pconfig` which will help detect
inheritance chain of your yml files. It displays properly indented and inherited
config tree for given environment.

To run, type:
``$ pconfig development.ini``


Adding more defaults
--------------------

**tzf.pyramid_yml** allows to create more defaults, based on same location
of yaml files, as defined in *yml.location*, allowing to use this method
by 3rd party pyramid plugins.

To do this, config_defaults method has been added to Configurator object.
It's use is as simple as:

.. code-block:: python

    config.config_defaults('package.module:folder/subfolder')
    config.config_defaults('package.module:folder/subfolder', ['my_defaults.yml'])

It's more detailed within api section. :meth:`tzf.pyramid_yml.config_defaults`
