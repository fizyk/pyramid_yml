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
    return factories.pyramid_config({
        'yaml.location': request.param,
        'pyramid.includes': ['tzf.pyramid_yml']
    })(request)


@pytest.fixture(scope='function',
                params=['tests:config', 'tests:config/config.yaml', full_path])
def prod_config(request):
    return factories.pyramid_config({
        'env': 'prod',
        'yaml.location': request.param,
        'pyramid.includes': ['tzf.pyramid_yml']
    })(request)


multifolder_config = factories.pyramid_config({
    'env': 'prod',
    'yaml.location': ['tests:config', 'tests:config2'],
    'pyramid.includes': ['tzf.pyramid_yml']
})
