'''Example about how to use PLANET and some if its error characteristics.
'''

import numpy as np
# import matplotlib.pyplot as plt
from tqdm import trange, tqdm

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET

if __name__ == '__main__':

    num_pc = 10
    I = np.zeros(num_pc, dtype='complex')
    pcs = np.linspace(0, 2*np.pi, num_pc, endpoint=False)
    TR = 10e-3
    M0 = 1
    T1s = np.linspace(.2, 2, 100)
    alpha = np.deg2rad(30)
    sigma = 0.0005

    iters = 1000
    T1_true = np.zeros(iters)
    T2_true = np.zeros(iters)
    df_true = np.zeros(iters)

    T1_est = np.zeros(iters)*np.nan
    T2_est = np.zeros(iters)*np.nan
    df_est = np.zeros(iters)*np.nan

    asserts = 0
    for jj in trange(iters, leave=False):
        # Try to stay away from edges, (-1/TR, 1/TR) gets confused at bnds
        df_true[jj] = np.random.uniform(-1/(2*TR), 1/(2*TR))
        T1_true[jj] = np.random.choice(T1s)
        T1_guess = T1_true[jj]
        T2_true[jj] = np.random.uniform(.01, .5*T1_true[jj])

        I = ssfp(T1_true[jj], T2_true[jj], TR, alpha, df_true[jj], pcs, M0=M0)
        n = np.random.normal(0, sigma/2, I.shape) + 1j*np.random.normal(
            0, sigma/2, I.shape)
        I += n

        try:
            _Meff, T1_est[jj], T2_est[jj], df_est[jj] = PLANET(
                I, alpha, TR, T1_guess, compute_df=True)
        except AssertionError as e:
            tqdm.write(str(e))
            asserts += 1

    # Compute percent difference
    T1diff = 100*(T1_true - T1_est)/T1_true
    T2diff = 100*(T2_true - T2_est)/T2_true
    dfdiff = 100*(df_true - df_est)/df_true

    # Tell us all about it
    print('T1 %%err, mean: %%%g, std: %g' % (
        np.nanmean(T1diff), np.nanstd(T1diff)))
    print('T2 %%err, mean: %%%g, std: %g' % (
        np.nanmean(T2diff), np.nanstd(T2diff)))
    print('df %%err, mean: %%%g, std: %g' % (
        np.nanmean(dfdiff), np.nanstd(dfdiff)))

    if asserts > 0:
        print(
            '%d asserts out of %d, %%%g' % (asserts, iters, asserts/iters*100))
