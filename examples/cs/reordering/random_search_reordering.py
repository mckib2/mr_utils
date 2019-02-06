'''Example demonstrating how difficult it is to find an effective reordering.

We use a wavelet transformation and try k different random permutations.
'''

import matplotlib.pyplot as plt
import numpy as np

from mr_utils.utils.orderings import random_search
from mr_utils.utils.wavelet import cdf97_2d_forward
from mr_utils.test_data.phantom import binary_smiley

def T(x0):
    '''Wavelet transform.'''
    return cdf97_2d_forward(x0, level=5)[0]
    # return np.diff(x0)
    # return hadamard(N).dot(x0)

if __name__ == '__main__':

    N = 512
    x = binary_smiley(N)

    # We can try two ways:
    # (1) Try to reduce l1 of T(x)
    idx = random_search(x, T, k=500, compare='l1', disp=True)

    T0 = T(x).flatten()
    T1 = T(x[np.unravel_index(idx, x.shape)].reshape(x.shape)).flatten()

    # Look at the sorted coefficients
    plt.plot(-np.sort(-np.abs(T0)))
    plt.plot(-np.sort(-np.abs(T1)), '--')
    plt.show()

    # (2) Try to reduce number of nonzero coefficients
    idx = random_search(x, T, k=500, compare='nonzero',
                        compare_opts={'thresh': 1e-4}, disp=True)

    T0 = T(x).flatten()
    T1 = T(x[np.unravel_index(idx, x.shape)].reshape(x.shape)).flatten()

    # Look at the sorted coefficients
    plt.plot(-np.sort(-np.abs(T0)))
    plt.plot(-np.sort(-np.abs(T1)), '--')
    plt.show()
