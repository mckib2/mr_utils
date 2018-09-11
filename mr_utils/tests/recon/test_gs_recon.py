import unittest
import numpy as np
import matplotlib.pyplot as plt
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=ImportWarning)
    from scipy.io import loadmat

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
        self.assertTrue(np.allclose(I0,I1))


class GSReconKneeData(unittest.TestCase):

    def setUp(self):
        from mr_utils.test_data import I1,I2,I3,I4
        self.I1 = loadmat(I1)['I1']
        self.I2 = loadmat(I2)['I2']
        self.I3 = loadmat(I3)['I3']
        self.I4 = loadmat(I4)['I4']

    def test_max_magnitudes(self):
        from mr_utils.test_data import I_max_mag
        from mr_utils.recon.ssfp import get_max_magnitudes

        I_max_mag = loadmat(I_max_mag)['maximum']

        # Make sure we both find the same maximum magnitude values
        I_max_mag_py = get_max_magnitudes(self.I1,self.I2,self.I3,self.I4)
        self.assertTrue(np.allclose(I_max_mag,I_max_mag_py))

    def test_complex_sum(self):
        from mr_utils.test_data import CS
        from mr_utils.recon.ssfp import complex_sum

        CS = loadmat(CS)['CS']

        CS_py = complex_sum(self.I1,self.I2,self.I3,self.I4)
        self.assertTrue(np.allclose(CS_py,CS))

    def test_direct_solution(self):
        from mr_utils.test_data import Id
        from mr_utils.sim.ssfp import get_complex_cross_point

        Id = loadmat(Id)['M']

        Id_py = get_complex_cross_point(self.I1,self.I2,self.I3,self.I4)
        self.assertTrue(np.allclose(Id_py,Id))

    def test_weighted_combination(self):
        from mr_utils.test_data import w13,w24
        from mr_utils.recon.ssfp import compute_Iw,complex_sum,get_max_magnitudes,get_complex_cross_point

        w13 = loadmat(w13)['w1']
        w24 = loadmat(w24)['w2']
        Iw13 = self.I1*w13 + self.I3*(1 - w13)
        Iw24 = self.I2*w24 + self.I4*(1 - w24)

        # A little processing to get where we need to to compare weighted combs
        Id = get_complex_cross_point(self.I1,self.I2,self.I3,self.I4)
        CS = complex_sum(self.I1,self.I2,self.I3,self.I4)
        I_max_mag = get_max_magnitudes(self.I1,self.I2,self.I3,self.I4)
        mask = np.abs(Id) > I_max_mag
        Id[mask] = CS[mask]
        Iw13_py = compute_Iw(self.I1,self.I3,Id,patch_size=(5,5))

        self.assertTrue(np.allclose(Iw13,Iw13_py))

    def test_gs_recon_knee(self):
        from mr_utils.test_data import I
        from mr_utils.recon.ssfp import gs_recon

        I0 = loadmat(I)['I']
        I1 = gs_recon(self.I1,self.I2,self.I3,self.I4)
        self.assertTrue(np.allclose(I0,I1))

if __name__ == '__main__':
    unittest.main()
