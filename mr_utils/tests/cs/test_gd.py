'''Unit tests for generalized gradient descent.'''

import unittest

import numpy as np
from scipy.optimize import rosen, rosen_der
from skimage.measure import compare_ssim

from mr_utils.cs import gd
from mr_utils.test_data import optimization_functions as of
from mr_utils.cs.models import UFT
from mr_utils.sim.traj import radial
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.utils import dTV

class TestGradientDescent(unittest.TestCase):
    '''Sanity checks for GD.'''

    def setUp(self):
        pass

    # @unittest.skip('Skip while debugging image recon')
    def test_quadratic(self):
        '''Simple quadratic function test.'''

        x, _cost = gd(
            shape=(1,),
            updates=[lambda x0: of.grad_quadratic(None, x0)],
            x0=np.ones(1)*5,
            alphas=None,
            costs=[of.quadratic],
            maxiter=200)

        self.assertTrue(np.allclose(x[0], 9/4))

    @unittest.skip('Takes a long time to converge.')
    def test_rosenbrock(self):
        '''Test Rosenbrock's function.'''

        x, _cost = gd(
            shape=(2,),
            updates=[rosen_der],
            x0=None,
            alphas=None,
            costs=[rosen],
            maxiter=5000,
            disp=False)
        self.assertTrue(np.allclose(x, np.ones(2), atol=1e-2))

    # @unittest.skip('Skip while debugging image recon')
    def test_ackley(self):
        '''Test ackley function.'''

        d = 10
        x, _cost = gd(
            shape=(d,),
            updates=[lambda x0: of.grad_ackley(None, x0)],
            x0=np.ones(d)*-.5, # need to start close to find minimum
            alphas=None,
            costs=[of.ackley],
            maxiter=200,
            disp=False)

        self.assertTrue(np.allclose(x, np.zeros(d), atol=1e-7))

    def test_tv_image_recon(self):
        '''Try a simple TV constrained image recon.'''

        N = 64
        im = binary_smiley(N)

        num_spokes = 16
        mask = radial(im.shape, num_spokes)
        uft = UFT(mask)

        kspace_u = uft.forward_ortho(im)
        imspace_u = uft.inverse_ortho(kspace_u)

        fid = lambda x0: np.linalg.norm(
            uft.forward_ortho(x0) - kspace_u)**2
        fid_grad = lambda x0: uft.inverse_ortho(
            uft.forward_ortho(x0)) - imspace_u

        tv = lambda x0: np.linalg.norm(
            np.diff(np.diff(np.abs(x0)**2, axis=1), axis=0), ord=1)
        tv_grad = lambda x0: dTV(x0)

        x, _cost = gd(
            shape=im.shape,
            updates=[fid_grad, tv_grad],
            x0=imspace_u,
            alphas=[1, .002],
            costs=[fid, tv],
            maxiter=700,
            disp=False)

        ssim = compare_ssim(np.abs(im), np.abs(x))
        self.assertTrue(ssim > .9)
