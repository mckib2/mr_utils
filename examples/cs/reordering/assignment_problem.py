'''Reordering assignment by minimum weight matching.

This is a simplistic example where we assume a k-sparse signal under the DCT.
We then take a bunch of random measurements which is not sparse under the DCT.
Then we match y to x by casting it as the assignment problem and using an
out-of-the-box scipy solver to do it for us.  Once we've found the assignments,
we use this as the reordering of y to make it look like x, which was by
assumption k-sparse!  Assigned y has many nonzero components, but the most
significant k match those of x.

The point of this exercise is to show that given even random data, we can make
it match a signal we know to be k-sparse, and thus be approximately k-sparse
itself.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment as lsa
from scipy.fftpack import dct, idct
from scipy.spatial.distance import cdist

if __name__ == '__main__':

    # Make a signal that we want to approximate sparse under DCT
    N = 400
    x = np.zeros(N)
    k = 20
    idx = np.random.choice(np.arange(N), k, False)
    x[idx] = 1
    x = idct(x)
    x /= np.max(np.abs(x))

    # We get what we get -- choose random for simplicity
    y = np.random.random(N)*2 - 1
    y /= np.max(np.abs(y))

    # y is not sparse under DCT
    plt.plot(dct(x))
    plt.plot(dct(y), '--')
    plt.show()

    # Now match y to x
    C = cdist(x[:, None], y[:, None])
    rows, cols = lsa(C)

    # Now y matches x and is (mostly) sparse under DCT!  Kill all but the
    # largest k coefficients of y
    cy = dct(y[cols])
    cy[np.argsort(np.abs(cy))[:-k]] = 0
    plt.plot(dct(x))
    plt.plot(cy, '--')
    plt.show()

    plt.plot(x)
    plt.plot(idct(cy)/np.max(np.abs(idct(cy))), '--')
    plt.show()

    # Does it work with a 2d array?
    N = int(np.sqrt(N))
    x = np.zeros((N, N))
    idx = np.random.choice(np.arange(x.size), k, False)
    x[np.unravel_index(idx, x.shape)] = 1
    x = idct(idct(x, axis=0), axis=1)
    x /= np.max(np.max(np.abs(x)))

    # Make y similar to last time, random
    y = np.random.random(x.shape)*2 - 1
    y /= np.max(np.max(np.abs(y)))

    # Show x sparse, y not so sparse
    plt.subplot(1, 2, 1)
    plt.imshow(dct(dct(x, axis=0), axis=1))
    plt.subplot(1, 2, 2)
    plt.imshow(dct(dct(y, axis=0), axis=1))
    plt.show()

    # Match maker, match maker, make me a match!
    C = cdist(x.flatten()[:, None], y.flatten()[:, None])
    rows, cols = lsa(C)

    # Show that we've got a match
    plt.subplot(1, 2, 1)
    plt.imshow(dct(dct(x, axis=0), axis=1))
    plt.subplot(1, 2, 2)
    plt.imshow(dct(dct(y.flatten()[cols].reshape(x.shape), axis=0), axis=1))
    plt.show()

    # May want to select only k largest coefficients again here, but you get
    # the picture...
