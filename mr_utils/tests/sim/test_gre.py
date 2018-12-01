import unittest
from mr_utils.sim.gre import spoiled_gre,ernst
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils import view
import numpy as np

class TestGRE(unittest.TestCase):

    def setUp(self):
        pass

    def test_spoiled_gre(self):

        T1s,T2s,PD = cylinder_2d()
        im = spoiled_gre(T1s,T2s,TR=.3,TE=.003,alpha=None,M0=PD)

        # All nonzero pixels should be the same magnitude
        self.assertTrue(np.all(np.diff(im[np.nonzero(im)]) == 0))
