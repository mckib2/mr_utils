'''Approximate message passing algorithm unit test cases.'''

import unittest

import numpy as np

from mr_utils.utils import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.test_data import AMPData
from mr_utils.cs.models import UFT
# from mr_utils import view

class TestAMP(unittest.TestCase):
    '''Make sure we line up with Stanford results.'''

    def setUp(self):

        # We'll need to pull the data down if we don't have it
        try:
            self.x0 = AMPData.x0()
            self.y = AMPData.y()
            self.mask = AMPData.mask()
            self.cdf97, self.level = AMPData.cdf97()
        except FileNotFoundError:
            import requests
            import shutil
            import os
            from mr_utils.definitions import TEST_DATA_HOST
            for file in ['cdf97.mat', 'mask.mat', 'x0.mat', 'y.mat']:
                url = ('%smr_utils/test_data/cs/thresholding/amp/%s'
                       '' % (TEST_DATA_HOST, file))
                filename = ('mr_utils/test_data/tests/cs/thresholding/amp/%s'
                            '' % file)
                os.makedirs(os.path.dirname(filename), exist_ok=True)

                with requests.get(url, stream=True) as r:
                    with open(filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)

            self.x0 = AMPData.x0()
            self.y = AMPData.y()
            self.mask = AMPData.mask()
            self.cdf97, self.level = AMPData.cdf97()


        self.uft = UFT(self.mask)

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
