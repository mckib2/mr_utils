'''Acquire pairs of points that are close together (i.e., dtheta small).

Given a spectral profile, d(theta), any two points sampled along d(theta), say
m0 and m1, do not constrain d(theta) to single possible profile.  Normally, we
sample at theta=0 and theta=180 degrees and then do a sum of squares for
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
    T1s = np.linspace(1, 2, 11)
    T2s = np.linspace(.5, 2, 11)

    # Params for sim
    alpha = np.pi
    T1 = 1.8
    T2 = 0.8
    df = .3/TR
    phase_cycs = [0, np.pi]
    print('phase cycles: ', phase_cycs)
    use_offset = True

    # Simulate acquisitions
    acqs = np.zeros(len(phase_cycs), dtype='complex')
    for ii, phase_cyc in enumerate(phase_cycs):
        acqs[ii] = ssfp(T1, T2, TR, alpha, df, phase_cyc=phase_cyc)

    # Make a dictionary
    keys = get_keys(T1s, T2s, np.atleast_1d(alpha))
    D = np.zeros((dfs.size, keys.shape[1]), dtype='complex')
    for ii, df0 in np.ndenumerate(dfs):
        D[ii, :] = ssfp(keys[0, :], keys[1, :], TR, alpha, field_map=df0)

    # Find out where the second acquisition should be relative to first
    idx_away = (phase_cycs[1] - phase_cycs[0])/(2*np.pi)*(1/TR)
    idx_away = np.around(idx_away/(2/TR)*dfs.size).astype(int)
    print(idx_away)

    # Find error at each dictionary df
    err = np.zeros(D.shape)
    for ii in range(dfs.size):
        if use_offset:

            tmp1 = np.abs(D[ii, :] - acqs[0, None])
            tmp2 = np.abs(D[ii, :] - acqs[1, None])
            err[ii, :] = tmp1 + tmp2

        else:
            err[ii, :] = np.abs(D[ii, :] - acqs[0])

    # Look up the best match
    idx = np.unravel_index(np.argmin(err), D.shape)
    plt.plot(dfs, np.abs(D[:, idx[1]]))
    plt.plot((dfs[idx[0]], dfs[np.mod(idx[0] + idx_away, dfs.size)]),
             np.abs(acqs), '*')
    plt.show()

    print('Found:')
    print('    df: %g' % dfs[idx[0]])
    print('    T1: %g' % keys[0, idx[1]])
    print('    T2: %g' % keys[1, idx[1]])

    print('True:')
    print('    df: %g' % df)
    print('    T1: %g' % T1)
    print('    T2: %g' % T2)
