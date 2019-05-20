'''Unit tests for generalized gradient descent.'''

import unittest

import numpy as np
from scipy.optimize import rosen, rosen_der

from mr_utils.cs import gd
from mr_utils.test_data import optimization_functions as of

class TestGradientDescent(unittest.TestCase):
    '''Sanity checks for GD.'''

    def setUp(self):
        pass

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

    def test_ackley(self):
        '''Test ackley function.'''

        d = 10
        x, _cost = gd(
            shape=(d,),
            updates=[lambda x0: of.grad_ackley(None, x0)],
            x0=np.ones(d)*-.5,
            alphas=None,
            costs=[of.ackley],
            maxiter=200,
            disp=False)

        self.assertTrue(np.allclose(x, np.zeros(d), atol=1e-7))

    def test_tv_image_recon(self):
        '''Try a simple TV constrained image recon.'''

        pass
