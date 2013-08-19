# -*- coding: utf-8 -*-

import pytest
from tzf.pyramid_yml import scripts


def test_printer():
    """ printer: key:value pair
        Simple values should be placed in same line as key
    """
    lines = scripts.printer({'key': 'value'}).split('\n')
    assert len(lines) == 1


def test_printer_two_keys_simple():
    '''printer: 2x key:value
       There are only two key:value pairs
    '''
    lines = scripts.printer({'key': 'value', 'key2': 'value'}).split('\n')
    assert len(lines) == 2


def test_printer_composite_key():
    '''printer: key:key:value
       should be only two lines
    '''

    lines = scripts.printer({'key': {'key2': 'value'}}).split('\n')
    assert len(lines) == 2


def test_simplevalue():
    '''tests for simple value
    '''
    line = scripts.printer(1)
    #value passed should be represented by type in round parenthesis
    assert line == '1 (int)'


# decorator below is used to invoke one test multiple times
# with different sets of test data
# we have two sets of test data (test will be invoked twice)
@pytest.mark.parametrize(('configvalue', 'countlines'),
                         [
                             ({'key': ['value', 'value 2']}, 3),
                             ({'key': ['value']}, 2)
                         ])
def test_printer_list(configvalue, countlines):
    '''printer: key:[value:value]'''
    lines = scripts.printer(configvalue).split('\n')
    #should be three lines. one for key, and two for list
    assert len(lines) == countlines


def test_slice_no_key1():
    '''test no slice pass for config'''
    conf = {'key': 'value', 'key2': {'key3': 'value'}}
    #configuration should be the same
    assert conf == scripts._slice_config(conf, None)


def test_slice_no_key2():
    '''test one key slice for config'''
    conf = {'key': 'value', 'key2': {'key3': 'value'}}
    #configuration should be the same
    assert conf['key2'] == scripts._slice_config(conf, 'key2')


def test_slice_no_key3():
    '''test one key slice for config'''
    conf = {'key': 'value', 'key2': {'key3': 'value'}}
    #configuration should be the same
    assert conf['key2']['key3'] == scripts._slice_config(conf, 'key2.key3')
