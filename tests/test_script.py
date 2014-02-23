# -*- coding: utf-8 -*-

import pytest
from tzf.pyramid_yml import scripts


def test_simplevalue():
    '''tests for simple value
    '''
    line = scripts.printer(1)
    # value passed should be represented by type in round parenthesis
    assert line == '1 (int)'


@pytest.mark.parametrize('configvalue, countlines', (
    ({'key': ['value', 'value 2']}, 3),  # list of values
    ({'key': ['value']}, 2),  # one element list of values
    ({'key': 'value', 'key2': 'value'}, 2),  # two keys
    ({'key': 'value'}, 1),  # simple key value
    ({'key': {'key2': 'value'}}, 2),  # composite key
))
def test_printer_list(configvalue, countlines):
    '''printer: key:[value:value]'''
    lines = scripts.printer(configvalue).split('\n')
    # should be three lines. one for key, and two for list
    assert len(lines) == countlines


conf_slicing = {'key': 'value', 'key2': {'key3': 'value'}}


@pytest.mark.parametrize('config, slice_key, sliced', (
    (conf_slicing, None, conf_slicing),
    (conf_slicing, 'key2', conf_slicing['key2']),
    (conf_slicing, 'key2.key3', conf_slicing['key2']['key3']),
))
def test_slice(config, slice_key, sliced):
    '''test no slice pass for config'''
    # configuration should be the same
    assert sliced == scripts._slice_config(config, slice_key)
