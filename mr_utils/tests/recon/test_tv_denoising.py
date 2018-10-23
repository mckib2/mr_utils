import unittest
from skimage.data import camera
import numpy as np

class TestTVDenoisingTestCase(unittest.TestCase):

    def setUp(self):
        self.im = camera()
        self.im /= np.max(self.im)
        self.sigma = 10
        self.im_noisy = self.sigma*np.random.normal(0,1,self.im.shape)

    def test_tv_denoising(self):

        lam = 1
        im0 = tv_l1_denoise(self.im_noisy,lam,niter=100)

        plt.subplot(1,3,1)
        plt.imshow(self.im_noisy)
        plt.subplot(1,3,2)
        plt.imshow(im0)
        plt.subplot(1,3,3)
        plt.imshow(np.abs(self.im - self.im0))
        plt.show()



if __name__ == '__main__':
    unittest.main()
