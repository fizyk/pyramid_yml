"""tzf.pyramid_yml installation file."""
import os
import re
from setuptools import setup, find_packages

here = os.path.dirname(__file__)
with open(os.path.join(here, 'tzf', 'pyramid_yml', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S)\
                        .match(v_file.read())\
                        .group(1)


def read(fname):
    """Quick way to read a file content."""
    content = None
    with open(os.path.join(here, fname)) as f:
        content = f.read()
    return content

test_requires = [
    'pytest-cov==2.2.1',
    'pytest_pyramid==0.2.0'
]

extras_require = {
    'docs': ['sphinx'],
    'tests': test_requires,
}

setup(
    name='tzf.pyramid_yml',
    version=package_version,
    description='Loads a yml defined configuration',
    long_description=(
        read('README.rst') + '\n\n' + read('CHANGES.rst')
    ),
    keywords='pyramid yml configuration',
    author='Grzegorz Sliwinski',
    author_email='username: fizyk, domain: fizyk.net.pl',
    url='https://github.com/fizyk/pyramid_yml',
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
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
        'pymlconf >= 0.3.7'
    ],
    tests_require=test_requires,
    extras_require=extras_require,
    entry_points='''
    [console_scripts]
    pconfig = tzf.pyramid_yml.scripts:print_config
    ''',
)
