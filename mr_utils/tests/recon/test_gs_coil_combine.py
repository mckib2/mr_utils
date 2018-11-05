import unittest
from mr_utils.sim.ssfp.gs_coil_combine_comparison import comparison_numerical_phantom

class GSCoilCombineTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_comparison_numerical_phantom(self):
        comparison_numerical_phantom()


if __name__ == '__main__':
    unittest.main()
