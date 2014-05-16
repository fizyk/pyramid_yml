# Copyright (c) 2013 - 2014 by tzf.pyramid_yml authors and contributors
#   <see AUTHORS file>
#
# This module is part of tzf.pyramid_yml and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""First level of namespace package."""

# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
