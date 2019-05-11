'''Unit tests for utils.Sparsify class.'''

import unittest

import numpy as np

from mr_utils.utils import Sparsify

class TestSparsify(unittest.TestCase):
    '''Sanity checks for sparsifying transforms.'''

    def setUp(self):
        # Do for 1 dimensional signal
        self.N = 100
        self.sig1d = np.random.random(self.N)
        self.S1d = Sparsify()

        # Do along 1 dimension of a 3 dimensional signal
        self.sig3d = np.random.random((self.N,)*3)
        self.S3d = Sparsify(axis=1)

    def test_1d_finite_differences(self):
        '''Make sure 1d signals work fine for finite differences.'''
        self.assertTrue(np.allclose(self.S1d.inverse_fd(
            self.S1d.forward_fd(self.sig1d)), self.sig1d))

    def test_1d_dct(self):
        '''Make sure 1d signals work fine for DCT.'''
        self.assertTrue(np.allclose(self.S1d.inverse_dct(
            self.S1d.forward_dct(self.sig1d)), self.sig1d))

    def test_1d_wavelet(self):
        '''Make sure 1d signals work fine for wavelet.'''
        self.assertTrue(np.allclose(self.S1d.inverse_wvlt(
            self.S1d.forward_wvlt(self.sig1d)), self.sig1d))

    def test_nD_1d_finite_differences(self):
        '''FD along 1 dimension of a multidimensional array.'''
        self.assertTrue(np.allclose(self.S3d.inverse_fd(
            self.S3d.forward_fd(self.sig3d)), self.sig3d))

    def test_nD_1d_dct(self):
        '''DCT along 1 dimension of a multidimensional array.'''
        self.assertTrue(np.allclose(self.S3d.inverse_dct(
            self.S3d.forward_dct(self.sig3d)), self.sig3d))

    def test_nD_1d_wavelet(self):
        '''Wavelet along 1 dimension of a multidimensional array.'''
        self.assertTrue(np.allclose(self.S3d.inverse_wvlt(
            self.S3d.forward_wvlt(self.sig3d)), self.sig3d))

if __name__ == '__main__':
    unittest.main()
