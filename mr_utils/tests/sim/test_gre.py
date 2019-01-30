'''Test GRE contrast simulations.'''

import unittest

import numpy as np

from mr_utils.sim.gre import spoiled_gre, gre_sim, gre_sim_loop
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp

class TestGRE(unittest.TestCase):
    '''Verify GRE simulations against various implementations.'''

    def setUp(self):
        self.T1s, self.T2s, self.PD = cylinder_2d()

        self.alpha = np.pi/3
        self.TR, self.TE = 12e-3, 6e-3

    def test_spoiled_gre(self):
        '''Sanity check -- all nonzero pixels should be the same intensity.'''
        im = spoiled_gre(
            self.T1s, self.T2s, TR=.3, TE=.003, alpha=None, M0=self.PD)
        # All nonzero pixels should be the same magnitude
        self.assertTrue(np.all(np.diff(im[np.nonzero(im)]) == 0))

    def test_gre_sim_mat_against_gre_sim_loop(self):
        '''Verify against loop implementation.'''
        T1s, T2s, PD = cylinder_2d(dims=(16, 16))
        dphi = np.pi
        im1 = gre_sim_loop(T1s, T2s, TR=self.TR, TE=self.TE, alpha=self.alpha,
                           field_map=None, dphi=dphi, M0=PD, maxiter=50)
        im2 = gre_sim(T1s, T2s, TR=self.TR, TE=self.TE, alpha=self.alpha,
                      field_map=None, dphi=dphi, M0=PD, maxiter=50)
        self.assertTrue(np.allclose(np.abs(im1), np.abs(im2)))

    def test_gre_sim_against_closed_form_solution(self):
        '''Verify iterative solution against closed form solution.

        Uses fixed number of iterations.
        '''
        im1 = spoiled_gre(self.T1s, self.T2s, TR=self.TR, TE=self.TE,
                          alpha=self.alpha, M0=self.PD)
        im2 = gre_sim(self.T1s, self.T2s, TR=self.TR, TE=self.TE,
                      alpha=self.alpha, field_map=None, M0=self.PD, maxiter=10)

        # same within a scale factor...
        val = np.abs(im1) - np.abs(im2)
        self.assertTrue(np.all(np.diff(val[np.nonzero(val)]) == 0))

    def test_gre_sim_using_tol_against_closed_form_sol(self):
        '''Verify iterative solution against closed form solution.

        Used tolerance instead of fixed number of iterations.
        '''
        im1 = spoiled_gre(self.T1s, self.T2s, TR=self.TR, TE=self.TE,
                          alpha=self.alpha, M0=self.PD)
        im2 = gre_sim(self.T1s, self.T2s, TR=self.TR, TE=self.TE,
                      alpha=self.alpha, field_map=None, M0=self.PD, tol=1)

        # same within a scale factor...
        val = np.abs(im1) - np.abs(im2)
        self.assertTrue(np.all(np.diff(val[np.nonzero(val)]) == 0))

    def test_gre_unspoiled_and_bssfp(self):
        '''Very balanced steady state solution.'''
        M0, T1, T2 = 5.0, 1.0, .5
        im1 = gre_sim(T1, T2, TR=self.TR, TE=self.TR/2, alpha=self.alpha,
                      field_map=np.zeros(1), M0=M0, spoil=False, maxiter=200)
        im2 = ssfp(T1, T2, TR=self.TR, alpha=self.alpha, field_map=np.zeros(1),
                   phase_cyc=0, M0=M0)

        # Currently failing...
        self.assertEqual(im1, im2)
