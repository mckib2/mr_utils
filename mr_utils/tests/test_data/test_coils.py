import unittest
import numpy as np
import matplotlib.pyplot as plt

class CoilsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_csm_generation(self):
        from mr_utils.test_data.coils import simple_csm

        num_maps = 6
        cs_maps = simple_csm(num_maps)
        N,x,y = cs_maps.shape[:]
        for ii in range(N):
            # Derivative of linear function should be constant
            grad = np.gradient(cs_maps[ii,0,:])
            # We expect each coil sensitivity to be a linear gradient
            self.assertTrue(np.allclose(grad,grad[0]))

if __name__ == '__main__':
    unittest.main()
