'''Relax the problem from integer programming to convex optimization.

This may or may not make sense to do...

Notes
=====
Using norm=None in concaluting xhat seems to do better.  It seems like we can
consistently beat the sort case with either obj1 or obj2, with obj2 performing
better (with same lambda weight, might need to tweak a bit to get a better
comparison).  In general, obj2 goes much faster, as lsa is not performed each
iteration, just a simple sorting operation.  We can't get Jacobian expressions
for either, unfortunately: 1) because of LSA operation, 2) because of sorting
operation.

This also appears to have the advantage of working under a wide variety of k --
small, large, consistently outperforming the sort(x) heuristic.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import idct

from mr_utils.cs import relaxed_ordinator

if __name__ == '__main__':

    lam = .5
    norm = False
    add_noise = False

    N = 70
    k = 5
    c_true = np.zeros(N)
    idx_true = np.random.choice(np.arange(N), k)
    c_true[idx_true] = np.random.normal(2, 1, k)
    xpi = idct(c_true, norm='ortho')
    xpi /= np.max(np.abs(xpi))

    # # Show xpi
    # plt.plot(xpi)
    # plt.stem(dct(xpi, norm='ortho'))
    # plt.show()

    # Now jumble up to get our real signal
    pi = np.random.permutation(np.arange(N))
    x = xpi[pi]

    # Make it noisy if we want that
    if add_noise:
        x += np.random.normal(0, 1, x.shape)

    # # Show the messy x signal
    # plt.plot(x)
    # plt.stem(dct(x, norm='ortho'))
    # plt.show()

    # Find the ordering!
    pi = relaxed_ordinator(x, lam, k, lambda c0: idct(c0, norm='ortho'))

    # Let's take a look...
    plt.plot(-np.sort(-np.abs(idct(x, norm='ortho'))), label='x')
    plt.plot(-np.sort(-np.abs(idct(x[pi], norm='ortho'))), label='xpi')
    plt.plot(
        -np.sort(-np.abs(idct(np.sort(x), norm='ortho'))), label='sort(x)')
    plt.legend()
    plt.show()
