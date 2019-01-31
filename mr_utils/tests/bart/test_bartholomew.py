'''Tests for Bartholomew, BART interface object.'''

import unittest
from mr_utils.bart import Bartholomew as B
from mr_utils.bart import BartholomewObject

class BartholomewTestCase(unittest.TestCase):
    '''Tests and sanity checks for your friendly, neighborhood Bartholomew.'''

    def setUp(self):
        pass

    def test_bartholomew_object(self):
        '''Make sure that B was imported as a BartholomewObject.'''
        self.assertEqual(type(B), BartholomewObject)

    def test_incorrect_function_name(self):
        '''Make sure we can catch invalid function name calls.'''
        with self.assertRaises(AttributeError):
            B.hello()

    def test_incorrect_position_args(self):
        '''Make sure we catch incorrect positional arguments.'''
        with self.assertRaises(Exception):
            B.traj(256, 256)

    def test_traj(self):
        '''Generate a traj and make sure it has the right shape.'''
        x, y = 256, 64
        val = B.traj(x=x, y=y, a=1, G=True, q=[0, 0, 0])
        self.assertEqual((3, x, y), val.shape)

if __name__ == '__main__':
    unittest.main()
