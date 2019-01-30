'''Validate perfomance of gradient descent algorithm.'''

import unittest

import numpy as np

from mr_utils.test_data import optimization_functions as of
from mr_utils.optimization import gd, fd_complex_step

class TestGD(unittest.TestCase):
    '''Using example optimization functions, demonstrate that GD can optimize.
    '''

    def setUp(self):
        pass

    def test_quadratic(self):
        '''Simple quadratic function with min at 9/4.'''
        x0 = 6
        x, _iter = gd(of.quadratic, fd_complex_step, x0, alpha=None)
        self.assertTrue(np.allclose(x, 9/4))

    def test_maxiter(self):
        '''Make sure that hitting maxiter raises a warning.'''
        x0 = 6
        num_iter = 5
        with self.assertWarnsRegex(Warning, 'GD hit maxiters!'):
            _x, _iter = gd(of.quadratic, fd_complex_step, x0, maxiter=num_iter)
        # self.assertEqual(iter, num_iter)

    # def test_rosenbrock(self):
    #     x0 = np.zeros(2)
    #     x,iter = gd(of.rosenbrock,fd_complex_step,x0)
    #     self.assertTrue(np.allclose(x,np.ones(x.shape)))

    def test_rastrigin(self):
        '''Rastrigin function with min at 0.'''
        x0 = np.ones(10)
        x, _iter = gd(of.rastrigin, fd_complex_step, x0)
        self.assertTrue(np.allclose(x, np.zeros(x.shape)))

    def test_ackley(self):
        '''Ackley function with min at 0.'''
        # This has many minima, make sure we only get the closest one
        x0 = np.zeros(10)
        x, _iter = gd(of.ackley, of.grad_ackley, x0)
        self.assertTrue(np.allclose(x, np.zeros(x.shape)))

    def test_sphere(self):
        '''Sphere function with min at origin.'''
        x0 = np.random.random(10)
        x, _iter = gd(of.sphere, fd_complex_step, x0)
        self.assertTrue(np.allclose(x, np.zeros(x.shape)))

    def test_beale(self):
        '''Beale function with min at (3, 1/2).'''
        x0 = np.zeros(2)
        x, _iter = gd(of.beale, fd_complex_step, x0)
        self.assertTrue(np.allclose(x, np.array([3, 0.5])))

    def test_bohachevsky1(self):
        '''Bohachevsky function 1 with min at origin.'''
        x0 = np.ones(2)*300
        x, _iter = gd(of.bohachevsky1, of.grad_bohachevsky1, x0)
        self.assertTrue(np.allclose(x, np.zeros(x.shape)))

    def test_bohachevsky2(self):
        '''Bohachevsky function 2 with min at origin.'''
        x0 = np.ones(2)*200
        x, _iter = gd(of.bohachevsky2, of.grad_bohachevsky2, x0)
        self.assertTrue(np.allclose(x, np.zeros(x.shape)))

    def test_bohachevsky3(self):
        '''Bohachevsky function 3 with min at origin.'''
        x0 = np.ones(2)*200
        x, _iter = gd(of.bohachevsky3, of.grad_bohachevsky3, x0)
        self.assertTrue(np.allclose(x, np.zeros(x.shape)))

if __name__ == '__main__':
    unittest.main()
