import unittest
import numpy as np
from mr_utils.sim.ssfp import ssfp,quantitative_fm
from tqdm import trange

class TestQuantitativeFieldMap(unittest.TestCase):

    def setUp(self):
        pass

    def test_simulated_field_maps(self):

        # Get quantitative MR maps
        T1 = 1.
        T2 = .8
        PD = 1
        TR = 6e-3
        alpha = np.deg2rad(10)
        phase_cyc = 0

        # Monte Carlo: find the response that matches Mxy most closely
        num_sims = 1000
        err = 0
        tol = 1.
        beta = 1 # don't simulate df on the boundaries of the profile...
        ddf = .1
        for ii in trange(num_sims,leave=False,desc='Monte Carlo'):

            # Measure the signal in the real off-resonance environment
            df_true = np.random.uniform(low=-1/TR + beta,high=1/TR - beta)
            Mxy = ssfp(T1,T2,TR,alpha,df_true,phase_cyc=phase_cyc,M0=PD)

            # Find closest match and take that to be the off-resonance value
            df0 = quantitative_fm(Mxy,ddf,T1,T2,PD,TR,alpha,phase_cyc)
            if np.abs(df_true - df0) > tol:
                print('True: %g, found: %g' % (df_true,df0))
                err += 1

        self.assertFalse(err)


if __name__ == '__main__':
    unittest.main()
