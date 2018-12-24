import unittest
from mr_utils.optimization import gd,fd_complex_step,linesearch_quad
from mr_utils.test_data import optimization_functions as of
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class TestGD(unittest.TestCase):

    def setUp(self):
        pass

    def test_quadratic(self):
        x0 = 6
        x,iter = gd(of.quadratic,fd_complex_step,x0,alpha=None)
        self.assertTrue(np.allclose(x,9/4))

    def test_maxiter(self):
        x0 = 6
        num_iter = 5
        with self.assertWarnsRegex(Warning,'GD hit maxiters!'):
            x,iter = gd(of.quadratic,fd_complex_step,x0,iter=num_iter)
        self.assertEqual(iter,num_iter)

    # def test_rosenbrock(self):
    #     x0 = np.zeros(2)
    #     x,iter = gd(of.rosenbrock,fd_complex_step,x0)
    #     self.assertTrue(np.allclose(x,np.ones(x.shape)))

    def test_rastrigin(self):
        x0 = np.ones(10)
        x,iter = gd(of.rastrigin,fd_complex_step,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    def test_ackley(self):
        # This has many minima, make sure we only get the closest one
        x0 = np.zeros(10)
        x,iter = gd(of.ackley,of.grad_ackley,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    def test_sphere(self):
        x0 = np.random.random(10)
        x,iter = gd(of.sphere,fd_complex_step,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    def test_beale(self):
        x0 = np.zeros(2)
        x,iter = gd(of.beale,fd_complex_step,x0)
        self.assertTrue(np.allclose(x,np.array([ 3,0.5 ])))

    def test_bohachevsky1(self):
        x0 = np.ones(2)*300
        x,iter = gd(of.bohachevsky1,of.grad_bohachevsky1,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    def test_bohachevsky2(self):
        x0 = np.ones(2)*200
        x,iter = gd(of.bohachevsky2,of.grad_bohachevsky2,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    def test_bohachevsky3(self):
        x0 = np.ones(2)*200
        x,iter = gd(of.bohachevsky3,of.grad_bohachevsky3,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

if __name__ == '__main__':
    unittest.main()
