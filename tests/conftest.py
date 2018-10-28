"""Tests conftest file."""
import os
import sys

import pytest
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pytest_pyramid import factories

# pylint:disable=invalid-name
package_name, filename = resolve_asset_spec('tests:config')
__import__(package_name)
package = sys.modules[package_name]
full_path = os.path.join(package_path(package), filename)

base_config_package = factories.pyramid_config({
    'yaml.location': 'tests:config',
    'pyramid.includes': ['tzf.pyramid_yml']
})

base_config_package_file = factories.pyramid_config({
    'yaml.location': 'tests:config/config.yaml',
    'pyramid.includes': ['tzf.pyramid_yml']
})


base_config_full_path = factories.pyramid_config({
    'yaml.location': full_path,
    'pyramid.includes': ['tzf.pyramid_yml']
})


@pytest.fixture(
    scope='function',
    params=[
        'base_config_package',
        'base_config_package_file',
        'base_config_full_path'
    ]
)
def base_config(request):
    """Config parametrized for different configuration location."""
    return request.getfixturevalue(request.param)


prod_config_package = factories.pyramid_config({
    'env': 'prod',
    'yaml.location': 'tests:config',
    'pyramid.includes': ['tzf.pyramid_yml']
})


prod_config_package_file = factories.pyramid_config({
    'env': 'prod',
    'yaml.location': 'tests:config/config.yaml',
    'pyramid.includes': ['tzf.pyramid_yml']
})


prod_config_full_path = factories.pyramid_config({
    'env': 'prod',
    'yaml.location': full_path,
    'pyramid.includes': ['tzf.pyramid_yml']
})


@pytest.fixture(
    scope='function',
    params=[
        'prod_config_package',
        'prod_config_package_file',
        'prod_config_full_path'
    ]
)
def prod_config(request):
    """Config parametrized for different configuration location."""
    return request.getfixturevalue(request.param)


prod_config_list1 = factories.pyramid_config({
    'env': 'prod',
    'yaml.location': ['tests:config', 'tests:config2'],
    'pyramid.includes': ['tzf.pyramid_yml']
})


prod_config_list2 = factories.pyramid_config({
    'env': 'prod',
    'yaml.location': 'tests:config, tests:config2',
    'pyramid.includes': ['tzf.pyramid_yml']
})


@pytest.fixture(
    scope='function',
    params=['prod_config_list1', 'prod_config_list2']
)
def multifolder_config(request):
    """Test with two ways of setting many locations for config."""
    return request.getfixturevalue(request.param)
# pylint:enable=invalid-name
