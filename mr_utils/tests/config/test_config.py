'''Unit tests for ProfileConfig.'''

import unittest
import os

from mr_utils.config import ProfileConfig

class ProfileConfigTestCase(unittest.TestCase):
    '''Sanity checks for generation of profiles.config.'''

    def setUp(self):
        self.filename = 'filenameonlytobeusedfortestingreally.conphig'

        try:
            os.remove(self.filename)
        except OSError:
            pass

        self.profile = ProfileConfig(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_create_profile(self):
        '''Create dummy profile and verify its existence.'''
        self.profile.create_profile('mine')
        with self.assertRaises(RuntimeError):
            self.profile.create_profile('mine')

    def test_get_val(self):
        '''Make sure default value is accessible through get_config_val.'''
        self.assertTrue(
            self.profile.get_config_val('gadgetron.host') == 'localhost')

    def test_activate_profile(self):
        '''Make sure that profiles can be activated.'''
        self.profile.create_profile('mine')
        self.profile.activate_profile('default')
        self.assertTrue(self.profile.active_profile == 'default')

        self.profile.activate_profile('mine')
        self.assertTrue(self.profile.active_profile == 'mine')

    def test_set_config(self):
        '''Set a configuration value.'''
        self.profile.create_profile('workcomp')
        self.profile.activate_profile('workcomp')
        self.profile.set_config({'gadgetron.port':8080})

        self.assertTrue(self.profile.get_config_val('gadgetron.port') == 8080)


if __name__ == '__main__':
    unittest.main()
