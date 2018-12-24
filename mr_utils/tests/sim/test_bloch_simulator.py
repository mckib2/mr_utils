import unittest
import numpy as np
from mr_utils.sim import bloch

class TestBloch(unittest.TestCase):

    def setUp(self):
        dims = (2,1,1)
        self.M0 = np.ones(dims)*1.0
        self.T1 = np.zeros(dims)
        self.T2 = np.zeros(dims)

        # Choose some T1,T2 values
        self.T1[0,...] = 1.5
        self.T1[1,...] = 2.0
        self.T2[0,...] = 0.8
        self.T2[1,...] = 1.0

        # Time mesh for simulation
        self.Nt = 100000
        self.t,self.h = np.linspace(0,10,self.Nt,retstep=True)

        # RF flip, (alpha,beta,gamma)
        self.RF = (0,np.pi/2,0)

    def test_matrix_against_loop(self):
        # Run once using for loops, once with matrix algebra to make sure we
        # did the einsteinian sum correctly
        spins0 = bloch.sim(self.T1,self.T2,self.M0,self.Nt,self.h,*self.RF)
        spins1 = bloch.sim_loop(self.T1,self.T2,self.M0,self.Nt,self.h,*self.RF)
        self.assertTrue(np.allclose(spins0,spins1))

    def test_spoiled_gre(self):
        pass

if __name__ == '__main__':
    unittest.main()
