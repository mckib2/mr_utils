import unittest
import numpy as np
from mr_utils.sim import bloch
from mr_utils import view
from mr_utils.sim.gre import gre_sim

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

    # def test_matrix_against_loop(self):
    #     # Run once using for loops, once with matrix algebra to make sure we
    #     # did the einsteinian sum correctly
    #     spins0 = bloch.sim(self.T1,self.T2,self.M0,self.Nt,self.h,*self.RF)
    #     spins1 = bloch.sim_loop(self.T1,self.T2,self.M0,self.Nt,self.h,*self.RF)
    #     self.assertTrue(np.allclose(spins0,spins1))

    def test_against_gre(self):

        TR = 15e-3
        TE = 6e-3
        h = 1e-4
        num_TRs = 200
        Nt = num_TRs*TR/h
        spins0 = bloch.gre(self.T1,self.T2,self.M0,Nt,h,*self.RF,TR,TE)
        spins0 = spins0[0,...] + 1j*spins0[1,...]

        spins1 = gre_sim(self.T1,self.T2,TR,TE,alpha=self.RF[1],field_map=None,phi=0,dphi=0,M0=self.M0,tol=1e-5,iter=None,spoil=True)

        print(spins0.shape,spins1.shape)

        view(np.stack((spins0,spins1)))

if __name__ == '__main__':
    unittest.main()
