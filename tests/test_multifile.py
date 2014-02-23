
def test_multifolder(multifolder_config):
    '''
    Checks if files from 2nd folder had been loaded
    '''

    assert 'key_config2' in multifolder_config.registry['config']
