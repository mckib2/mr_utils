'''Make sure 2D SSFP contrast simulation works.'''

import unittest
import numpy as np
# from mr_utils import view

class BSSFP2DSimTestCase(unittest.TestCase):
    '''Test Cases for bSSFP contrast simulation.'''

    def setUp(self):

        dim = 64
        self.dim = dim

        # Bottle
        x = np.linspace(-1, 1, dim)
        y = np.linspace(-1, 1, dim)
        X, Y = np.meshgrid(x, y)
        bottle_idx = np.sqrt(X**2 + Y**2) < .5

        self.PD = np.random.normal(0, 0.1, (dim, dim)) # controls noise level
        self.T1s = np.zeros((dim, dim))
        self.T2s = np.zeros((dim, dim))

        self.PD[bottle_idx] = 5
        self.T1s[bottle_idx] = 1.5
        self.T2s[bottle_idx] = 0.8

        min_df, max_df = 0, 500
        fx = np.linspace(min_df, max_df, dim)
        fy = np.zeros(dim)
        self.field_map, _ = np.meshgrid(fx, fy)

        self.TR = 6e-3
        self.alpha = np.pi/3

        self.args = {
            'T1': self.T1s,
            'T2': self.T2s,
            'TR': self.TR,
            'alpha': self.alpha,
            'field_map': self.field_map,
            'M0': self.PD
        }

    def test_t1_t2_field_map_mats(self):
        '''Generate simulation given t1,t2, and field maps.'''
        from mr_utils.sim.ssfp import ssfp

        # Let T1,T2, and field_map all be matrices over the entire 2d image
        sig = ssfp(self.T1s, self.T2s, self.TR, self.alpha, self.field_map,
                   phase_cyc=0, M0=self.PD)
        # view(sig)

    def test_gs(self):
        '''Test GS recon using simulated data.'''
        from mr_utils.sim.ssfp import ssfp
        from mr_utils.recon.ssfp import gs_recon

        pcs = np.zeros((4, self.dim, self.dim), dtype='complex')
        for ii, pc in enumerate([0, np.pi/2, np.pi, 3*np.pi/2]):
            pcs[ii, ...] = ssfp(**self.args, phase_cyc=pc)
        # view(pcs)

        recon = gs_recon(*[x.squeeze() for x in np.split(pcs, 4)])
        # view(recon)

if __name__ == '__main__':
    unittest.main()
