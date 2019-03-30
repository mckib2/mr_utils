'''Sanity tests to make sure phase is correct in sssp sims.'''

import unittest

import numpy as np

from mr_utils.sim.ssfp import ssfp, freeman_ssfp

class SSFPSanityTestCase(unittest.TestCase):
    '''Checks against multiple implementations.'''

    def setUp(self):
        self.T1 = 1.2
        self.T2 = .035
        self.M0 = 1
        self.TR = 10e-3
        self.alpha = np.arccos(
            (self.T1 - self.T2)/(self.T1 + self.T2))
        self.df = 10
        # self.phi_rf = np.deg2rad(-70)

        self.args = {
            'T1': self.T1,
            'T2': self.T2,
            'TR': self.TR,
            'alpha': self.alpha,
            'field_map': self.df,
            'M0': self.M0,
            # 'phi_rf': self.phi_rf
        }

    def test_against_freeman(self):
        '''Make sure contrast matches Freeman-Hill solution.'''
        I = ssfp(**self.args)
        I0 = freeman_ssfp(**self.args, before=False)
        self.assertAlmostEqual(I, I0)

if __name__ == '__main__':
    unittest.main()
