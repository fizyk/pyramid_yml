import pytest
from webtest import TestApp

from tests.utils import config_factory
from .conftest import App


@pytest.fixture(scope='function')
def multifolder_app():
    """Configure the Pyramid application.
       This time we want it to production environment.
    """

    # Configure redirect routes
    config = config_factory(**{
                            'env': 'prod',
                            'yml.location': ['tests:config', 'tests:config2']
                            })
    # Add routes for change_password, change_username,
    app = TestApp(config.make_wsgi_app())
    return App(app, config)


def test_multifolder(multifolder_app):
    '''
    Checks if files from 2nd folder had been loaded
    '''

    assert 'key_config2' in multifolder_app.config.registry['config']
