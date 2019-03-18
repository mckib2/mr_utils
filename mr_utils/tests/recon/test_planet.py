'''Tests for python PLANET implementation.'''

import unittest

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET
from mr_utils.utils import fit_ellipse_halir, fit_ellipse_fitzgibon, check_fit

class TestPLANET(unittest.TestCase):
    '''PLANET sanity checks.'''

    def setUp(self):
        self.num_pc = 6
        self.pcs = [2*np.pi*n/self.num_pc for n in range(self.num_pc)]
        self.TR = 10e-3
        self.alpha = np.deg2rad(30)
        self.df = 1/(5*self.TR)
        self.T1 = 1.5
        self.T2 = .8
        self.T1s = np.linspace(.2, 2, 100)
        self.I = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                      phase_cyc=self.pcs)

    def test_ellipse_fit(self):
        '''Make sure we can fit an ellipse using complex ssfp data.'''
        c = fit_ellipse_halir(self.I.real, self.I.imag)
        self.assertTrue(np.allclose(
            check_fit(c, self.I.real, self.I.imag), np.zeros(self.I.size)))

        # Try with alternative method
        c = fit_ellipse_fitzgibon(self.I.real, self.I.imag)
        self.assertTrue(np.allclose(
            check_fit(c, self.I.real, self.I.imag), np.zeros(self.I.size)))

    def test_no_noise_case(self):
        '''Make sure we perform in ideal conditions.'''
        _Meff, T1, T2 = PLANET(self.I, self.alpha, self.TR, T1s=self.T1s,
                               disp=True)
        self.assertTrue(np.allclose([T1, T2], [self.T1, self.T2]))
