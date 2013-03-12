# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

here = os.path.dirname(__file__)
with open(os.path.join(here, 'tzf', 'pyramid_yml', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


def read(fname):
    return open(os.path.join(here, fname)).read()

test_requires = [
    'WebTest',
    'nose',
    'coverage',
]

extras_require = {
    'docs': ['sphinx', 'sphinx_bootstrap_theme'],
}

setup(
    name='tzf.pyramid_yml',
    version=package_version,
    description='Reads and sets routing configuration from a package',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    keywords='pyramid yml configuration',
    author='Grzegorz Sliwinski',
    author_email='username: fizyk, domain: fizyk.net.pl',
    url='https://github.com/fizyk/pyramid_yml',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    namespace_packages=['tzf'],
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyramid',
        'pymlconf >= 0.2.9a'
    ],
    tests_require=test_requires,
    extras_require=extras_require,
)
