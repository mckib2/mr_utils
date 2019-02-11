'''Generate figures for paper.'''

import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy.spatial.distance import cosine as vcos_dist
from scipy.spatial.distance import jensenshannon
from scipy.stats import wasserstein_distance
from scipy.optimize import minimize

from mr_utils.utils.wavelet import wavelet_forward, wavelet_inverse
from mr_utils.utils.orderings import inverse_permutation
from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils import view

def plot_coeffs(c, *kargs):
    '''Plot sorted coefficients, c.'''
    plt.plot(-np.sort(-np.abs(c.flatten())))

    for cs in kargs:
        plt.plot(-np.sort(-np.abs(cs.flatten())))

    plt.show()

def H_metric(H1, H2, mode='chi2'):
    '''Histogram metrics.

    H1, H2 -- 1d histograms with matched bins.
    mode -- Metric to use.

    Modes:
        l2 -- Euclidean distance
        l1 -- Manhattan distance
        vcos -- Vector cosine distance
        intersect -- Histogram intersection distance
        chi2 -- Chi square distance
        jsd -- Jensen-Shannan Divergence
        emd -- Earth Mover's Distance
    '''

    if mode == 'l2':
        return np.linalg.norm(H1 - H2, ord=2)
    if mode == 'l1':
        return np.linalg.norm(H1 - H2, ord=1)
    if mode == 'vcos':
        return vcos_dist(H1, H2)
    if mode == 'intersect':
        return np.sum(np.min(np.stack((H1, H2)), axis=0))
    if mode == 'chi2':
        a = 2*((H1 - H2)**2).astype(float)
        b = H1 + H2
        return np.sum(np.divide(a, b, out=np.zeros_like(a), where=b != 0))
    if mode == 'jsd':
        return jensenshannon(H1, H2)
    if mode == 'emd':
        return wasserstein_distance(H1, H2)

    raise NotImplementedError()


