"""Tests conftest file."""
import os
import sys

import pytest
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pytest_pyramid import factories


package_name, filename = resolve_asset_spec('tests:config')
__import__(package_name)
package = sys.modules[package_name]
full_path = os.path.join(package_path(package), filename)


@pytest.fixture(scope='function',
                params=['tests:config', 'tests:config/config.yaml', full_path])
def base_config(request):
    """Basic config parametrized for different configuration location."""
    return factories.pyramid_config({
        'yaml.location': request.param,
        'pyramid.includes': ['tzf.pyramid_yml']
    })(request)


@pytest.fixture(scope='function',
                params=['tests:config', 'tests:config/config.yaml', full_path])
def prod_config(request):
    """Basic with env set parametrized for different configuration location."""
    return factories.pyramid_config({
        'env': 'prod',
        'yaml.location': request.param,
        'pyramid.includes': ['tzf.pyramid_yml']
    })(request)


@pytest.fixture(
    scope='function',
    params=[['tests:config', 'tests:config2'], 'tests:config, tests:config2'])
def multifolder_config(request):
    """Test with two ways of setting many locations for config."""
    return factories.pyramid_config({
        'env': 'prod',
        'yaml.location': request.param,
        'pyramid.includes': ['tzf.pyramid_yml']
    })(request)
