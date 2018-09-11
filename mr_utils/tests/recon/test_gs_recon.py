import unittest
import numpy as np
import matplotlib.pyplot as plt

class GSReconTestCase(unittest.TestCase):

    def setUp(self):
        from mr_utils.sim.ssfp import ssfp

        self.TR = 6e-3
        self.T1,self.T2 = 1,.8
        self.alpha = np.pi/3

        # To get periodic banding like we want to see, we need some serious
        # field inhomogeneity.
        dim = 256
        min_df,max_df = 0,500
        x = np.linspace(min_df,max_df,dim)
        y = np.zeros(dim)
        self.field_map,_ = np.meshgrid(x,y)

        # Get four phase cycled images
        self.I1 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=0)
        self.I2 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=np.pi/2)
        self.I3 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=np.pi)
        self.I4 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=3*np.pi/2)

    def test_gs_recon(self):
        from mr_utils.recon.ssfp import gs_recon_for_loop,gs_recon

        # Make sure it doesn't matter if we go pixel by pixel or do the whole
        # matrix at once
        I0 = gs_recon_for_loop(self.I1,self.I2,self.I3,self.I4)
        I1 = gs_recon(self.I1,self.I2,self.I3,self.I4)
        plt.plot(np.abs(I1[100,:]))
        plt.show()
        self.assertTrue(np.allclose(I0,I1))

    def test_max_magnitudes(self):
        from mr_utils.recon.ssfp import get_max_magnitudes_for_loop,get_max_magnitudes

        # Make sure it doesn't matter if we go pixel by pixel or do the whole
        # matrix at once
        I0 = get_max_magnitudes_for_loop(self.I1,self.I2,self.I3,self.I4)
        I1 = get_max_magnitudes(self.I1,self.I2,self.I3,self.I4)
        self.assertTrue(np.allclose(I0,I1))

    def test_noisy_gs_recon(self):
        from mr_utils.recon.ssfp import gs_recon,gs_recon_for_loop

        # Add in gaussian noise on both real,imag channels
        m,std = 0,.08
        n1 = np.random.normal(m,std,size=self.I1.shape) + 1j*np.random.normal(m,std,size=self.I1.shape)
        n2 = np.random.normal(m,std,size=self.I1.shape) + 1j*np.random.normal(m,std,size=self.I1.shape)
        n3 = np.random.normal(m,std,size=self.I1.shape) + 1j*np.random.normal(m,std,size=self.I1.shape)
        n4 = np.random.normal(m,std,size=self.I1.shape) + 1j*np.random.normal(m,std,size=self.I1.shape)

        I0 = gs_recon(self.I1 + n1,self.I2 + n2,self.I3 + n3,self.I4 + n4)
        I1 = gs_recon_for_loop(self.I1 + n1,self.I2 + n2,self.I3 + n3,self.I4 + n4)

        # plt.imshow(np.abs(I0))
        # plt.show()

        self.assertTrue(np.allclose(I0,I1))

if __name__ == '__main__':
    unittest.main()
