import unittest
import numpy as np
from scipy.io import loadmat

class SCGrogTestCase(unittest.TestCase):

    def test_get_gx_gy_results(self):
        from mr_utils.test_data import test_grog_data_4D,gx_gy_results
        from mr_utils.gridding.scgrog import get_gx_gy

        # Load in test data
        data = loadmat(test_grog_data_4D)
        traj = data['testTrajectory3D']
        kspace = data['testData4D']

        # Run the function
        Gx,Gy = get_gx_gy(kspace,traj)

        # Test it against the known truth
        data = loadmat(gx_gy_results)
        Gxm = data['officialGx']
        Gym = data['officialGy']

        self.assertTrue(np.allclose(Gx,Gxm))
        self.assertTrue(np.allclose(Gy,Gym))

    def test_scgrog(self):
        from mr_utils.test_data import test_gridder_data_4D,test_gx_gy_data,grog_result
        from mr_utils.gridding.scgrog import get_gx_gy
        from mr_utils.gridding import scgrog

        # Load in the test data
        data = loadmat(test_gridder_data_4D)['KSpaceData']
        kspace = data['kSpace'][0][0]
        traj = data['trajectory'][0][0]
        cartdims = tuple(list(data['cartesianSize'][0][0][0]))

        # First get Gx,Gy
        Gx,Gy = get_gx_gy(kspace,traj,cartdims=cartdims)

        # Check to make sure Gx,Gy are correct
        data = loadmat(test_gx_gy_data)
        Gxm = data['Gx']
        Gym = data['Gy']

        self.assertTrue(np.allclose(Gx,Gxm))
        self.assertTrue(np.allclose(Gy,Gym))

        # Now use Gx,Gy to regrid using grog
        kspace,mask = scgrog(kspace,traj,Gx,Gy,cartdims)

        # Check our work to see if it worked
        data = loadmat(grog_result)
        kspacem = data['officialCartesianKSpace']
        maskm = data['officialKMask']
        self.assertTrue(np.allclose(kspace,kspacem))
        self.assertTrue(np.allclose(mask,maskm))

if __name__ == '__main__':
    unittest.main()
