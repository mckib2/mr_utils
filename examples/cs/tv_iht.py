'''Total variation example using iterative hard thresholding.

This is actually a dumb example, because the assumption we make a square wave
which turns out to be a binary signal in finite differences domain, but it's
treated as the sample problem as binary_iht.py.  Sorry about that.
The measurements should actually be taken in the nonsparse domain (i.e.,
y = As instead of y = Ax).
'''

import logging

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

from  mr_utils.cs import IHT

if __name__ == '__main__':
    N = 2000
    n = 500
    k = 30

    # Make a sparse signal in TV domain -- how about a square wave!
    s = np.sin(np.pi*np.arange(N+1)*k/(N+1))
    s[s < 0] = -1.0
    s[s > 0] = 2.0
    x = np.diff(s)

    # Well, it looks very similar to a binary 1d signal! Great! We can use the
    # same A measurement matrix!
    A = np.random.randn(n, N)
    A /= np.sqrt(np.sum(A**2, axis=0))

    # Pick where to make measurements
    y = np.dot(A, x)

    # Reconstruct using IHT
    x_iht = IHT(A, y, k=k, x=x, disp=True, maxiter=200)

    # We fail sometimes if we don't get a random matrix that satisfies RIP
    if not np.allclose(x_iht, x):
        logging.warning('x_iht might not be a good approximation to x!')

    # Look at it!
    plt.plot(x, label='True x[n]')
    plt.plot(x_iht, '--', label='Recon x_iht[n]')
    plt.xlabel('time index, n')
    plt.title('MSE: %g' % compare_mse(x, x_iht))
    plt.legend()
    plt.show()
