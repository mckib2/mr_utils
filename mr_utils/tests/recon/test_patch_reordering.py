import unittest
import numpy as np
from mr_utils import view

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

        # Flatten the array and sort
        im = im.flatten()
        idx = np.argsort(im) # sorts by real
        # idx = np.argsort(-np.abs(im)) # sorts by magnitude
        # view(im[idx])
        view(np.diff(im[idx]))



if __name__ == '__main__':
    unittest.main()
