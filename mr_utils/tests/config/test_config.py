import unittest
from mr_utils.config import ProfileConfig
import os

class ProfileConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = 'filenameonlytobeusedfortestingreally.conphig'

        try:
            os.remove(self.filename)
        except:
            pass

        self.profile = ProfileConfig(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_create_profile(self):
        self.profile.create_profile('mine')
        with self.assertRaises(RuntimeError):
            self.profile.create_profile('mine')

    def test_get_val(self):
        self.assertTrue(self.profile.get_config_val('gadgetron.host') == 'localhost')

    def test_activate_profile(self):
        self.profile.create_profile('mine')
        self.profile.activate_profile('default')
        self.assertTrue(self.profile.active_profile == 'default')

        self.profile.activate_profile('mine')
        self.assertTrue(self.profile.active_profile == 'mine')

    def test_set_config(self):

        self.profile.create_profile('workcomp')
        self.profile.activate_profile('workcomp')
        self.profile.set_config({'gadgetron.port':8080})

        self.assertTrue(self.profile.get_config_val('gadgetron.port') == 8080)


if __name__ == '__main__':
    unittest.main()
