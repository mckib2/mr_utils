'''Approximate message passing algorithm unit test cases.'''

import unittest

import numpy as np

from mr_utils.utils import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.test_data import load_test_data
from mr_utils.cs.models import UFT

class TestAMP(unittest.TestCase):
    '''Make sure we line up with Stanford results.'''

    def setUp(self):
        data = load_test_data('mr_utils/test_data/tests/cs/thresholding/amp',
                              ['cdf97', 'mask', 'x0', 'y'])
        self.cdf97, self.mask, self.x0, self.y = data[:] #pylint: disable=W0632
        self.uft = UFT(self.mask)
        self.level = 5

    def test_uft(self):
        '''Test undersampled fourier encoding.'''

        y0 = self.uft.forward_ortho(self.x0)
        self.assertTrue(np.allclose(self.y, y0))

    @unittest.skip('Currently do not know how to match cdf97 using pywavelets')
    def test_wavelet_decomposition(self):
        '''Make sure we decompose using the same wavelet transformation.'''

        wavelet_transform, locations = cdf97_2d_forward(self.x0, self.level)

        # # Check 'em out
        # view(np.stack((np.log(np.abs(self.cdf97)),
        #                np.log(np.abs(wavelet_transform)))))
        # view(np.stack((self.cdf97 - wavelet_transform)), log=True)
        #
        # # Make sure we can go back
        inverse = cdf97_2d_inverse(wavelet_transform, locations)
        self.assertTrue(np.allclose(self.x0, inverse))
        # view(self.x0 - inverse)
        # view(cdf97_2d_inverse(wavelet_transform, locations))

        # Currently failing...
        self.assertTrue(np.allclose(wavelet_transform, self.cdf97))

if __name__ == '__main__':
    unittest.main()
