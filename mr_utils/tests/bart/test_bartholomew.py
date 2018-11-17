import unittest
from mr_utils.bart import Bartholomew as B
from mr_utils.bart import BartholomewObject
from mr_utils import view
import numpy as np

class BartholomewTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_bartholomew_object(self):
        self.assertEqual(type(B),BartholomewObject)

    def test_incorrect_function_name(self):
        with self.assertRaises(AttributeError):
            B.hello()

    def test_incorrect_position_args(self):
        with self.assertRaises(Exception):
            B.traj(256,256)

    def test_traj(self):
        x,y = 256,64
        val = B.traj(x=x,y=y,a=1,G=True,q=[0,0,0])
        self.assertEqual((3,x,y),val.shape)

    def test_non_cart_example(self):
        '''"non-Cartesian MRI using BART"

        Adapted from:
            https://mrirecon.github.io/bart/examples.html
        '''

        # Generate k-space trajectory with num_spokes radial spokes
        num_spokes = 32
        traj_rad = B.traj(x=512,y=num_spokes,r=True)

        # 2x oversampling
        traj_rad2 = B.scale(0.5,traj_rad)

        # simulate num_chan-channel k-space data
        num_chan = 8
        ksp_sim = B.phantom(k=True,s=num_chan,t=traj_rad2)

        # increase the reconstructed FOV a bit
        traj_rad2 = B.scale(0.6,traj_rad)

        # inverse gridding
        igrid = B.nufft(ksp_sim,i=True,t=traj_rad2)

        # channel combination
        reco1 = B.rss(num_chan,igrid)

        # reconstruct low-resolution image and transform back to k-space
        lowres_img = B.nufft(ksp_sim,i=True,d=[24,24,1],t=traj_rad2)
        lowres_ksp = B.fft(lowres_img,u=7)

        # zeropad to full size
        ksp_zerop = B.resize(lowres_ksp,c=(0,308,1,308))

        # ESPIRiT calibration
        sens = B.ecalib(ksp_zerop,m=1)

        # non-Cartesian parallel imging
        reco2 = B.pics(ksp_sim,sens,S=True,r=0.001,t=traj_rad2)
        reco3 = B.pics(ksp_sim,sens,l1=True,S=True,r=0.005,m=True,t=traj_rad2)
        # view(np.squeeze(np.concatenate((reco1,reco2,reco3))))

    def test_calibration_matrix(self):
        num_spokes = 32
        traj_rad = B.traj(x=512,y=num_spokes,r=True)
        traj_rad2 = B.scale(0.5,traj_rad)
        num_chan = 8
        ksp_sim = B.phantom(k=True,s=num_chan,t=traj_rad2)
        traj_rad2 = B.scale(0.6,traj_rad)

        calmat = B.calmat(ksp_sim,r=20,k=6)
        U,SV,VH = B.svd(calmat)
        # view(SV)

        calib,emaps = B.ecalib(ksp_sim,r=20)
        sens = B.slice((4,0),calib)


if __name__ == '__main__':
    unittest.main()
