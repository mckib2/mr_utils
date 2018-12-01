import unittest
from mr_utils.load_data import pyport
from mr_utils.test_data import bssfp_phantom

class PyPortTestCase(unittest.TestCase):

    def setUp(self):
        self.sample = bssfp_phantom

    def test_pyport(self):

        args = {
            'version': False,
            'list': True,
            'extract': None,
            'user_stylesheet': None,
            'file': self.sample,
            'pMapStyle': None,
            'measNum': 1,
            'pMap': None,
            'user_map': None,
            'debug': False
        }

        pyport.main(args)

if __name__ == '__main__':
    unittest.main()
