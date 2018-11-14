import unittest
from mr_utils.bart import Bartholomew as B

class BartholomewTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_traj(self):
        x,y = 256,64
        val = B.traj(x,y,a=1,G=True,q=[0,0,0])
        self.assertEqual((3,x,y),val.shape)

if __name__ == '__main__':
    unittest.main()
