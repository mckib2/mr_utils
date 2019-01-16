import unittest
import numpy as np
from mr_utils import view

class TestAMP(unittest.TestCase):

    def setUp(self):
        from mr_utils.test_data import AMPData
        from mr_utils.cs.models import UFT

        self.x0 = AMPData.x0()
        self.y = AMPData.y()
        self.mask = AMPData.mask()
        self.cdf97,self.level = AMPData.cdf97()
        self.uft = UFT(self.mask)

    def test_uft(self):
        '''Test undersampled fourier encoding.'''

        y0 = self.uft.forward_ortho(self.x0)
        self.assertTrue(np.allclose(self.y,y0))

    def test_wavelet_decomposition(self):

        import pywt
        from mr_utils.utils import cdf97_2d_forward,cdf97_2d_inverse
        wavelet_transform,locations = cdf97_2d_forward(self.x0,self.level)

        # # biorthogonal 4/4 is the same as CDF 9/7 according to wikipedia:
        # #   https://en.wikipedia.org/wiki/Cohen%E2%80%93Daubechies%E2%80%93Feauveau_wavelet#Numbering
        # # periodization seems to be the only way to get shapes to line up.
        # cdf97 = pywt.wavedec2(self.x0,wavelet='bior4.4',mode='periodization',level=self.level)
        # wavelet_transform = np.zeros(self.cdf97.shape)
        #
        # # Initialize
        # cVy = 0
        # cHx = 0
        #
        # ## Strategy:
        # #                             -------------------
        # #                             |        |        |
        # #                             | cA(LL) | cH(LH) |
        # #                             |        |        |
        # # (cA, (cH, cV, cD))  <--->   -------------------
        # #                             |        |        |
        # #                             | cV(HL) | cD(HH) |
        # #                             |        |        |
        # #                             -------------------
        #
        # # Start top left
        # cA5 = cdf97[0]
        # xx,yy = cA5.shape[:]
        # wavelet_transform[:xx,:yy] = cA5
        # cHx += xx
        # cVy += yy
        #
        # # Iterate over tuples (cHi,cVi,cDi)
        # for ii in range(1,len(cdf97)):
        #
        #     # Fill in cD
        #     xx,yy = cdf97[ii][2].shape[:]
        #     wavelet_transform[cHx:cHx+xx,cVy:cVy+yy] = cdf97[ii][2]
        #     # wavelet_transform[cVy:cVy+yy,cHx:cHx+xx] = cdf97[ii][2]
        #
        #     # cA is already in place, move on to cH
        #     xx,yy = cdf97[ii][0].shape[:]
        #     wavelet_transform[cHx:cHx+xx,:yy] = cdf97[ii][0]
        #     # wavelet_transform[:yy,cHx:cHx+xx] = cdf97[ii][0]
        #     cHx += xx
        #
        #     # Now get cV
        #     xx,yy = cdf97[ii][1].shape[:]
        #     wavelet_transform[:xx,cVy:cVy+yy] = cdf97[ii][1]
        #     # wavelet_transform[cVy:cVy+yy,:xx] = cdf97[ii][1]
        #     cVy += yy

        view(np.stack((np.log(np.abs(self.cdf97)),np.log(np.abs(wavelet_transform)))))
        view(np.stack((self.cdf97 - wavelet_transform)),log=True)

        # Make sure we can go back
        view(cdf97_2d_inverse(wavelet_transform,locations))

        self.assertTrue(np.allclose(wavelet_transform,self.cdf97))

if __name__ == '__main__':
    unittest.main()
