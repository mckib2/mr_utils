'''Test module for simple GRAPPA implementation.'''

import unittest
import warnings # We know skimage will complain about itself importing imp...

import numpy as np
# import matplotlib.pyplot as plt
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

# from mr_utils import view
from mr_utils.utils import sos
from mr_utils.test_data import load_test_data

class GRAPPAUnitTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_recon(self):
        '''Replicate MATLAB results.'''

        # Get the shepp logan phantom
        path = 'mr_utils/test_data/tests/recon/grappa/'
        im = load_test_data(path, ['phantom_shl'])[0]
        dim = im.shape[0]

        # Get simple coil sensitivities
        N = 6
        # csm = simple_csm(N,(dim,dim))
        csm = load_test_data(path, ['ch_sensitivity'])[0]
        # self.assertTrue(np.allclose(csm,csm_mat))

        # Apply csm to image to get coil images
        coils = csm*im
        coils_mat = load_test_data(path, ['phantom_ch'])
        self.assertTrue(np.allclose(coils, coils_mat))

        # Put each channel into kspace
        kspace = np.fft.fftshift(
            np.fft.fft2(np.fft.ifftshift(coils), axes=(1, 2)))
        kspace_mat = GRAPPA.phantom_ch_k()
        self.assertTrue(np.allclose(kspace, kspace_mat))

        # Undersample by Rx
        Rx = 2
        kspace_d = np.zeros(kspace.shape, dtype='complex')
        kspace_d[:, ::Rx, :] = kspace[:, ::Rx, :]
        kspace_d_mat = GRAPPA.phantom_ch_k_u()
        self.assertTrue(np.allclose(kspace_d, kspace_d_mat))

        # Choose center fully samples lines as autocalibration signal (ACS)
        center_row, pad = int(dim/2), 8
        mask = np.zeros(kspace_d.shape, dtype=bool)
        mask[:, center_row-pad:center_row+pad, :] = True
        autocal = kspace[mask].reshape((N, -1, mask.shape[-1]))
        autocal_mat = GRAPPA.phantom_ch_k_acl()
        self.assertTrue(
            np.allclose(np.pad(autocal, ((0, 0), (24, 24), (0, 0)),
                               mode='constant'), autocal_mat))

        # Separate the autocalibration region into patches to get source matrix
        patch_size = (3, 3)
        S0 = np.zeros((N, (autocal.shape[1] - 2)*(autocal.shape[2] - 2),
                       patch_size[0]*patch_size[1]), dtype='complex')
        for ii in range(N):
            S0[ii, :, :] = view_as_windows(
                autocal[ii, :, :], patch_size).reshape(
                    (S0.shape[1], S0.shape[2]))

        S0_mat = GRAPPA.S_ch_temp()
        self.assertTrue(np.allclose(np.conj(S0), S0_mat))

        # Remove the unknown values.  The remaiming values form source matrix,
        # S, for each coil
        S_temp = S0[:, :, [0, 1, 2, 6, 7, 8]]
        S_temp_mat = GRAPPA.S_ch()
        self.assertTrue(np.allclose(np.conj(S_temp), S_temp_mat))

        S = np.hstack(S_temp[:])
        S_mat = GRAPPA.S()
        self.assertTrue(np.allclose(np.conj(S), S_mat))

        # The middle pts form target vector, T, for each coil
        T = S0[:, :, 4].T
        T_mat = GRAPPA.T()
        self.assertTrue(np.allclose(np.conj(T), T_mat))

        # Invert S to find weights, W
        W = np.linalg.pinv(S).dot(T)
        W_mat = GRAPPA.W()
        self.assertTrue(np.allclose(np.conj(W), W_mat))

        # Now onto the forward problem to fill in the missing lines...

        # Make patches out of all acquired data (skip the missing lines)
        S0 = np.zeros(
            (N, int((kspace_d.shape[1] - 2)/Rx)*(kspace_d.shape[2] - 2),
             patch_size[0]*patch_size[1]), dtype='complex')
        for ii in range(N):
            S0[ii, :, :] = view_as_windows(
                kspace_d[ii, :, :], patch_size, step=(Rx, 1)).reshape(
                    (S0.shape[1], S0.shape[2]))

        S0_mat = GRAPPA.S_ch_new_temp()
        self.assertTrue(np.allclose(np.conj(S0), S0_mat))

        # Remove the unknown values.  The remaiming values form source matrix,
        # S, for each coil
        S_new_temp = S0[:, :, [0, 1, 2, 6, 7, 8]]
        S_new_temp_mat = GRAPPA.S_ch_new()
        self.assertTrue(np.allclose(np.conj(S_new_temp), S_new_temp_mat))

        S_new = np.hstack(S_new_temp[:])
        S_new_mat = GRAPPA.S_new()
        self.assertTrue(np.allclose(np.conj(S_new), S_new_mat))

        T_new = S_new.dot(W)
        T_new_mat = GRAPPA.T_new()
        self.assertTrue(np.allclose(np.conj(T_new), T_new_mat))

        # Back fill in the missing lines to recover the image
        lines = np.reshape(T_new.T, (N, -1, dim - 2))
        lines_mat = GRAPPA.T_ch_new_M()
        self.assertTrue(np.allclose(lines, lines_mat))

        kspace_d[:, 1:-1:Rx, 1:-1] = lines

        recon = sos(np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
            kspace_d), axes=(1, 2))), axes=0)
        recon_mat = GRAPPA.Im_Recon()
        self.assertTrue(np.allclose(recon, recon_mat))

        # plt.imshow(recon)
        # plt.show()

    def test_grappa2d(self):
        '''Do simple 2d recon.'''
        from mr_utils.recon.grappa import grappa2d
        from mr_utils.test_data import GRAPPA

        # Get everything set up with downsampling and such
        im = GRAPPA.phantom_shl()
        sens = GRAPPA.csm()
        # view(sens)
        coils = sens*im
        kspace = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(
            coils), axes=(1, 2)))
        Rx = 2
        kspace_d = np.zeros(kspace.shape, dtype='complex')
        kspace_d[:, ::Rx, :] = kspace[:, ::Rx, :]

        # Get the undersampled image space coil images
        coil_ims = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
            kspace_d), axes=(1, 2)))

        # Get the autocalibration signal
        center_row, pad = int(sens.shape[1]/2), 8
        mask = np.zeros(kspace_d.shape, dtype=bool)
        mask[:, center_row-pad:center_row+pad, :] = True
        acs = kspace[mask].reshape((sens.shape[0], -1, mask.shape[-1]))
        # view(acs)

        # Run the recon
        recon = grappa2d(coil_ims, sens, acs, Rx, Ry=1, kernel_size=(3, 3))

        # Check to see if the answers match
        recon = sos(recon, axes=0)
        recon_mat = GRAPPA.Im_Recon()
        self.assertTrue(np.allclose(recon, recon_mat))

if __name__ == '__main__':
    unittest.main()
