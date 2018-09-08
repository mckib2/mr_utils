import unittest
from mr_utils.sim.noise import rician,rayleigh,rayleigh_mean
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rayleigh as rayleigh_scipy

class RayleighNoiseTestCase(unittest.TestCase):

    def setUp(self):
        num_samples = 100
        self.M = np.linspace(0,7,num_samples)

    def test_rayleigh_low_noise(self):
        sigma = .8
        rv = rayleigh_scipy()
        pM_scipy = rv.pdf(self.M)
        # Expressions for dist are different in paper and scipy, correction
        # factor to convert between them
        pM_scipy *= np.exp(self.M**2/2 - self.M**2/(2*sigma**2))/(sigma**2)

        # Do ours
        pM = rayleigh(self.M,sigma)

        self.assertTrue(np.allclose(pM,pM_scipy))

    def test_rayleigh_high_noise(self):
        sigma = 20
        rv = rayleigh_scipy()
        pM_scipy = rv.pdf(self.M)
        # Expressions for dist are different in paper and scipy, correction
        # factor to convert between them
        pM_scipy *= np.exp(self.M**2/2 - self.M**2/(2*sigma**2))/(sigma**2)

        # Do ours
        pM = rayleigh(self.M,sigma)

        self.assertTrue(np.allclose(pM,pM_scipy))

    def test_rayleigh_is_rician_low_noise(self):
        # Rayleigh is special case of Rician (A=0)
        sigma = .8
        pM = rayleigh(self.M,sigma)
        pM_rician = rician(self.M,0,sigma)
        self.assertTrue(np.allclose(pM,pM_rician))

    def test_rayleigh_is_rician_high_noise(self):
        # Rayleigh is special case of Rician (A=0)
        sigma = 20
        pM = rayleigh(self.M,sigma)
        pM_rician = rician(self.M,0,sigma)
        self.assertTrue(np.allclose(pM,pM_rician))

    def test_rayleigh_mean_low_noise(self):
        sigma = .8
        rv = rayleigh_scipy()
        M_scipy = rv.mean()*sigma

        # Do ours
        M = rayleigh_mean(sigma)

        self.assertEqual(M,M_scipy)

    def test_rayleigh_mean_high_noise(self):
        sigma = 20
        rv = rayleigh_scipy()
        M_scipy = rv.mean()*sigma

        # Do ours
        M = rayleigh_mean(sigma)

        self.assertEqual(M,M_scipy)


if __name__ == '__main__':
    unittest.main()
