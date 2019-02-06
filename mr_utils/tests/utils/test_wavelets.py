'''Make sure wavelet transforms work the way we want them to.'''

import unittest

import numpy as np

from mr_utils.utils.wavelet import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.utils.wavelet import wavelet_forward, wavelet_inverse
from mr_utils.test_data.phantom import binary_smiley

class TestCDF97Wavelets(unittest.TestCase):
    '''Make sure CDF 9/7 wavelets do what they're supposed to.'''

    def setUp(self):
        self.im = binary_smiley(512)

    def test_forward_inverse(self):
        '''Test forward transform invertibility.'''
        forward, locs = cdf97_2d_forward(self.im, level=5)
        inverse = cdf97_2d_inverse(forward, locs)
        self.assertTrue(np.allclose(inverse, self.im))


    def test_max_level(self):
        '''Make sure we clip the level at the high end.'''
        with self.assertWarns(Warning):
            high_level = np.random.randint(6, 10)
            forward, _locs = cdf97_2d_forward(self.im, level=high_level)
        forward_check, _locs = cdf97_2d_forward(self.im, level=5)
        self.assertTrue(np.allclose(forward, forward_check))

class TestWavelets(unittest.TestCase):
    '''Make sure that arbitrary wavelet transforms can be performed.'''

    def setUp(self):
        self.im = np.random.randn(512, 512)

    def test_forward_inverse(self):
        '''Test forward transform invertibility.'''
        forward, locs = wavelet_forward(
            self.im, 'bior4.4', mode='periodization', level=5)
        inverse = wavelet_inverse(
            forward, locs, 'bior4.4', mode='periodization')
        self.assertTrue(np.allclose(inverse, self.im))

    def test_max_level(self):
        '''Make sure we clip the level at the high end.'''
        with self.assertWarns(Warning):
            high_level = np.random.randint(6, 10)
            f, _locs = wavelet_forward(
                self.im, 'bior4.4', mode='periodization', level=high_level)
        f_check, _locs = wavelet_forward(
            self.im, 'bior4.4', mode='periodization', level=5)
        self.assertTrue(np.allclose(f, f_check))

if __name__ == '__main__':
    unittest.main()
