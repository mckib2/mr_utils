'''Search all coefficient combinations and use basinhopping at each step.

Exhaustively search each possible class of k-sparse signals.  For each class,
solve for coefficient values that minimize the histogram error using a global
optimization technique.  In this case, we choose the basinhopping algorithm.

I also introduce the notion that we might not expect the coefficient locations
to be in the high frequency locations -- since the sorted signal removes high
frequencies.  So we can restrict the effective search space from n choose k to
something like n/r choose k, where r is a reduction factor (r > 1).
'''

import numpy as np
from scipy.fftpack import dct, idct

from mr_utils.cs import ordinator1d

def forward(x):
    '''Forward transform.'''
    return dct(x, norm='ortho')

def inverse(c):
    '''Inverse transform.'''
    return idct(c, norm='ortho')

if __name__ == '__main__':

    # Assume there is a k-sparse representation,
    N = 30
    k = 2
    Neff = int(N) # Search a reduced space
    chunksize = 10
    cx = np.zeros(N)
    idx_true = np.random.choice(np.arange(N), k, False)
    cx[idx_true] = np.random.normal(1, 1, k)
    xpi = inverse(cx)

    # We measure a permutation of x
    pi_true = np.random.permutation(np.arange(N))
    x = xpi[pi_true]

    pi = ordinator1d(x, k, inverse, chunksize=10, pdf=None, pdf_metric=None,
                     forward=forward, disp=True)
