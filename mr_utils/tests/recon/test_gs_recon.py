import unittest
import numpy as np
import matplotlib.pyplot as plt

class GSReconTestCase(unittest.TestCase):

    def setUp(self):
        self.TR = 6e-3
        self.T1,self.T2 = 1,.8
        self.alpha = np.pi/3

    def test_gs_recon(self):
        from mr_utils.recon.ssfp import gs_recon_for_loop,gs_recon
        from mr_utils.sim.ssfp import ssfp

        # To get periodic banding like we want to see, we need some serious
        # field inhomogeneity.
        dim = 256
        min_df,max_df = 0,500
        x = np.linspace(min_df,max_df,dim)
        y = np.zeros(dim)
        field_map,_ = np.meshgrid(x,y)

        # Get four phase cycled images
        I1 = ssfp(self.T1,self.T2,self.TR,self.alpha,field_map,phase_cyc=0)
        I2 = ssfp(self.T1,self.T2,self.TR,self.alpha,field_map,phase_cyc=np.pi/2)
        I3 = ssfp(self.T1,self.T2,self.TR,self.alpha,field_map,phase_cyc=np.pi)
        I4 = ssfp(self.T1,self.T2,self.TR,self.alpha,field_map,phase_cyc=3*np.pi/2)

        # Make sure it doesn't matter if we go pixel by pixel or do the whole
        # matrix at once
        I0 = gs_recon_for_loop(I1,I2,I3,I4)
        I1 = gs_recon(I1,I2,I3,I4)
        self.assertTrue(np.allclose(I0,I1))

if __name__ == '__main__':
    unittest.main()
