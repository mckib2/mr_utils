import unittest
from mr_utils.test_data import SSFPMultiphase
from mr_utils import view
import numpy as np
from mr_utils.recon.grappa import grappa2d
from mr_utils.recon.util import sos

class MultiphaseTestCase(unittest.TestCase):

    def setUp(self):

        # Load in ankle data to get kspace: (phase_cycle,x,y,coils)
        pc0 = SSFPMultiphase.ssfp_ankle_te_6_pc_0()
        pc180 = SSFPMultiphase.ssfp_ankle_te_6_pc_180()
        self.kspace = np.stack((pc0,pc180))

    def test_multiphase(self):
        # Check out what we got:
        # view(self.kspace,fft=True,movie_axis=0,montage_axis=3)

        # Under sample even, odd lines
        kspace = self.kspace.copy()
        Rx = 2
        kspace[0,0::Rx,:,:] = 0
        kspace[1,1::Rx,:,:] = 0
        # view(kspace[0,...],fft=False)

        # Make an autocalibration region by combining center lines from each
        # Right now still struggling to get GRAPPA to work...
        num_acl_lines = 24
        acl_idx = range(int(kspace.shape[2]/2-num_acl_lines/2),int(kspace.shape[2]/2+num_acl_lines/2))
        acl = self.kspace[0,:,acl_idx,:].transpose((2,0,1))
        view(acl,log=True)

        # We also need to get some coil sensitivity maps, let's try a crude one
        # first from original data.  Later we'll do espirit...
        imspace = np.fft.fftshift(np.fft.fft2(self.kspace,axes=(1,2)),axes=(1,2))
        comb_sos = sos(imspace[0,...],axes=-1)[...,None]
        sens = (np.abs(imspace[0,...])/np.tile(comb_sos,(1,1,4))).transpose((2,0,1))
        view(sens)

        # Get coils in the image domain with dims in order grappa2d expects
        coil_ims_pc_0 = np.fft.fftshift(np.fft.ifft2(kspace[0,...],axes=(0,1)),axes=(0,1)).transpose((2,0,1))
        view(coil_ims_pc_0)

        recon = grappa2d(coil_ims_pc_0,sens,acs=acl,Rx=2,Ry=1)
        recon = sos(recon,axes=0)
        view(recon)

if __name__ == '__main__':
    unittest.main()
