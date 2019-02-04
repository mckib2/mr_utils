'''Acquire pairs of points that are close together (i.e., dtheta small).

Given a spectral profile, d(theta), any two points sampled along d(theta), say
m0 and m1, do not constrain d(theta) to a single possible profile.  Normally,
we sample at theta=0 and theta=180 degrees and then do a sum of squares for
optimal SNR banding reduction.  However, if we choose dtheta small, then we can
constrain d(theta) by two points plus the approximate derivative,
d/dtheta d(theta), at (theta1 - theta0)/2.

This script attempts to show that this will limit possible realizations of
d(theta) further than just taking two points 180 degrees apart.  We will also
try to apply the elliptical signal model with pairs of points taken at small
theta intervals.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp, get_keys

if __name__ == '__main__':

    # Search params
    TR = 6e-3
    dfs = np.linspace(-1/TR, 1/TR, 101)
    T1s = np.linspace(1.5, 2, 51)
    T2s = np.linspace(.5, 1.5, 51)
    alpha = np.pi
    keys = get_keys(T1s, T2s, np.atleast_1d(alpha))

    # Params for sim
    idx_true = np.random.randint(0, keys.shape[1])
    T1, T2, _ = keys[:, idx_true]
    df = np.random.choice(dfs)
    # df = 123.333
    phase_cycs = [0, np.pi/2]
    use_diff = False
    add_noise = False
    scale_fac = 1e17
    sigma = 0.25

    # Simulate acquisitions
    acqs = np.zeros(len(phase_cycs), dtype='complex')
    for ii, phase_cyc in enumerate(phase_cycs):
        acqs[ii] = ssfp(T1, T2, TR, alpha, df, phase_cyc=phase_cyc)*scale_fac

    # Add complex valued noise Gaussian noise to real/imag channels
    if add_noise:
        acqs += np.random.normal(0, sigma, acqs.shape) \
            + 1j*np.random.normal(0, sigma, acqs.shape)

    # Make a dictionary
    D = np.zeros((dfs.size, keys.shape[1]), dtype='complex')
    for ii, df0 in np.ndenumerate(dfs):
        D[ii, :] = ssfp(keys[0, :], keys[1, :], TR, alpha, field_map=df0) \
            *scale_fac

    # Find out where the second acquisition should be relative to first
    idx_away = (phase_cycs[1] - phase_cycs[0])/(2*np.pi)*(1/TR)
    idx_away = np.around(idx_away/(2/TR)*dfs.size).astype(int)
    print(idx_away)

    # Find error at each dictionary df
    err = np.zeros(D.shape)
    for ii in range(dfs.size):
        if use_diff:
            pass
            # # Here's where we need a term to do something with difference
            # diff = acqs[1] - acqs[0]

        else:
            # Use Euclidean distance
            for jj in range(len(phase_cycs)):
                err[ii, :] += np.abs(D[ii, :] - acqs[jj, None])
            # err[ii, :] = np.abs(D[ii, :] - acqs[0, None])

    # Look up the best match
    idx = np.unravel_index(np.argmin(err), D.shape)
    plt.plot(dfs, np.abs(D[:, idx[1]]),
             (dfs[idx[0]], dfs[np.mod(idx[0] + idx_away, dfs.size)]),
             np.abs(acqs), '.', label='Found')

    df2 = np.mod(df + (phase_cycs[1] - phase_cycs[0])/(2*np.pi)*(1/TR), 1/TR)
    plt.plot(dfs, np.abs(D[:, idx_true]), '--', (df, df2), np.abs(acqs), '.',
             label='True')

    plt.legend()
    plt.show()

    # Let's see how we did:
    print('Found:')
    print('    df: %g Hz' % dfs[idx[0]])
    print('    T1: %g sec' % keys[0, idx[1]])
    print('    T2: %g sec' % keys[1, idx[1]])

    print('True:')
    print('    df: %g Hz' % df)
    print('    T1: %g sec' % T1)
    print('    T2: %g sec' % T2)
