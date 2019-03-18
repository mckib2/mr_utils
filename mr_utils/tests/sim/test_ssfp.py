'''Test cases for SSFP simulation.'''

import unittest

import numpy as np
# import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp, ssfp_dictionary, make_cart_ellipse, \
    ssfp_dictionary_for_loop, find_atom, ssfp_from_ellipse, \
    elliptical_params, get_cart_elliptical_params, get_center_of_mass, \
    get_center_of_mass_nmr, spectrum, get_cross_point, \
    get_complex_cross_point

class DictionaryTestCase(unittest.TestCase):
    '''Look up df in a dictionary of T1,T2,alpha.'''

    def setUp(self):
        # Haystack
        self.TR = 6e-6
        self.T1s = np.linspace(0, 1, 11)[1:] # T1 can't be 0
        self.T2s = np.linspace(0, 1, 11)[1:] # T2 can't be 0
        self.alphas = np.linspace(np.pi/3, 2*np.pi/3, 10)
        self.df = np.linspace(-1/self.TR, 1/self.TR, 100)

        # Needle
        self.T10 = self.T1s[6]
        self.T20 = self.T2s[3]
        self.alpha0 = self.alphas[5]

    def test_dictionary(self):
        '''Verify implementation against a naive loop implementation.'''

        # Make sure we get the same answer whether we build dictionary from
        # matrix operations or iterate through a for loop:
        D0, keys0 = ssfp_dictionary(self.T1s, self.T2s, self.TR, self.alphas,
                                    self.df)
        D1, keys1 = ssfp_dictionary_for_loop(self.T1s, self.T2s, self.TR,
                                             self.alphas, self.df)
        self.assertTrue(np.allclose(keys0, keys1))
        self.assertTrue(np.allclose(D0, D1))

        # # Look at the dictionary
        # plt.plot(np.abs(D0.T))
        # plt.plot(np.abs(D1.T), '--')
        # plt.show()

    def test_find_atom(self):
        '''Test method that finds atom in a given dictionary.'''

        D, keys = ssfp_dictionary(
            self.T1s, self.T2s, self.TR, self.alphas, self.df)
        sig = ssfp(self.T10, self.T20, self.TR, self.alpha0, self.df)
        found_params = find_atom(sig, D, keys)
        actual_params = np.array([self.T10, self.T20, self.alpha0])

        self.assertTrue(np.allclose(actual_params, found_params))

class EllipticalSignalTestCase(unittest.TestCase):
    '''Test elliptical signal model functions against cartesian, NMR funcs.'''

    def setUp(self):
        self.TR = 6e-3
        self.T1, self.T2 = 1, .8
        self.alpha = np.pi/3
        self.df = 100

    def test_ssfp_sim(self):
        '''Generate signal from bSSFP signal eq and elliptical model.'''

        # Do it the "normal" way
        I0 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df)

        # Now do it using the elliptical model
        M, a, b = elliptical_params(self.T1, self.T2, self.TR, self.alpha)
        I1 = ssfp_from_ellipse(M, a, b, self.TR, self.df)

        self.assertTrue(np.allclose(I0, I1))

    def test_make_ellipse(self):
        '''Make an ellipse given NMR params and elliptical params.'''

        M, a, b = elliptical_params(self.T1, self.T2, self.TR, self.alpha)
        xc, yc, A, B = get_cart_elliptical_params(M, a, b)
        x, y = make_cart_ellipse(xc, yc, A, B)

        res = np.zeros(x.shape)
        for ii in range(x.size):
            res[ii] = (x[ii] - xc)**2/A**2 + (y[ii] - yc)**2/B**2

        # (x - xc)**2/A**2 + (y - yc)**2/B**2 == 1
        # Make sure generated x,y satisfy equation for an ellipse
        self.assertTrue(np.allclose(res, np.ones(res.shape)))

    def test_center_of_mass(self):
        '''Make sure we can find the center of mass of an ellipse.'''

        M, a, b = elliptical_params(self.T1, self.T2, self.TR, self.alpha)
        cm0 = get_center_of_mass(M, a, b)
        cm1 = get_center_of_mass_nmr(self.T1, self.T2, self.TR, self.alpha)

        self.assertTrue(np.allclose(cm0, cm1))

    def test_spectrum(self):
        '''Generate bSSFP spectrum.'''

        # This is mostly just to show how it's used
        _sig = spectrum(self.T1, self.T2, self.TR, self.alpha)
        # plt.subplot(2,1,1)
        # plt.plot(np.abs(sig))
        # plt.subplot(2,1,2)
        # plt.plot(np.angle(sig))
        # plt.show()

    def test_banding_sim_2d(self):
        '''Make sure banding looks the same coming from NMR params and ESM.'''

        # To get periodic banding like we want to see, we need some serious
        # field inhomogeneity.
        dim = 256
        min_df, max_df = 0, 500
        x = np.linspace(min_df, max_df, dim)
        y = np.zeros(dim)
        field_map, _ = np.meshgrid(x, y)

        # # Show the field map
        # plt.imshow(field_map)
        # plt.show()

        # # Generate simulated banding image explicitly using NMR parameters
        sig0 = ssfp(self.T1, self.T2, self.TR, self.alpha, field_map)
        # plt.subplot(2,1,1)
        # plt.imshow(np.abs(sig0))
        # plt.subplot(2,1,2)
        # plt.plot(np.abs(sig0[int(dim/2),:]))
        # plt.show()

        # Generate simulated banding image using elliptical signal model
        M, a, b = elliptical_params(self.T1, self.T2, self.TR, self.alpha)
        sig1 = ssfp_from_ellipse(M, a, b, self.TR, field_map)

        self.assertTrue(np.allclose(sig0, sig1))

    def test_cross_point(self):
        '''Find cross point from cartesian and ESM function.'''

        # Get four phase cycled images
        I1 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                  phase_cyc=0)
        I2 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                  phase_cyc=np.pi/2)
        I3 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                  phase_cyc=np.pi)
        I4 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                  phase_cyc=3*np.pi/2)
        Is = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df,
                  phase_cyc=[0, np.pi/2, np.pi, 3*np.pi/2])

        # Find cross points
        x0, y0 = get_cross_point(I1, I2, I3, I4)
        M = get_complex_cross_point(Is)

        # Make sure we get the same answer
        self.assertTrue(np.allclose(x0 + 1j*y0, M))

