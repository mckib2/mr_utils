import unittest
import numpy as np

class RudinEtAlTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_algo_for_loop(self):
        from mr_utils.recon.reordering import update_all_for_loop

        u0 = np.array([ [ 1,2,3 ],[ 4,5,6 ],[ 7,8,9 ] ])
        dt = 1
        h = 1
        sigma = .01
        niters = 100

        u = update_all_for_loop(u0,dt,h,sigma,niters)

if __name__ == '__main__':
    unittest.main()
