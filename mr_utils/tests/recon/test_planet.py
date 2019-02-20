'''Tests for python PLANET implementation.'''

import unittest

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.utils import fit_ellipse, check_fit

class TestPLANET(unittest.TestCase):
    '''PLANET sanity checks.'''

    def setUp(self):
        self.num_pc = 6
        self.I = np.zeros(self.num_pc, dtype='complex')
        self.pcs = [2*np.pi*n/self.num_pc for n in range(self.num_pc)]
        TR = 3e-3
        for ii, pc in enumerate(self.pcs):
            self.I[ii] = ssfp(1.5, .8, TR, np.pi/5, 1/(2*TR), pc)

    def test_ellipse_fit(self):
        '''Make sure we can fit an ellipse using complex ssfp data.'''
        c = fit_ellipse(self.I)
        self.assertTrue(np.allclose(
            check_fit(c, self.I), np.zeros(self.I.size)))
