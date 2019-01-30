import unittest
import numpy as np
from mr_utils import view

class TestAMP(unittest.TestCase):

    def setUp(self):
        from mr_utils.test_data import AMPData
        from mr_utils.cs.models import UFT

        self.x0 = AMPData.x0()
        self.y = AMPData.y()
        self.mask = AMPData.mask()
        self.cdf97,self.level = AMPData.cdf97()
        self.uft = UFT(self.mask)

    def test_uft(self):
        '''Test undersampled fourier encoding.'''

        y0 = self.uft.forward_ortho(self.x0)
        self.assertTrue(np.allclose(self.y,y0))

    def test_wavelet_decomposition(self):

        import pywt
        from mr_utils.utils import cdf97_2d_forward,cdf97_2d_inverse
        wavelet_transform,locations = cdf97_2d_forward(self.x0,self.level)

        # Check 'em out
        view(np.stack((np.log(np.abs(self.cdf97)),np.log(np.abs(wavelet_transform)))))
        view(np.stack((self.cdf97 - wavelet_transform)),log=True)

        # Make sure we can go back
        view(cdf97_2d_inverse(wavelet_transform,locations))

        self.assertTrue(np.allclose(wavelet_transform,self.cdf97))

if __name__ == '__main__':
    unittest.main()
