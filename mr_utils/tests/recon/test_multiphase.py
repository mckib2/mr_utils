import unittest
from mr_utils.sim.ssfp import ssfp
from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils import view
import numpy as np

class MultiphaseTestCase(unittest.TestCase):

    def setUp(self):
        # Load phantom
        dim = 64
        phantom = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])

        # SSFP params
        self.T1 = 2
        self.T2 = 1
        self.TR = 6e-3
        self.alpha = np.pi/3
        self.phase_cycs = np.array([ 0,np.pi ])

        # # To get periodic banding like we want to see, we need some serious
        # # field inhomogeneity.
        # min_df,max_df = 0,500
        # x = np.linspace(min_df,max_df,dim)
        # y = np.zeros(dim)
        # self.field_map,_ = np.meshgrid(x,y)
        self.field_map = phantom

        # Generate simulated banding image explicitly using NMR parameters
        imspace_pc_0 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=self.phase_cycs[0])
        kspace_pc_0 = np.fft.fftshift(np.fft.fft2(imspace_pc_0))
        imspace_pc_1 = ssfp(self.T1,self.T2,self.TR,self.alpha,self.field_map,phase_cyc=self.phase_cycs[1])
        kspace_pc_1 = np.fft.fftshift(np.fft.fft2(imspace_pc_1))

        self.imspace = np.stack((imspace_pc_0,imspace_pc_1))
        self.kspace = np.stack((kspace_pc_0,kspace_pc_1))

    def test_multiphase(self):

        # Check out the images
        # view(self.imspace)

        # Even lines get pc0, odd lines get pc1
        kspace_pc0 = self.kspace[0,...]
        # kspace_pc0[1::2,:] = 0
        kspace_pc1 = self.kspace[1,...]
        # kspace_pc1[0::2,:] = 0

        # idc = np.unravel_index(np.argmax(kspace_pc0),kspace_pc0.shape)
        # print(idc)
        # kspace_pc1[idc[0],:] = kspace_pc0[idc[0],:]

        view(kspace_pc1,fft=True,fftshift=False)
        # view(kspace_pc1)

if __name__ == '__main__':
    unittest.main()
