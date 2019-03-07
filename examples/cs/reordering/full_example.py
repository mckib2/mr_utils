'''Search all coefficient combinations and use basinhopping at each step.

Exhaustively search each possible class of k-sparse signals.  For each class,
solve for coefficient values that minimize the histogram error using a global
optimization technique.  In this case, we choose the basinhopping algorithm.

I also introduce the notion that we might not expect the coefficient locations
to be in the high frequency locations -- since the sorted signal removes high
frequencies.  So we can restrict the effective search space from n choose k to
something like n/r choose k, where r is a reduction factor (r > 1).
'''

from itertools import combinations
from functools import partial
from multiprocessing import Pool
from time import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from scipy.special import comb
from scipy.optimize import basinhopping, linear_sum_assignment as lsa
from scipy.spatial.distance import cdist
from tqdm import tqdm

from mr_utils.utils.histogram import dH

def forward(x):
    '''Forward transform.'''
    return dct(x, norm='ortho')

def inverse(c):
    '''Inverse transform.'''
    return idct(c, norm='ortho')

def density(x0, bins, lims):
    '''Return density estimate of x0.'''
    return np.histogram(x0, bins, lims)[0]

def obj(ck, N, locs, Href, bins, lims, mode, xref):
    '''Objective function for basinhopping.'''
    c = np.zeros(N)
    c[locs] = ck
    xhat = inverse(c)
    # Compare directly to xref -- this seems the same as comparing histogram?
    # Just loose some of the binning properties we might like
    if xref is not None:
        return np.linalg.norm(np.sort(xhat) - np.sort(xref))**2
    return dH(Href, density(xhat, bins, lims), mode=mode)

def get_xhat(N, locs, Href, bins, lims, mode, xref):
    '''Compute xhat for given coefficient locations using basinhopping.

    N -- Length of desired signal (also number of coefficients in total).
    locs -- Locations of coefficients defining the class of k-sparse signal.
    Href -- Reference histogram.
    bins -- Bin locations, should be the same as reference histogram.
    lims -- Limits used to construct histogram, should be same as reference.
    mode -- Mode to run histogram metric: {'l1', 'l2', 'emd', etc...}.
    '''

    c0 = np.zeros(N)
    ck = np.zeros(k)
    res = basinhopping(
        obj,
        ck,
        minimizer_kwargs={'args':(N, locs, Href, bins, lims, mode, xref)})
    c0[locs] = res['x']
    xhat = inverse(c0)
    return(xhat, locs, res['x'])

def search_fun(cc, N, Href, bins, lims, mode, xref):
    '''Return function for parallel loop.'''
    xhat, locs, vals = get_xhat(N, [*cc], Href, bins, lims, mode, xref)

    if np.min(xhat) < lims[0]:
        print('XHAT MIN WAS LOWER THAN X MIN!')
    if np.max(xhat) > lims[1]:
        print('XHAT MAX WAS HIGHER THAN X MAX!')

    return(locs, vals, dH(Href, density(xhat, bins, lims), mode=mode))

if __name__ == '__main__':

    # Assume there is a k-sparse representation,
    N = 30
    k = 5
    Neff = int(N/2) # Search a reduced space
    chunksize = 10
    cx = np.zeros(N)
    idx_true = np.random.choice(np.arange(N), k, False)
    cx[idx_true] = np.random.normal(1, 1, k)
    xpi = inverse(cx)

    # We measure a permutation of x
    pi_true = np.random.permutation(np.arange(N))
    x = xpi[pi_true]

    # Thus the pixel intensity distribution of x is the that of y
    lims = (2*np.min(x), 2*np.max(x)) # adjust until xhat always fits into lims
    Hx, bins = np.histogram(x, bins=N, range=lims)

    # Let's try to do things in parallel -- more than twice as fast!
    mode = 'l2'
    search_fun_partial = partial(
        search_fun, N=N, Href=Hx, bins=bins, lims=lims, mode=mode, xref=x)

    t0 = time() # start the timer
    with Pool() as pool:
        res = list(tqdm(pool.imap(
            search_fun_partial, combinations(range(Neff), k), chunksize),
                        total=comb(Neff, k, exact=True), leave=False))
    res = np.array(res)

    # Choose the winner
    winner_idx = np.where(res[:, -1] == res[:, -1].min())[0]
    potentials = []
    for idx0 in winner_idx:
        potentials.append(res[idx0, :])
        print('potential:', potentials[-1][0])
    print('Actual:', np.sort(idx_true))
    print('Found %d out of %d (%%%g) potentials in %d seconds!' % (
        len(potentials), res.shape[0], len(potentials)/res.shape[0]*100,
        time() - t0))

    # See if we found the correct indices
    if np.sort(idx_true).tolist() in [p[0] for p in potentials]:
        print('WE WIN!')
    else:
        print('FAILED TO FIND CORRECT INDICES!')

    # Now solve the assignment problem, we only need one of the potentials, so
    # look at all of them and choose the one that is most sparse
    for ii, potential in enumerate(potentials):
        c = np.zeros(N)
        idx_proposed = potential[0]
        c[idx_proposed] = potential[1]
        xhat = inverse(c)
        C = cdist(xhat[:, None], x[:, None])
        rows, cols = lsa(C)
        plt.plot(-np.sort(-np.abs(forward(x[cols]))), '--', label='xpi%d' % ii)

    # # Show reference coefficients
    plt.plot(-np.sort(-np.abs(forward(xhat))), label='xhat')
    plt.plot(-np.sort(-np.abs(forward(np.sort(x)))), ':', label='sort(x)')
    plt.legend()
    plt.title('Sorted DCT Coefficients')
    plt.show()
