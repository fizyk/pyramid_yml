# -*- coding: utf-8 -*-

import os
import sys

import pytest
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from webtest import TestApp

from tests.utils import config_factory

package_name, filename = resolve_asset_spec('tests:config')
__import__(package_name)
package = sys.modules[package_name]
full_path = os.path.join(package_path(package), filename)


class App(object):

    """Simplest form of our test application"""

    def __init__(self, app, config):
        self.app = app
        self.config = config


@pytest.fixture(scope='function',
                params=['tests:config', 'tests:config/config.yml', full_path])
def base_app(request):
    """Configure the Pyramid application."""

    # Configure redirect routes
    config = config_factory(**{'yml.location': request.param})
    # Add routes for change_password, change_username,
    app = TestApp(config.make_wsgi_app())
    return App(app, config)


@pytest.fixture(scope='function',
                params=['tests:config', 'tests:config/config.yml', full_path])
def prod_app(request):
    """Configure the Pyramid application.
       This time we want it to production environment.
    """

    # Configure redirect routes
    config = config_factory(**{'env': 'prod',
                            'yml.location': request.param})
    # Add routes for change_password, change_username,
    app = TestApp(config.make_wsgi_app())
    return App(app, config)
