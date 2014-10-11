Usage
=====

To use **tzf.pyramid_yml** in your pyramid app, add a ``config.include`` directive:

.. code-block:: python

    config.include('tzf.pyramid_yml')

Now you need to add ``yaml.location`` into your application's ``settings.ini`` file.

.. code-block:: ini

    [app:main]
    # ....
    yaml.location = my.package:config
    env = dev # default value is dev
    # ....

This settings key can be a **path** or **list of paths** allowing you to keep
configurations for your production environment separately.

.. note::
    This configuration option works on the same principle as defining pyramid
    assets. It can be a package asset path or a pathname only.

Path can point to directory or to exact file. In the latter case, pyramid_yml
will try to inject the env part into the filename, and will try to read from both
the main config, and the env one, alike. So setting
*my.package:config/application.yaml* will result in pyramid_yml trying to read
configuration from both */path/to/my/package/config/application.yaml* and
*/path/to/my/package/config/application.env.yaml*.

There's no rule here on what extensions pyramid_yml will try to read;
just that these files must contain yaml syntax.

.. note::
    You do not have to define any of these options:

    * **yaml.location** defaults to the place you start your app from (usually the same place you keep your .ini files usually)
    * **env** defaults to dev

Multifile configuration support
-------------------------------

There exists multifile configuration support, meaning that configuration can be
stored in several files at once and all of them will be joined.

To do that, you need to either load defaults with a list of config locations,
or add other locations separated by comma in your ini file:

.. code-block:: ini

    [app:main]
    # ....
    yaml.location = my.package:config, my.package:config3
    # ....

Yaml configuration files
------------------------

tzf.pyramid_yml will read two yaml configuration files:
*config.yaml* and *config.{env}.yaml* (config.dev.yaml in this case) from yaml.location.
The second one will overwrite the values from the first file,
but all keys and values defined in first, and not in second, will stay the same:

.. code-block:: yaml

    # config.yaml
    key:
        subkey: value
        subkey2: value2


.. code-block:: yaml

    #config.dev.yaml
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

Configuration will be accessible from the request object under the ``config`` attribute:
``request.config``. It's a ``ConfigManager`` instance, meaning
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
of yaml files, as defined in *yaml.location*, allowing to use this method
by 3rd party pyramid plugins.

To do this, config_defaults method has been added to Configurator object.
Using it is as simple as:

.. code-block:: python

    config.config_defaults('package.module:folder/subfolder')
    config.config_defaults('package.module:folder/subfolder', ['my_defaults.yaml'])

It's more detailed within the api section. :meth:`tzf.pyramid_yml.config_defaults`
