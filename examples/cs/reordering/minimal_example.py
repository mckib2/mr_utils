'''Make a minimal example showing how this is supposed to work.

Should be small enough for us to exhaustively search for the best solution as
to show that we can do better than montonically sorting.  We will consider a
simple 1d signal known to be sparse under the discrete cosine transform after
reordering.
'''

import numpy as np
from scipy.fftpack import dct
import matplotlib.pyplot as plt

from mr_utils.utils.histogram import dH
from mr_utils.utils.orderings import random_match

if __name__ == '__main__':

    # Make a very simple signal derived from a simple dictionary, n must be
    # large enough to give us a good histogram to work with
    n = 9
    D = dct(np.eye(n))
    true_idx = int(n/2)
    x_pi = 2.5*D[:, true_idx]
    tol = 1e-10

    # We do infact have a 1-sparse signal
    plt.plot(x_pi)
    plt.show()
    plt.plot(dct(x_pi))
    plt.show()

    # Now randomly mix it up, and we have a not-so-sparse signal
    np.random.seed(0)
    x = np.random.permutation(x_pi)
    print('Number nonzero coefficients of x: %d' \
        % np.count_nonzero(np.abs(dct(x)) > tol))
    plt.plot(x)
    plt.show()
    plt.plot(dct(x))
    plt.show()

    # Apply simple heuristic of sorting montonically
    x_sort = np.sort(x)
    print('Number nonzero coefficients of montonically sorted x: %d' \
        % np.count_nonzero(np.abs(dct(x_sort)) > tol))
    plt.plot(x_sort)
    plt.show()
    plt.plot(dct(x_sort))
    plt.plot(dct(x))
    plt.show()

    # Find the histogram of x and constrain bins from here on out
    # Need to be careful about range we bin over, so let's normalize all
    # values to be in (-1, 1)
    Hx, bins = np.histogram(x/np.max(np.abs(x)), bins='fd')
    print('Constructed histogram of x with %d bins' % bins[:-1].size)
    # plt.bar(bins[:-1], Hx)
    # plt.show()

    # Construct by exhaustive search the 1-sparse signal whose histogram
    # matches that of x.  Since we expect 1-sparse, we only need to go through
    # one coefficient at a time
    err = np.zeros(n)
    for ii in range(n):

        # Choose coefficient ii
        y = D[:, ii]
        Hy, _ = np.histogram(y/np.max(np.abs(y)), bins=bins)
        # plt.bar(bins[:-1], Hy)
        # plt.show()

        # Find difference between normalized histograms
        err[ii] = dH(Hx, Hy, mode='chi2')
        # print(err[ii])

    guess_idx = np.argmin(err)
    print('Winner is %d, true is %d' % (guess_idx, true_idx))

    # Now construct the 1-sparse signal x_hat defined by the coefficient we
    # chose, take the normalized x_hat to be our estimate of x_pi
    x_hat = D[:, guess_idx]
    plt.plot(x_pi/np.max(np.abs(x_pi)))
    plt.plot(x_hat/np.max(np.abs(x_hat)), '--')
    plt.show()

    # Since x_pi by assumption was the permuted signal x, we need to map all
    # the pixels of x to x_hat (our guess of what x_pi is), and call this the
    # reordering.  Obviously, the histograms in general will be not be
    # identical (although that would be ideal).  If they are not, we need a
    # strategy for matching pixels from x_hat to x.  I can think of two off the
    # top of my head:
    #     1) Histogram matching -- ignore relative variations in pixels and
    #        the effect this might have on sparsity.  This means a gauranteed
    #        unambigous mapping but will not be optimally sparse.
    #     2) Bipartite traveling salesman -- Find the matchings of least
    #        resistance between x and x_hat and choose these.  This will be the
    #        best you can do assuming a k-sparse signal exists and you found
    #        the correct k coefficients and their values in the step before
    #        this one.

    # For now, while I don't have either of these implemented, this example is
    # simple enough that we get a really git histogram match, so use a
    # randomized matcher
    pi = random_match(x/np.max(np.abs(x)), x_hat/np.max(np.abs(x_hat)))
    print('Number nonzero coefficients using constructed pi: %d' \
        % np.count_nonzero(np.abs(dct(x[pi])) > tol))

    plt.plot(x_pi/np.max(np.abs(x_pi)))
    plt.plot(x[pi]/np.max(np.abs(x)))
    plt.show()

    plt.plot(dct(x[pi]))
    plt.plot(dct(x_sort))
    plt.show()
