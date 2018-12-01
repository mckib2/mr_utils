import unittest
import numpy as np
import matplotlib.pyplot as plt

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
        patches = get_patches(imspace,(4,4))

        # Reorder patches
        

if __name__ == '__main__':
    unittest.main()
