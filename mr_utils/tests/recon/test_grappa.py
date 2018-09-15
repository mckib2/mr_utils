import unittest
import numpy as np
import matplotlib.pyplot as plt
import warnings # We know skimage will complain about itself importing imp...
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

class GRAPPAUnitTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_recon(self):
        from mr_utils.recon import grappa
        from mr_utils.test_data.phantom import modified_shepp_logan
        from mr_utils.test_data.coils import simple_csm

        # Get the shepp logan phantom
        dim = 64
        im = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])

        # Get simple coil sensitivities
        N = 6
        csm = simple_csm(N,(dim,dim))

        # Apply csm to image to get coil images
        coils = csm*im

        # Put each channel into kspace
        kspace = np.fft.fftshift(np.fft.fft2(coils,axes=(1,2)))

        # Undersample by Rx
        Rx = 2
        kspace_d = np.zeros(kspace.shape,dtype='complex')
        kspace_d[:,::Rx,:] = kspace[:,::Rx,:]

        # Choose center lines to autocalibrate
        center_row,pad = int(dim/2),8
        mask = np.zeros(kspace_d.shape,dtype=bool)
        mask[:,center_row-pad:center_row+pad,:] = True
        autocal = kspace_d[mask].reshape((N,-1,mask.shape[-1]))

        # Separate the autocalibration region into patches to get source matrix
        patch_size = (3,3)
        S0 = np.zeros((N,autocal.shape[1]-2,autocal.shape[2]-2,patch_size[0]*patch_size[1]),dtype='complex')
        for ii in range(N):
            S0[ii,:,:,:] = view_as_windows(autocal[ii,:,:],patch_size).reshape((S0.shape[1],S0.shape[2],S0.shape[-1]))

        # Remove the unknown values.  The remaiming values form source matrix,
        # S, for each coil
        S = S0[:,:,:,[0,1,2,6,7,8]]

        # The middle pts form target vector, T, for each coil
        T = S0[:,:,:,4]

        print(S.shape)
        print(T.shape)

        # Invert S to find weights, W
        Si = np.linalg.pinv(S)
        W = Si.dot(T)

        print(W.shape)



if __name__ == '__main__':
    unittest.main()
