import unittest
from mr_utils.bart import Bartholomew as B
from mr_utils.bart import BartholomewObject
from mr_utils import view

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

    def test_nufft(self):
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

        view(igrid)


if __name__ == '__main__':
    unittest.main()
