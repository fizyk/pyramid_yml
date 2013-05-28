# -*- coding: utf-8 -*-

import unittest

from tzf.pyramid_yml import scripts


class PConfigTestCase(unittest.TestCase):

    def setUp(self):
        '''Configuring pconfig tests'''

    def test_printer_simple(self):
        '''printer: key:value'''

        lines = scripts.printer({'key': 'value'}).split('\n')

        self.assertEqual(len(lines), 1, 'Simple values should be placed in same line as key')

    def test_printer_two_keys_simple(self):
        '''printer: 2x key:value'''

        lines = scripts.printer({'key': 'value', 'key2': 'value'}).split('\n')

        self.assertEqual(len(lines), 2, 'There are only two key:value pairs')

    def test_printer_composite_key(self):
        '''printer: key:key:value'''

        lines = scripts.printer({'key': {'key2': 'value'}}).split('\n')

        self.assertEqual(len(lines), 2, 'should be only two lines')

    def test_simplevalue(self):
        '''tests for simple value'''
        line = scripts.printer(1)
        self.assertEqual(line, '1 (int)', 'value passed should be represented by type in round parenthesis')

    def test_printer_list(self):
        '''printer: key:[value:value]'''

        lines = scripts.printer({'key': ['value', 'value 2']}).split('\n')

        self.assertEqual(len(lines), 3, 'should be three lines. one for key, and two for list')

    def test_printer_list(self):
        '''printer: key:[value]'''

        lines = scripts.printer({'key': ['value']}).split('\n')
        self.assertEqual(len(lines), 2, 'should be three lines. one for key, and one for list')

    def test_slice_no_key(self):
        '''test no slice pass for config'''
        conf = {'key': 'value', 'key2': {'key3': 'value'}}
        self.assertEqual(conf, scripts._slice_config(conf, None), 'configuration should be the same')

    def test_slice_no_key(self):
        '''test one key slice for config'''
        conf = {'key': 'value', 'key2': {'key3': 'value'}}
        self.assertEqual(conf['key2'], scripts._slice_config(conf, 'key2'), 'configuration should be the same')

    def test_slice_no_key(self):
        '''test one key slice for config'''
        conf = {'key': 'value', 'key2': {'key3': 'value'}}
        self.assertEqual(conf['key2']['key3'], scripts._slice_config(
            conf, 'key2.key3'), 'configuration should be the same')
