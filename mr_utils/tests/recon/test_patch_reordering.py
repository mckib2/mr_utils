import unittest
import numpy as np
from mr_utils import view
from mr_utils.recon.reordering import sort2d
from mr_utils.matlab import Client
from skimage.measure import compare_mse,compare_ssim,compare_psnr

class PatchReorderTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_reorder(self):
        from mr_utils.test_data.phantom import modified_shepp_logan
        from mr_utils.recon.reordering import get_patches

        # Get phantom
        dim = 64
        phantom = np.rot90(modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)])
        kspace = np.fft.fftshift(np.fft.fft2(phantom))
        imspace = np.fft.ifft2(kspace)

        # Get patches
        patches = get_patches(imspace,(3,3))

        # Take mean of each patch to be the pixel value
        im = np.mean(patches,axis=(-2,-1))
        # view(im)

        # # Try 2d reordering and using Ganesh's MATLAB script to do recon
        # # view(im)
        # im_sorted,idx = sort2d(im) # default sort by real
        # self.assertTrue(np.allclose(im.take(idx),im_sorted))
        # # Run Ganesh's recon
        # client = Client()
        # client.run('cd mr_utils/recon/reordering/spatial_tv')
        # client.run('run SCR_reordering.m')
        # data = client.get([ 'Coil1','img_est','measuredImgDomain','prior_data' ])
        # client.exit()

        # # Run Ganesh's temporal recon
        # client = Client()
        # client.run('cd mr_utils/recon/reordering/temporal_tv')
        # client.run('run TCR_reordering_main.m')
        # data = client.get([ 'Coil','mask_k_space_sparse','recon_data' ])
        # client.exit()
        # np.save('mr_utils/recon/reordering/temporal_tv/data.npy',data)
        data = np.load('mr_utils/recon/reordering/temporal_tv/data.npy').item()

        # Get reference, recon, and prior image estimates
        coil_imspace = np.fft.fftshift(np.fft.fft2(data['Coil'],axes=(0,1)),axes=(0,1))
        recon_flipped = np.rot90(np.rot90(data['recon_data'])).astype(coil_imspace.dtype)
        prior = np.fft.fftshift(np.fft.fft2(data['Coil']*data['mask_k_space_sparse'],axes=(0,1)),axes=(0,1))

        # Normalize so they are comparable
        abs_coil_imspace = np.abs(coil_imspace)
        abs_coil_imspace /= np.max(abs_coil_imspace)
        abs_recon_flipped = np.abs(recon_flipped)
        abs_recon_flipped /= np.max(abs_recon_flipped)
        abs_prior = np.abs(prior)
        abs_prior /= np.max(abs_prior)

        r_coil_imspace = coil_imspace.real/np.max(np.abs(coil_imspace.real))
        i_coil_imspace = coil_imspace.imag/np.max(np.abs(coil_imspace.imag))
        r_recon_flipped = recon_flipped.real/np.max(np.abs(recon_flipped.real))
        i_recon_flipped = recon_flipped.imag/np.max(np.abs(recon_flipped.imag))
        r_prior = prior.real/np.max(np.abs(prior.real))
        i_prior = prior.imag/np.max(np.abs(prior.imag))

        # Comparisons
        print('MSE  of px reorder: %g' % (.5*(compare_mse(r_coil_imspace,r_recon_flipped) + compare_mse(i_coil_imspace,i_recon_flipped))))
        print('SSIM of px reorder: %g' % compare_ssim(abs_coil_imspace,abs_recon_flipped))
        print('PSNR of px reorder: %g' % compare_psnr(abs_coil_imspace,abs_recon_flipped))

        print('MSE  of patch reorder: %g' % (.5*(compare_mse(r_coil_imspace,) + compare_mse(i_coil_imspace,))))
        print('SSIM of patch reorder: %g' % compare_ssim(abs_coil_imspace,))
        print('PSNR of patch reorder: %g' % compare_psnr(abs_coil_imspace,))


        # # These are different because of scaling:
        # # print('MSE  of prior: %g' % compare_mse(abs_coil_imspace,abs_prior))
        # print('MSE  of prior: %g' % ((compare_mse(r_coil_imspace,r_prior) + compare_mse(i_coil_imspace,i_prior))/2))
        # print('SSIM of prior: %g' % compare_ssim(abs_coil_imspace,abs_prior))
        # print('PSNR of prior: %g' % compare_psnr(abs_coil_imspace,abs_prior))

        view(prior)
        view(recon_flipped)

        # # Flatten the array and sort
        # im = im.flatten()
        # idx = np.argsort(im) # sorts by real
        # # idx = np.argsort(-np.abs(im)) # sorts by magnitude
        # view(im[idx])
        # view(np.diff(im[idx]))



if __name__ == '__main__':
    unittest.main()
