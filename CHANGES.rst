=======
CHANGES
=======

1.1.0
-------

- all scripts functions are public
- cleaned pconfig's argument check
- changed config_defaults to not have default mutable argument. It's None instead - which gets replaced by default config.yaml and config.yml.

1.0.1
-------

- improved support for defining more than one configuration locations in ini file


1.0.0
-----
- changed tests to depend on pytest_pyramid
- changed to support yaml extension by default, updated docs


0.3.0
-----
- rewrite all test to py.test
- introduced License
- allow to load configuration files from more than one folder
- use only existing files to squash PymlConf warnings
- ability to use full path to file in yml.location path
- clearing some tests

0.2.0
-----
- *pconfig* command line tool for displaying merged yaml config
- added *config.config_defaults* method to allow creating a default yaml configurations for pyramid packages, and easy merge into these created by tzf.pyramid_yml

0.1.0
-----
- python 3 compatibility
- Include pyramid packages
- filling in standard settings based on configurator: in yml configuration

0.0.1
-----
- merging two yml files int one
- reading yml files
