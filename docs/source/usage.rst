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
