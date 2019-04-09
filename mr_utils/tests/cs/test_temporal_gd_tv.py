'''Tests against MATLAB output for temporal_gd_tv().'''

import unittest

import numpy as np

from mr_utils.test_data import load_test_data
from mr_utils.cs.convex.temporal_gd_tv.generate_prior import (
    generate_prior)
from mr_utils.cs.convex.temporal_gd_tv.sort_real_imag_parts import (
    sort_real_imag_parts)
from mr_utils.cs import GD_temporal_TV
from mr_utils.cs.models import UFT
from mr_utils import view

class TestTemporalGDTV(unittest.TestCase):
    '''Make sure output of function matches MATLAB output.'''

    @classmethod
    def setUpClass(cls):
        # Point self to cls so we can use it like in a normal method
        self = cls

        # Load in test data
        self.path = ('mr_utils/test_data/tests/cs/convex/'
                     'temporal_gd_tv')
        self.Coil, self.mask = load_test_data(
            self.path, ['Coil6', 'mask'])

        # For some reason they are the wrong dimensions coming out
        # of MATLAB, probably because they are old format
        self.Coil = self.Coil.T
        self.mask = self.mask.T

        # Set the recon parameters
        self.weight_fidelity = 1
        self.weight_temporal = .01
        self.beta_sqrd = 0.0000001
        self.niter = 200

        # Get an encoding model
        self.uft = UFT(self.mask, axes=(0, 1))

        # Compute reduced kspace
        self.reduced_kspace = self.Coil*self.mask

        # Compute prior
        self.prior = generate_prior(
            self.Coil*self.mask, self.uft.inverse_s)

        # Compute monotonic sort order
        (self.sort_order_real,
         self.sort_order_imag) = sort_real_imag_parts(
             self.prior, axis=-1)

        # Compute measured image domain
        self.measuredImgDomain = self.uft.inverse_s(
            self.reduced_kspace)

        # Get reduced data, whatever that is
        self.reduced_data = np.abs(self.measuredImgDomain)

        # Get initial estimates
        self.img_est = self.measuredImgDomain.copy()
        self.W_img_est = self.measuredImgDomain.copy()

        # Construct R and C (rows and columns, I assume)
        rows, cols, pages = self.img_est.shape[:]
        self.R = np.tile(
            np.arange(rows), (cols, pages, 1)).transpose((2, 0, 1))
        self.C = np.tile(
            np.arange(cols), (rows, pages, 1)).transpose((0, 2, 1))

        # From R and C get the indices we'll actually use
        self.nIdx_real = self.R + self.C*rows + (
            self.sort_order_real)*rows*cols
        self.nIdx_imag = self.R + self.C*rows + (
            self.sort_order_imag)*rows*cols

    def test_reduced_kspace(self):
        '''Verify reduced_kspace variable is the same as MATLAB'''

        reduced_kspace_true = load_test_data(
            self.path, ['reduced_kspace'])
        self.assertTrue(
            np.allclose(self.reduced_kspace, reduced_kspace_true))

    def test_generate_prior(self):
        '''Verify prior variable is the same as MATLAB'''

        prior_true = load_test_data(self.path, ['prior'], )
        self.assertTrue(np.allclose(self.prior, prior_true))

    def test_monotonic_sort_real_imag_parts(self):
        '''Verify sort orders are the same as MATLAB'''

        real_true, imag_true = load_test_data(
            self.path, ['sort_order_real', 'sort_order_imag'])
        # 0-based indexing
        real_true -= 1
        imag_true -= 1
        self.assertTrue(np.alltrue(self.sort_order_real == real_true))
        self.assertTrue(np.alltrue(self.sort_order_imag == imag_true))

    def test_measuredImgDomain(self):
        '''Verify measuredImgDomain variable same as MATLAB'''

        mid = load_test_data(self.path, ['measuredImgDomain'])
        self.assertTrue(np.allclose(self.measuredImgDomain, mid))

    def test_reduced_data(self):
        '''Verify reduced_data variable same as MATLAB'''

        reduced_data = load_test_data(self.path, ['reduced_data'])
        self.assertTrue(np.allclose(self.reduced_data, reduced_data))

    def test_R_and_C(self):
        '''Verify R, C variables are the same as MATLAB'''

        R, C = load_test_data(self.path, ['R', 'C'])
        self.assertTrue(np.allclose(self.R, R-1))
        self.assertTrue(np.allclose(self.C, C-1))

    def test_nIdx_real_and_imag(self):
        '''Verify nIdx_real/imag variables are the same as MATLAB'''

        real, imag = load_test_data(
            self.path, ['nIdx_real', 'nIdx_imag'])

        # print(np.unravel_index(self.nIdx_real, self.prior.shape))

        self.assertTrue(np.allclose(self.nIdx_real, real-1))
        self.assertTrue(np.allclose(self.nIdx_imag, imag-1))

    def test_recon(self):
        '''See if the full recon matches the MATLAB output'''

        recon = GD_temporal_TV(
            self.prior, self.reduced_kspace, self.mask,
            self.weight_fidelity, self.weight_temporal,
            self.uft.forward_s, self.uft.inverse_s, x=self.Coil)
        view(recon)

if __name__ == '__main__':
    unittest.main()