if __name__ == '__main__':

    # Make a phantom to work with, shepp_logan will do
    dim = 50
    x = np.rot90(modified_shepp_logan((dim,)*3)[:, :, int(dim/2)])
    # view(x)

    # Define transform
    level = 1
    wavelets = ['haar', 'db', 'sym', 'coif', 'bior', 'rbio', 'dmey']
    modes = ['zero', 'constant', 'symmetric', 'reflect', 'periodic', 'smooth',
             'periodization']
    wavelet = wavelets[0]
    mode = modes[-1]
    wvlt, loc = wavelet_forward(x, wavelet, mode, level)
    T = lambda x: wavelet_forward(x, wavelet, mode, level)[0]
    Ti = lambda x: wavelet_inverse(x, loc, wavelet, mode)
    assert np.allclose(x, Ti(T(x)))
    # view(Ti(wvlt))

    # Construct a k-sparse signal
    # k = int(x.size/11)
    k = int(np.count_nonzero(wvlt)*.1)
    # k = 100
    print('We are looking for k=%d nonzero (%%%g)' % (k, 100*k/x.size))

    # Thresholding won't work because we're taking out a set number, and some
    # coefficients, especially in synthetic datasets, will be the same
    cs = T(x).flatten()
    idx = np.argsort(-np.abs(cs))
    cs = cs[idx]
    cs[k:] = 0
    cs = cs[inverse_permutation(idx)]
    assert k == np.count_nonzero(cs)

    # Reconstruct x_hat
    x_hat = Ti(cs.reshape(x.shape))

    # Show the coefficients
    plot_coeffs(wvlt, cs)

    # Construct histograms, make sure all bins are the same so we can compare
    # them
    mn = np.min(np.min((x, x_hat)))
    mx = np.max(np.max((x, x_hat)))
    H1, bins = np.histogram(x, bins='fd', range=(mn, mx))
    H2, _ = np.histogram(x_hat, bins=bins, range=(mn, mx))

    # As you can see, the histograms don't match up very well.  They're
    # but we might potentially do better!
    plt.plot(bins[:-1], H1, '.')
    plt.plot(bins[:-1], H2, '.')
    plt.show()

    # First we'll need to define a metric, here's all possible, leaning
    # toward l2 because we might be able to do things analytically with that
    H_metrics = ['l2', 'l1', 'vcos', 'intersect', 'chi2', 'jsd', 'emd']
    h_met = 6 #2
    # for hm in H_metrics:
    #     print('%s distance: %g' % (hm, H_metric(H1, H2, mode=hm)))


    # Now solve for the values of the coefficients that minimizes the
    # histogram cost metric

    # # This does not sort coefficients!
    # idx = np.argpartition(np.abs(T(x).flatten()), -k)[-k:]
    # c = T(x).flatten()[idx]
    # # idx = np.random.choice(x.size, k, replace=False)
    # # print(k, idx.shape)

    def make_hist(c0, idx):
        '''Make a histogram from c coefficients.'''
        coeffs = np.zeros(x.size)
        coeffs[idx] = c0
        coeffs = coeffs.reshape(x.shape)
        H, _ = np.histogram(Ti(coeffs), bins, range=(mn, mx))
        return H

    from scipy.optimize import least_squares
    idx = np.argsort(-np.abs(cs))[:k]
    x0 = cs[idx]
    res = least_squares(
        lambda y: H_metric(H1, make_hist(y, idx), H_metrics[h_met]), x0)
    print(res)
    # assert not np.allclose(res['x'], cs[idx])
    H3 = make_hist(res['x'], idx)

    # We can get a bit closer with clever choice of histogram metric
    plt.plot(H1, '--', label='Target')
    plt.plot(H2, '.', label='Truncated')
    plt.plot(H3, '.', label='Fit')
    plt.legend()
    plt.show()

    # Could we pick better indices?  Try sorting in 2-dimensions, then
    # truncating.  Obviously, the histograms between sorted and unsorted x will
    # be the same
    from mr_utils.utils.sort2d import sort2d
    x_2d, idx_2d = sort2d(x)
    wvlt_2d = T(x_2d).flatten()
    assert np.count_nonzero(wvlt_2d) > k, \
        'We are trying to do better than sort2d!'
    idx = np.argsort(-np.abs(wvlt_2d))[:k]
    cs = wvlt_2d[idx]
    H4 = make_hist(cs, idx)
    plt.plot(H1)
    plt.plot(H4)
    plt.show()

    # Try the same tuning technique
    x0 = cs.copy()
    res = least_squares(
        lambda y: H_metric(H1, make_hist(y, idx), H_metrics[h_met]), x0)
    print(res)
    # assert not np.allclose(res['x'], x0)
    H5 = make_hist(res['x'], idx)
    plt.plot(H1, '--', label='Target')
    plt.plot(H4, '.', label='Truncated Sort2d')
    plt.plot(H5, '.', label='Fit Sort2d')
    plt.legend()
    plt.show()

    # Well we're still off, and not even sorting first can fix all of it.  So
    # let's look around a little for better choices of coefficients.  Swap
    # individual coefficients greedily
    from tqdm import trange, tqdm
    winner = cs.copy()
    winner_score = H_metric(H1, make_hist(winner, idx), H_metrics[h_met])
    not_idx = np.setdiff1d(np.arange(x.size), idx, True)
    for cc in trange(k, leave=False):
        for ii in trange(not_idx.size, leave=False):

            idx0 = idx.copy()
            idx0[cc] = not_idx[ii]
            x0 = winner.copy()
            x0[cc] = 1
            res = least_squares(lambda y: H_metric(H1, make_hist(y, idx0), \
                H_metrics[h_met]), x0)

            score = H_metric(H1, make_hist(res['x'], idx0), H_metrics[h_met])
            if score < winner_score:
                idx = idx0
                winner = res['x']
                winner_score = score
                tqdm.write('We won! Score: %g' % winner_score)

    # This greedy algorithm seems to match the histogram better!
    H6 = make_hist(winner, idx)
    plt.plot(H1, '-', label='Target')
    plt.plot(H4, '--', label='Truncated Sort2d')
    plt.plot(H5, '.', label='Fit Sort2d')
    plt.plot(H6, '.', label='Searched')
    plt.legend()
    plt.show()

    # Now we want to create pi, the mapping from x to x_hat
    from mr_utils.utils.orderings import random_match
    coeffs = np.zeros(x.size)
    coeffs[idx] = winner
    coeffs = coeffs.reshape(x.shape)
    pi = random_match(x, Ti(coeffs))

    plot_coeffs(
        T(x), T(x_2d), T(x[np.unravel_index(pi, x.shape)].reshape(x.shape)))

    # # See which metric gives us the most improvement
    # cost = lambda coeffs, idx, hm: H_metric(H1, make_hist(coeffs, idx), hm)
    # for hm in H_metrics:
    #     print('For %s:' % hm)
    #     print('    Before: %g' % cost(c, idx, hm))
    #     res = minimize(cost, T(x_hat).flatten()[idx], args=(idx, hm,))
    #     print('     After: %g' % cost(res['x'], idx, hm))
    #
    #     plt.plot(bins[:-1], H1)
    #     plt.plot(bins[:-1], H2, '--')
    #     plt.plot(bins[:-1], make_hist(res['x'], idx), '-.')
    #     plt.show()

    # # Since that did almost nothing...
    # from itertools import permutations
    # from math import factorial
    # from tqdm import tqdm
    # idx = range(x.size)
    # for p in tqdm(permutations(idx), total=factorial(x.size)):


    # M = 10
    # m = int(k*.01)
    # cur_cost = cost(c, idx)
    # print('Starting at %g' % cur_cost)
    # for ii in range(M):
    #     print('iter %d:' % ii)
    #
    #     # Find the m lowest coefficients
    #     idx0 = np.argsort(np.abs(c))[:m]
    #
    #     # Swap in m random indices
    #     prospective_idx = idx.copy()
    #     prospective_idx[idx0] = np.random.choice(x.size, m, False)
    #
    #     # Now find the coefficient values that minimize histogram cost
    #     res = minimize(cost, c.copy(), args=(prospective_idx,))
    #     prospective_cost = cost(res['x'], prospective_idx)
    #     if prospective_cost < cur_cost:
    #         c = res['x']
    #         idx = prospective_idx
    #         cur_cost = prospective_cost
    #         print('Accepted %g' % cur_cost)
