'''Test generation of Rician noise.'''

import unittest

import numpy as np
from scipy.stats import rice

from mr_utils.sim.noise import rician

class RicianNoiseTestCase(unittest.TestCase):
    '''Tests against scipy's statistics module.'''

    def setUp(self):
        num_samples = 100
        self.M = np.linspace(0, 7, num_samples)
        self.A = 2

        # The expressions for the rician pdf from paper and scipy docs are
        # different, use this to convert between them
        self.correction = lambda sigma: np.exp(-self.A**2/(2*sigma**2) + \
            self.A**2/2 + self.M**2/(2*sigma**4) - self.M**2/(2*sigma**2))

    def test_rician_low_noise(self):
        '''Verify low noise case against scipy statistics module.'''
        # Generate rician distribution with low noise
        # sigma too small will blow up the correction term for scipy rice.pdf
        # function (see sigma**4 term in denominator)
        sigma = .8

        # Try out ours
        pM = rician(self.M, self.A, sigma)

        # Compare to scipy implementation
        rv = rice(self.A)
        pM_scipy = rv.pdf(self.M/(sigma**2))*self.correction(sigma)

        # # Take a gander
        # plt.plot(pM,label='Rician')
        # plt.plot(pM_scipy,label='Rice (scipy)')
        # plt.plot(pM - pM_scipy)
        # plt.legend()
        # plt.show()

        self.assertTrue(np.allclose(pM, pM_scipy))

    def test_rician_high_noise(self):
        '''Verify high noise case against scipy statistics module.'''
        # Generate rician distribution with high noise
        # High noise is where the correction term counts!
        sigma = 20

        # Try out ours
        pM = rician(self.M, self.A, sigma)

        # Compare to scipy implementation
        rv = rice(self.A)
        pM_scipy = rv.pdf(self.M/(sigma**2))
        # Should fail with no correction
        self.assertFalse(np.allclose(pM, pM_scipy))

        # Now correct
        pM_scipy *= self.correction(sigma)
        self.assertTrue(np.allclose(pM, pM_scipy))

        # # Take a gander
        # plt.plot(pM,label='Rician')
        # plt.plot(pM_scipy,label='Rice (scipy)')
        # plt.plot(pM - pM_scipy)
        # plt.legend()
        # plt.show()

if __name__ == '__main__':
    unittest.main()
