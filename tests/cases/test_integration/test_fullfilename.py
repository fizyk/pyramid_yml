# -*- coding: utf-8 -*-


def test_reading(prod_fullfile_app):
    '''Test whether config by full path gets read'''

    #In this test with env=prod,
    #config.dev.yml will not be read (would be prod if existed
    assert 'key' in prod_fullfile_app.config.registry['config']
