import unittest
from mr_utils.optimization import gd,fd_complex_step,linesearch_quad
from mr_utils.test_data import quadratic,rosenbrock,rastrigin,ackley,sphere,beale
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class TestGD(unittest.TestCase):

    def setUp(self):
        pass

    def test_quadratic(self):
        x0 = 6
        x,iter = gd(quadratic,fd_complex_step,x0,alpha=None)
        self.assertTrue(np.allclose(x,9/4))

    def test_maxiter(self):
        x0 = 6
        num_iter = 5
        with self.assertWarnsRegex(Warning,'GD hit maxiters!'):
            x,iter = gd(quadratic,fd_complex_step,x0,iter=num_iter)
        self.assertEqual(iter,num_iter)

    def test_rosenbrock(self):
        x0 = np.zeros(10)
        x,iter = gd(rosenbrock,fd_complex_step,x0,tol=1e-10)
        self.assertTrue(np.allclose(x,np.ones(x.shape)))

    def test_rastrigin(self):
        x0 = np.ones(10)
        x,iter = gd(rastrigin,fd_complex_step,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    # def test_ackley(self):
    #     x0 = np.ones(2)*0
    #     x,iter = gd(ackley,fd_complex_step,x0,tol=1e-10)
    #     print(x)

    def test_sphere(self):
        x0 = np.random.random(10)
        x,iter = gd(sphere,fd_complex_step,x0)
        self.assertTrue(np.allclose(x,np.zeros(x.shape)))

    def test_beale(self):
        x0 = np.zeros(2)
        x,iter = gd(beale,fd_complex_step,x0)
        self.assertTrue(np.allclose(x,np.array([ 3,0.5 ])))

        # lims = np.array([ -30,30 ],dtype=np.float32)
        #
        # x = np.linspace(lims[0],lims[1])
        # y = np.linspace(lims[0],lims[1])
        # X,Y = np.meshgrid(x,y)
        #
        # Z = np.zeros(X.shape)
        # for ii in range(x.size):
        #     for jj in range(y.size):
        #         Z[ii,jj] = rosenbrock([ x[ii],y[jj] ])
        #
        # fig = plt.figure()
        # ax = fig.add_subplot(111,projection='3d')
        # ax.plot_surface(X,Y,Z,cmap='magma')
        # plt.show()



if __name__ == '__main__':
    unittest.main()
