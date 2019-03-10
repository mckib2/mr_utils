'''Unit tests for SCGROG interpolation method.
'''

import unittest

import numpy as np

from mr_utils.test_data import load_test_data

class SCGrogTestCase(unittest.TestCase):
    '''Validate against output of MATLAB implementation.'''

    def test_get_gx_gy_results(self):
        '''Validate generation of GRAPPA kernels, Gx, Gy.'''
        from mr_utils.gridding.scgrog import get_gx_gy

        # Load in test data
        # kspace, traj = SCGROG.test_grog_data_4D()
        data = load_test_data('mr_utils/test_data/tests/gridding/scgrog/',
                              ['kspace', 'traj'])
        kspace, traj = data[0], data[1]

        # Run the function
        Gx, Gy = get_gx_gy(kspace, traj)

        # Test it against the known truth
        data = load_test_data('mr_utils/test_data/tests/gridding/scgrog/',
                              ['Gxm', 'Gym'])
        Gxm, Gym = data[0], data[1]
        self.assertTrue(np.allclose(Gx, Gxm))
        self.assertTrue(np.allclose(Gy, Gym))

    def test_scgrog(self):
        '''Make sure we get the same interpolation as MATLAB implementation.'''
        from mr_utils.gridding.scgrog import get_gx_gy
        from mr_utils.gridding import scgrog

        # Load in the test data
        data = load_test_data('mr_utils/test_data/tests/gridding/scgrog/',
                              ['kspace_gridder', 'traj_gridder', 'cartdims'])
        kspace, traj, cartdims = data[0], data[1], data[2]
        # First get Gx,Gy
        Gx, Gy = get_gx_gy(kspace, traj, cartdims=cartdims)

        # Check to make sure Gx,Gy are correct
        data = load_test_data('mr_utils/test_data/tests/gridding/scgrog/',
                              ['Gxm_data', 'Gym_data'])
        Gxm, Gym = data[0], data[1]
        self.assertTrue(np.allclose(Gx, Gxm))
        self.assertTrue(np.allclose(Gy, Gym))

        # Now use Gx,Gy to regrid using grog
        kspace, mask = scgrog(kspace, traj, Gx, Gy, cartdims)

        # Check our work to see if it worked
        data = load_test_data('mr_utils/test_data/tests/gridding/scgrog/',
                              ['kspace_res', 'mask_res'])
        kspacem, maskm = data[0], data[1]
        self.assertTrue(np.allclose(kspace, kspacem))
        self.assertTrue(np.allclose(mask, maskm))

if __name__ == '__main__':
    unittest.main()
