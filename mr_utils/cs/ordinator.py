'''Performs combinatorial optimization to find permutation maximizing sparsity.
'''

from functools import partial
from time import time
from multiprocessing import Pool
from itertools import combinations
import logging

import numpy as np
from tqdm import tqdm
from scipy.special import comb
from scipy.optimize import basinhopping, linear_sum_assignment as lsa
from scipy.spatial.distance import cdist

def obj(ck, N, locs, inverse, pdf_ref, pdf, pdf_metric):
    '''Objective function for basinhopping.'''
    c = np.zeros(N)
    c[locs] = ck
    xhat = inverse(c)
    xhat /= np.max(np.abs(xhat)) + np.finfo('float').eps
    return pdf_metric(pdf_ref, pdf(xhat))

def get_xhat(locs, N, k, inverse, pdf_ref, pdf, pdf_metric):
    '''Compute xhat for given coefficient locations using basinhopping.

    locs -- Coefficient location indices.
    N -- Length of the desired signal (also number of coefficients in total).
    k -- Desired sparsity level.
    inverse -- Inverse sparsifying transform.
    pdf_ref -- Reference pdf of the prior to compare against.
    pdf -- Function that estimates pixel intensity distribution.
    pdf_metric -- Function that returns the distance between pdfs.
    '''

    c0 = np.zeros(N)
    ck = np.zeros(k)
    res = basinhopping(
        obj, ck,
        minimizer_kwargs={'args':(N, locs, inverse, pdf_ref, pdf, pdf_metric)})
    c0[locs] = res['x']
    xhat = inverse(c0)
    xhat /= np.max(np.abs(xhat)) + np.finfo('float').eps
    return(xhat, locs, res['x'])

def search_fun(locs, N, k, inverse, pdf_ref, pdf, pdf_metric):
    '''Return function for parallel loop.

    locs -- Coefficient location indices.
    N -- Length of the desired signal (also number of coefficients in total).
    k -- Desired sparsity level.
    inverse -- Inverse sparsifying transform.
    pdf_ref -- Reference pdf of the prior to compare against.
    pdf -- Function that estimates pixel intensity distribution.
    pdf_metric -- Function that returns the distance between pdfs.
    '''
    xhat, locs, vals = get_xhat(
        [*locs], N, k, inverse, pdf_ref, pdf, pdf_metric)
    return(locs, vals, pdf_metric(pdf_ref, pdf(xhat)))

class pdf_default(object):
    '''Picklable object for computing pdfs.'''

    def __init__(self, prior):
        N = prior.size
        self.lims = (-1, 1)
        self.pdf_ref, self.bins = np.histogram(prior, bins=N, range=self.lims)

    def pdf(self, x):
        '''Estimate the pdf of x.'''
        if np.min(x) < self.lims[0]:
            tqdm.write('XHAT MIN WAS LOWER THAN X MIN: %g' % np.min(x))
        if np.max(x) > self.lims[1]:
            tqdm.write('XHAT MAX WAS HIGHER THAN X MAX: %g' % np.max(x))
        return np.histogram(x, self.bins, self.lims)[0]

def pdf_metric_default(x, y):
    '''Default pdf metric, l2 norm.'''
    return np.linalg.norm(x - y, ord=2)

def ordinator1d(prior, k, inverse, chunksize=10, pdf=None, pdf_metric=None,
                forward=None, disp=False):
    '''Find permutation that maximizes sparsity of 1d signal.

    prior -- Prior signal estimate to base ordering.
    k -- Desired sparsity level.
    inverse -- Inverse sparsifying transform.
    chunksize -- Chunk size for parallel processing pool.
    pdf -- Function that estimates pixel intensity distribution.
    pdf_metric -- Function that returns the distance between pdfs.
    forward -- Sparsifying transform (only required if disp=True).
    disp -- Whether or not to display coefficient plots at the end.

    pdf_method=None uses histogram.  pdf_metric=None uses l2 norm. If disp=True
    then forward transform function must be provided.  Otherwise, forward is
    not required, only inverse.

    pdf_method should assume the signal will be bounded between (-1, 1).  We do
    this by always normalizing a signal before computing pdf or comparing.
    '''

    # Make sure we have the forward transform if we want to display
    if disp and forward is None:
        raise ValueError('Must provide forward transform for display!')

    # Make sure we do in fact have a 1d signal
    if prior.ndim > 1:
        logging.warning('Prior is not 1d! Flattening!')
        prior = prior.flatten()
    N = prior.size

    # Go ahead and normalize the signal so we don't have to keep track of the
    # limits of the pdfs we want to compare, always between (-1, 1).
    prior /= np.max(np.abs(prior)) + np.finfo('float').eps

    # Default to histogram
    if pdf is None:
        pdf_object = pdf_default(prior)
        pdf = pdf_object.pdf
        pdf_ref = pdf_object.pdf_ref
    else:
        # Get reference pdf
        pdf_ref = pdf(prior)

    # Default to l2 metric
    if pdf_metric is None:
        pdf_metric = pdf_metric_default

    # Let's try to do things in parallel -- more than twice as fast!
    search_fun_partial = partial(
        search_fun, N=N, k=k, inverse=inverse, pdf_ref=pdf_ref,
        pdf_metric=pdf_metric, pdf=pdf)

    t0 = time() # start the timer
    with Pool() as pool:
        res = list(tqdm(pool.imap(
            search_fun_partial, combinations(range(N), k), chunksize),
                        total=comb(N, k, exact=True), leave=False))
    res = np.array(res)

    # Choose the winner
    winner_idx = np.where(res[:, -1] == res[:, -1].min())[0]
    potentials = []
    for idx0 in winner_idx:
        potentials.append(res[idx0, :])
        print('potential:', potentials[-1][0])
    print('Found %d out of %d (%%%g) potentials in %d seconds!' % (
        len(potentials), res.shape[0], len(potentials)/res.shape[0]*100,
        time() - t0))

    # Now solve the assignment problem, we only need one of the potentials, so
    # look at all of them and choose the one that is most sparse
    import matplotlib.pyplot as plt
    for potential in potentials:
        c = np.zeros(N)
        idx_proposed = potential[0]
        c[idx_proposed] = potential[1]
        xhat = inverse(c)
        xhat /= np.max(np.abs(xhat)) + np.finfo('float').eps
        C = cdist(xhat[:, None], prior[:, None])
        _rows, cols = lsa(C)

        if disp:
            tcoeffs = np.abs(forward(prior[cols]))
            # tcoeffs /= np.max(tcoeffs)
            plt.plot(-np.sort(-tcoeffs), '--', label='xpi')

    # Show reference coefficients
    if disp:
        # plt.plot(-np.sort(-np.abs(forward(xhat))), label='xhat')
        tcoeffs = np.abs(forward(np.sort(prior)))
        # tcoeffs /= np.max(tcoeffs)
        plt.plot(-np.sort(-tcoeffs), ':', label='sort(x)')
        plt.legend()
        plt.title('Sorted, Normalized Transform Coefficients')
        plt.show()

    return cols

if __name__ == '__main__':
    pass
