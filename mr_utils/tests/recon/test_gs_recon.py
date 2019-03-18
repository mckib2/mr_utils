'''Verification, validation of geometric solution to elliptical signal model.

Test solution against naive loop implementation, Hoff's MATLAB implementation,
and Taylor's MATLAB implementation.
'''

import unittest
import numpy as np
# from mr_utils import view

class GSReconTestCase(unittest.TestCase):
    '''Verify technical implementation of algorithm.'''

    def setUp(self):
        from mr_utils.sim.ssfp import ssfp

        self.TR = 6e-3
        self.T1, self.T2 = 1, .8
        self.alpha = np.pi/3

        # To get periodic banding like we want to see, we need some serious
        # field inhomogeneity.
        dim = 256
        min_df, max_df = 0, 500
        x = np.linspace(min_df, max_df, dim)
        y = np.zeros(dim)
        self.field_map, _ = np.meshgrid(x, y)

        # Get four phase cycled images
        self.I1 = ssfp(self.T1, self.T2, self.TR, self.alpha,
                       self.field_map, phase_cyc=0)
        self.I2 = ssfp(self.T1, self.T2, self.TR, self.alpha,
                       self.field_map, phase_cyc=np.pi/2)
        self.I3 = ssfp(self.T1, self.T2, self.TR, self.alpha,
                       self.field_map, phase_cyc=np.pi)
        self.I4 = ssfp(self.T1, self.T2, self.TR, self.alpha,
                       self.field_map, phase_cyc=3*np.pi/2)
        self.Is = ssfp(self.T1, self.T2, self.TR, self.alpha, self.field_map,
                       phase_cyc=[0, np.pi/2, np.pi, 3*np.pi/2])

    def test_gs_recon(self):
        '''Test matrix implementation against naive loop implementation.'''
        from mr_utils.recon.ssfp.gs_recon import gs_recon_for_loop, gs_recon

        # Make sure it doesn't matter if we go pixel by pixel or do the whole
        # matrix at once
        I0 = gs_recon_for_loop(self.I1, self.I2, self.I3, self.I4)
        I1 = gs_recon(self.Is)
        self.assertTrue(np.allclose(I0, I1))

    def test_max_magnitudes(self):
        '''Make sure we're indeed finding the maximum pixels.'''
        from mr_utils.recon.ssfp.gs_recon import get_max_magnitudes_for_loop
        from mr_utils.recon.ssfp.gs_recon import get_max_magnitudes

        # Make sure it doesn't matter if we go pixel by pixel or do the whole
        # matrix at once
        I0 = get_max_magnitudes_for_loop(self.I1, self.I2, self.I3, self.I4)
        I1 = get_max_magnitudes(self.I1, self.I2, self.I3, self.I4)
        self.assertTrue(np.allclose(I0, I1))

    def test_noisy_gs_recon(self):
        '''Add noise and make sure implementations are still identical.'''
        from mr_utils.recon.ssfp import gs_recon, gs_recon_for_loop

        # Add in gaussian noise on both real,imag channels
        m, std = 0, .08
        n = np.random.normal(m, std, size=self.Is.shape) + 1j*np.random.normal(
            m, std, size=self.Is.shape)
        n1 = n[0, ...]
        n2 = n[1, ...]
        n3 = n[2, ...]
        n4 = n[3, ...]

        I0 = gs_recon(self.Is + n)
        I1 = gs_recon_for_loop(
            self.I1 + n1, self.I2 + n2, self.I3 + n3, self.I4 + n4)
        self.assertTrue(np.allclose(I0, I1))

    def test_gs_recon3d(self):
        '''Make sure 3d recon gives same answer as running 2d on all slices.'''
        from mr_utils.recon.ssfp import gs_recon, gs_recon3d

        # Try individually
        I0 = gs_recon(self.Is)
        I0 = np.stack((I0, gs_recon(self.Is)), axis=-1)
        I1 = gs_recon3d(np.stack((self.I1, self.I1), axis=-1),
                        np.stack((self.I2, self.I2), axis=-1),
                        np.stack((self.I3, self.I3), axis=-1),
                        np.stack((self.I4, self.I4), axis=-1))
        self.assertTrue(np.allclose(I0, I1))


class GSReconKneeData(unittest.TestCase):
    '''Make sure our implementation matches output of Taylor knee recon.'''

    def setUp(self):
        from mr_utils.test_data import load_test_data

        path = 'mr_utils/test_data/tests/recon/ssfp/gs_recon/'
        files = ['I1', 'I2', 'I3', 'I4', 'I_max_mag', 'CS', 'Id', 'w13', 'w24',
                 'I']
        data = load_test_data(path, files)

        # Load in truth data
        self.I1 = data[0]
        self.I2 = data[1]
        self.I3 = data[2]
        self.I4 = data[3]
        self.Is = np.stack((data[:4]))
        self.I_max_mag = data[4]
        self.CS = data[5]
        self.Id = data[6]
        self.w13 = data[7]
        self.w24 = data[8]
        self.I = data[9]

    def test_max_magnitudes(self):
        '''Make sure max magnitues are the same as Taylor's implementation.'''
        from mr_utils.recon.ssfp.gs_recon import get_max_magnitudes

        # Make sure we both find the same maximum magnitude values
        I_max_mag_py = get_max_magnitudes(self.I1, self.I2, self.I3, self.I4)
        self.assertTrue(np.allclose(self.I_max_mag, I_max_mag_py))

    def test_complex_sum(self):
        '''Verify complex sum is the same as Taylor's implementation.'''
        from mr_utils.recon.ssfp import complex_sum

        CS_py = complex_sum(self.I1, self.I2, self.I3, self.I4)
        self.assertTrue(np.allclose(CS_py, self.CS))

    def test_direct_solution(self):
        '''Make sure first pass solution is the same as Taylor's.'''
        from mr_utils.sim.ssfp import get_complex_cross_point

        Id_py = get_complex_cross_point(self.Is)
        self.assertTrue(np.allclose(Id_py, self.Id))

    def test_weighted_combination(self):
        '''Make sure second pass solution is the same as Taylor's.'''
        from mr_utils.recon.ssfp import compute_Iw, \
            complex_sum, get_max_magnitudes, get_complex_cross_point
        Iw13 = self.I1*self.w13 + self.I3*(1 - self.w13)
        # Iw24 = self.I2*self.w24 + self.I4*(1 - self.w24)

        # A little processing to get where we need to to compare weighted combs
        Id = get_complex_cross_point(self.Is)
        CS = complex_sum(self.I1, self.I2, self.I3, self.I4)
        I_max_mag = get_max_magnitudes(self.I1, self.I2, self.I3, self.I4)
        mask = np.abs(Id) > I_max_mag
        Id[mask] = CS[mask]
        Iw13_py = compute_Iw(self.I1, self.I3, Id, patch_size=(5, 5))

        self.assertTrue(np.allclose(Iw13, Iw13_py))

    def test_gs_recon_knee(self):
        '''Verify the final solution matches Taylor's solution.'''
        from mr_utils.recon.ssfp import gs_recon

        I = gs_recon(np.stack((self.I1, self.I2, self.I3, self.I4)))
        self.assertTrue(np.allclose(I, self.I))

if __name__ == '__main__':
    unittest.main()
