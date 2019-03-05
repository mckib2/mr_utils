'''Do the search through all possible k-sparse to match densities in 1d.

Here we consider the 1d case of signals known to be k-spare under the DCT.
We do a brute force search through all possible k-sparse signals to try to
find the correct one.

Histogram constraints using l2-metric is used.  Coefficient values are solved
using scipy.optimize.minimize.

What's interesting is that we perform better than sorting especially at small
N.  So patch based processing with reordering has the potential to be really
good.
'''

from itertools import combinations
from functools import reduce, partial
import operator as op
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from scipy.special import comb
from scipy.optimize import linear_sum_assignment as lsa
# from scipy.optimize import minimize
from scipy.spatial.distance import cdist
from tqdm import tqdm

from mr_utils.utils.histogram import dH

def density(x0, bins, lims):
    '''Return density estimate of x0.'''
    return np.histogram(x0, bins, lims)[0]

def nCr(n, r):
    '''nCr function.'''
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

def kthCombination(k, l, r):
    '''Get the kth combination.'''
    if r == 0:
        return []
    if len(l) == r:
        return l

    i = nCr(len(l)-1, r-1)
    if k < i:
        return l[0:1] + kthCombination(k, l[1:], r-1)

    return kthCombination(k-i, l[1:], r)

def obj(c00, N, locs, bins, lims):
    '''Objective: choose c0 to minimize difference between histograms.'''
    c0 = np.zeros(N)
    c0[locs] = c00
    return dH(Hy, density(idct(c0), bins, lims))

def get_xhat(N, locs, _bins, _lims):
    '''Compute xhat for given coefficient locations.'''

    # Assume the coefficient is always one for now while we figure the math out
    # c00 = np.ones(k)
    # res = minimize(obj, c00, args=(N, locs, bins, lims,))
    c0 = np.zeros(N)
    # c0[locs] = res['x']
    c0[locs] = 1
    xhat = idct(c0)
    xhat /= np.linalg.norm(xhat)
    return xhat

def err_fun(cc, N, bins, lims):
    '''Error function for parallel loop.'''
    xhat = get_xhat(N, [*cc], bins, lims)
    return dH(Hy, density(xhat, bins, lims), mode='l2')

if __name__ == '__main__':

    # Assume there is a k-sparse representation,
    N = 30 # these choices of N,k give unique solution most of the time
    k = 3
    cx = np.zeros(N)
    idx_true = np.random.choice(np.arange(N), k, False)
    cx[idx_true] = 1# + np.random.normal(0, 1, k)
    x = idct(cx)
    x /= np.linalg.norm(x)

    # We measure a permutation of x
    pi_true = np.random.permutation(np.arange(N))
    y = x[pi_true]

    # Thus the pixel intensity distribution of x is the that of y
    lims = (-.5, .5)
    Hy, bins = np.histogram(y, bins=N, range=lims)

    # Let's try to do things in parallel -- more than twice as fast!
    err_fun_partial = partial(err_fun, N=N, bins=bins, lims=lims)
    with Pool() as pool:
        res = list(tqdm(pool.imap(err_fun_partial, combinations(range(N), k),
                                  chunksize=1000),
                        total=comb(N, k, exact=True), leave=False))
    err = np.array(res)

    # # we need to search through all N choose k possible k-sparse signals
    # err = np.zeros(comb(N, k, exact=True))
    # for ii, cc in tqdm(enumerate(
    #         combinations(range(N), k)), total=err.size, leave=False):
    #
    #     # We have the k locations, now we need to find the values
    #     xhat = get_xhat(N, [*cc], bins, lims)
    #     err[ii] = dH(Hy, density(xhat, bins, lims), mode='l2')

    # Choose the winner
    winner_idx = np.where(err == err.min())[0]
    potentials = []
    for idx0 in winner_idx:
        potentials.append(kthCombination(idx0, list(range(N)), k))
        print('potential:', potentials[-1])
    print('Actual:', np.sort(idx_true))
    print('Found %d out of %d (%%%g) potentials!' % (
        len(potentials), err.size, len(potentials)/err.size*100))

    # See if we found the correct indices
    if np.sort(idx_true).tolist() in potentials:
        print('WE WIN!')
    else:
        print('FAILED TO FIND CORRECT INDICES!')

    # Search potentials -- but we really only wanted one...
    # We're going to need another constraint if we want to make the solution
    # unique...  But all we need is "a" solution, right?
    for pot in potentials:

        # Match y to xhat
        xhat = get_xhat(N, pot, bins, lims)
        C = cdist(xhat[:, None], y[:, None])
        rows, cols = lsa(C)

        plt.subplot(1, 3, 1)
        plt.plot(xhat, label='xhat')
        plt.plot(y[cols], '--', label='y_pi')
        plt.plot(np.sort(y), ':', label='sort(y)')
        plt.title('Reordered y')
        plt.legend()
        plt.subplot(1, 3, 2)
        plt.plot(-np.sort(-np.abs(dct(xhat))), label='xhat')
        plt.plot(-np.sort(-np.abs(dct(y[cols]))), '--', label='y_pi')
        plt.plot(-np.sort(-np.abs(dct(np.sort(y)))), ':', label='sort(y)')
        plt.title('Sorted DCT Coefficients')
        plt.legend()
        plt.subplot(1, 3, 3)
        plt.plot(bins[:-1], Hy, label='Hy')
        plt.plot(bins[:-1], density(xhat, bins, lims), '--', label='Hxhat')
        plt.title('Histograms')
        plt.legend()
        plt.show()
