import unittest
import numpy as np

class SCGrogTestCase(unittest.TestCase):

    def test_get_gx_gy_results(self):
        from mr_utils.test_data import SCGROG
        from mr_utils.gridding.scgrog import get_gx_gy

        # Load in test data
        kspace,traj = SCGROG.test_grog_data_4D()

        # Run the function
        Gx,Gy = get_gx_gy(kspace,traj)

        # Test it against the known truth
        Gxm,Gym = SCGROG.gx_gy_results()

        self.assertTrue(np.allclose(Gx,Gxm))
        self.assertTrue(np.allclose(Gy,Gym))

    def test_scgrog(self):
        from mr_utils.test_data import SCGROG
        from mr_utils.gridding.scgrog import get_gx_gy
        from mr_utils.gridding import scgrog

        # Load in the test data
        kspace,traj,cartdims = SCGROG.test_gridder_data_4D()

        # First get Gx,Gy
        Gx,Gy = get_gx_gy(kspace,traj,cartdims=cartdims)

        # Check to make sure Gx,Gy are correct
        Gxm,Gym = SCGROG.test_gx_gy_data()

        self.assertTrue(np.allclose(Gx,Gxm))
        self.assertTrue(np.allclose(Gy,Gym))

        # Now use Gx,Gy to regrid using grog
        kspace,mask = scgrog(kspace,traj,Gx,Gy,cartdims)

        # Check our work to see if it worked
        kspacem,maskm = SCGROG.grog_result()
        self.assertTrue(np.allclose(kspace,kspacem))
        self.assertTrue(np.allclose(mask,maskm))

if __name__ == '__main__':
    unittest.main()
