import unittest
import numpy as np
import matplotlib.pyplot as plt

class PartialFourerPOCSTestCase(unittest.TestCase):

    def test_partial_fourier_pocs(self):
        from mr_utils.recon.partial_fourier import partial_fourier_pocs
        from mr_utils.test_data.phantom import modified_shepp_logan

        # Get something to test on
        dim = 64
        im = modified_shepp_logan((dim,dim,dim))[:,:,int(dim/2)]
        kspace_all = np.fft.fftshift(np.fft.fft2(im))
        kspace = np.zeros(kspace_all.shape,dtype='complex')

        # Now simulate the partial fourier
        pf_factor = 7/8
        startRO,endRO = int((1-pf_factor)*dim),dim-1
        startE1,endE1 = 0,dim-1
        kspace[startRO:endRO:,startE1:endE1:] = kspace_all[startRO:endRO:,startE1:endE1:]

        # Run the POCS recon
        res_kspace = partial_fourier_pocs(kspace,startRO,endRO,startE1,endE1,iter=1000,thres=1e-8)

        plt.subplot(1,3,1)
        plt.imshow(np.abs(np.fft.fft2(kspace_all)),cmap='gray')
        plt.title('Fully sampled')
        plt.subplot(1,3,2)
        plt.imshow(np.abs(np.fft.fft2(kspace)),cmap='gray')
        plt.title('Zero-pad recon')
        plt.subplot(1,3,3)
        plt.imshow(np.abs(np.fft.ifft2(res_kspace)),cmap='gray')
        plt.title('Partial Fourier POCS recon')
        plt.show()

if __name__ == '__main__':
    unittest.main()
