# -*- coding: utf-8 -*-


def test_reading_prod(prod_app):
    '''Test whether prod config gets read
    '''
    #In this test with env=prod,
    #config.dev.yml will not be read (would be prod if existed
    assert prod_app.config.registry['config'].key.env == 'default'


def test_include(prod_app):
    '''Tests if includemes options runs include action for defined data.'''
    #Included module should set a key on registry
    assert 'includeme_method' in prod_app.config.registry
    #Values set by included module should be True
    assert prod_app.config.registry['includeme_method']
    #Not included, no key on registry
    assert 'includeme_method2' in prod_app.config.registry
    #Values set by included module should be True
    assert prod_app.config.registry['includeme_method2']
