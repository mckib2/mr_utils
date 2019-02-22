'''Example about how to use PLANET with noisy data.

So as far as I can tell, this implementation is failing whenever there is any
noise, no matter how small.  It's probably due to how the ellipse is being
rotated.
'''

import numpy as np
from tqdm import trange, tqdm

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET

if __name__ == '__main__':

    num_pc = 10
    I = np.zeros(num_pc, dtype='complex')
    pcs = [2*np.pi*n/num_pc for n in range(num_pc)]
    TR = 10e-3
    T1s = np.linspace(.2, 2, 100)
    alpha = np.deg2rad(30)

    # Noise parameters
    mu = 0
    sigma = 1

    iters = 1
    misses = 0
    asserts = 0
    for jj in trange(iters, leave=False):
        df_true = np.random.uniform(-1/TR, 1/TR)
        T1_true = np.random.choice(T1s)
        T2_true = np.random.uniform(.01, .8*T1_true)
        for ii, pc in enumerate(pcs):
            I[ii] = ssfp(T1_true, T2_true, TR, alpha, df_true, pc)
        I += np.random.normal(mu, sigma/2) + 1j*np.random.normal(mu, sigma/2)
        try:
            Meff, T1, T2 = PLANET(I, alpha, TR, T1s, disp=True)
            if not np.allclose([T1, T2], [T1_true, T2_true]):
                misses += 1
        except AssertionError as e:
            tqdm.write(str(e))
            asserts += 1

    print('%d missed out of %d, %%%g' % (misses, iters, misses/iters*100))
    print('%d assert out of %d, %%%g' % (asserts, iters, asserts/iters*100))