class MultiplePhaseCycleTestCase(unittest.TestCase):
    '''Compute multiple phase-cycles at once.'''

    def setUp(self):
        self.TR = 6e-3
        self.T1, self.T2 = 1, .8
        self.alpha = np.pi/3
        self.df = 100

    def test_two_phase_cycles_single_point(self):
        '''Try doing two phase-cycles.'''

        # Gold standard is computing them individually
        pcs = np.linspace(0, 2*np.pi, 2, endpoint=False)
        I0 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df, pcs[0])
        I1 = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df, pcs[1])
        Itrue = np.stack((I0, I1))

        # Now try all at once
        Is = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df, pcs)

        self.assertTrue(np.allclose(Itrue, Is))

    def test_many_phase_cycles_single_point(self):
        '''Make sure we can do a bunch of them at once.'''

        pcs = np.linspace(0, 2*np.pi, 16, endpoint=False)
        Itrue = np.zeros(pcs.size, dtype='complex')
        for ii, pc in np.ndenumerate(pcs):
            Itrue[ii] = ssfp(
                self.T1, self.T2, self.TR, self.alpha, self.df, pc)

        Is = ssfp(self.T1, self.T2, self.TR, self.alpha, self.df, pcs)
        self.assertTrue(np.allclose(Itrue, Is))

    def test_two_phase_cycles_multiple_point(self):
        '''Now make MxN param maps and simulate multiple phase-cycles.'''

        M, N = 10, 5
        T1s = np.ones((M, N))*self.T1
        T2s = np.ones((M, N))*self.T2
        alphas = np.ones((M, N))*self.alpha

        # Linear gradient for field map
        min_df, max_df = 0, 200
        fx = np.linspace(min_df, max_df, N)
        fy = np.zeros(M)
        df, _ = np.meshgrid(fx, fy)

        # Gold standard is again, computing individually
        pcs = np.linspace(0, 2*np.pi, 2, endpoint=False)
        I0 = ssfp(T1s, T2s, self.TR, alphas, df, pcs[0])
        I1 = ssfp(T1s, T2s, self.TR, alphas, df, pcs[1])
        Itrue = np.stack((I0, I1))

        # Now try doing all at once
        # reps = (pcs.size, 1, 1)
        # pcs = np.tile(pcs, T1s.shape[:] + (1,)).transpose((2, 0, 1))
        # T1s = np.tile(T1s, reps)
        # T2s = np.tile(T2s, reps)
        # alphas = np.tile(alphas, reps)
        # df = np.tile(df, reps)
        # print(T1s.shape, T2s.shape, alphas.shape, df.shape, pcs.shape)

        Is = ssfp(T1s, T2s, self.TR, alphas, df, pcs)

        # from mr_utils import view
        # view(np.vstack((Itrue, Is)))

        # print(Itrue.shape, Is.shape)

        self.assertTrue(np.allclose(Itrue, Is))

if __name__ == '__main__':
    unittest.main()
