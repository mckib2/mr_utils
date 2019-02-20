'''Tests for python PLANET implementation.'''

import unittest

import numpy as np

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET
from mr_utils.utils import fit_ellipse, check_fit

class TestPLANET(unittest.TestCase):
    '''PLANET sanity checks.'''

    def setUp(self):
        self.num_pc = 6
        self.I = np.zeros(self.num_pc, dtype='complex')
        self.pcs = [2*np.pi*n/self.num_pc for n in range(self.num_pc)]
        self.TR = 10e-3
        self.alpha = np.deg2rad(30)
        self.df = 1/(5*self.TR)
        self.T1 = 1.5
        self.T2 = .8
        self.T1s = np.linspace(.2, 2, 100)
        for ii, pc in enumerate(self.pcs):
            self.I[ii] = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                              phase_cyc=pc)

    def test_requires_6_phase_cycles(self):
        '''Make sure we can't continue without 6 phase-cycles.'''
        with self.assertRaises(AssertionError):
            PLANET(self.I[:5], self.alpha, self.TR, self.T1s)

    def test_ellipse_fit(self):
        '''Make sure we can fit an ellipse using complex ssfp data.'''
        c = fit_ellipse(self.I)
        self.assertTrue(np.allclose(
            check_fit(c, self.I), np.zeros(self.I.size)))

    def test_no_noise_case(self):
        '''Make sure we perform in ideal conditions.'''
        _Meff, T1, T2 = PLANET(self.I, self.alpha, self.TR, self.T1s)
        self.assertTrue(np.allclose([T1, T2], [self.T1, self.T2]))
