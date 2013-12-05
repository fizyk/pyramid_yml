# -*- coding: utf-8 -*-

import os
import sys

import pytest
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from webtest import TestApp

from tests.utils import config_factory


class App(object):

    """Simplest form of our test application"""

    def __init__(self, app, config):
        self.app = app
        self.config = config


@pytest.fixture(scope='function')
def base_app():
    """Configure the Pyramid application."""

    # Configure redirect routes
    config = config_factory(**{'yml.location': 'tests:config'})
    # Add routes for change_password, change_username,
    app = TestApp(config.make_wsgi_app())
    return App(app, config)


@pytest.fixture(scope='function')
def prod_app():
    """Configure the Pyramid application.
       This time we want it to production environment.
    """

    # Configure redirect routes
    config = config_factory(**{'env': 'prod', 'yml.location': 'tests:config'})
    # Add routes for change_password, change_username,
    app = TestApp(config.make_wsgi_app())
    return App(app, config)


@pytest.fixture(scope='function')
def prod_fullfile_app():
    """Configure the Pyramid application.
       We need to be sure that we get full path to pass always,
       no matter where this test is being run.
    """

    package_name, filename = resolve_asset_spec('tests:config')
    __import__(package_name)
    package = sys.modules[package_name]
    path = os.path.join(package_path(package), filename)
    # Configure redirect routes
    config = config_factory(**{'env': 'prod', 'yml.location': path})
    # Add routes for change_password, change_username,
    app = TestApp(config.make_wsgi_app())
    return App(app, config)
