import unittest
# from mr_utils.sim.ssfp import ssfp
# from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils.test_data import SSFPMultiphase
from mr_utils import view
import numpy as np

class MultiphaseTestCase(unittest.TestCase):

    def setUp(self):
        # # Load phantom
        # # dim = 64
        # # phantom = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])
        #
        # # SSFP params
        # self.T1 = 2
        # self.T2 = 1
        # self.TR = 6e-3
        # self.alpha = np.pi/3
        # self.phase_cycs = np.array([ 0,np.pi ])
        #
        # # To get periodic banding like we want to see, we need some serious
        # # field inhomogeneity.
        # min_df,max_df = 0,500
        # x = np.linspace(min_df,max_df,dim)
        # y = np.zeros(dim)
        # self.field_map,_ = np.meshgrid(x,y)
        # # self.field_map = phantom
        #
        # # Generate simulated banding image explicitly using NMR parameters
        # imspace_pc_0 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=self.phase_cycs[0])
        # kspace_pc_0 = np.fft.fftshift(np.fft.fft2(imspace_pc_0))
        # imspace_pc_1 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=self.phase_cycs[1])
        # kspace_pc_1 = np.fft.fftshift(np.fft.fft2(imspace_pc_1))
        #
        # self.imspace = np.stack((imspace_pc_0,imspace_pc_1)).transpose((1,2,0))
        # self.kspace = np.stack((kspace_pc_0,kspace_pc_1)).transpose((1,2,0))

        # Load in ankle data to get kspace: (phase_cycle,x,y,coils)
        pc0,pc90 = SSFPMultiphase.ssfp_ankle_te_6_pc_0_and_90()
        self.kspace = np.stack((pc0,pc90))

    def test_multiphase(self):

        view(self.kspace,fft=True,movie_axis=0,montage_axis=3)
        # view(self.kspace,fft=True)


if __name__ == '__main__':
    unittest.main()
