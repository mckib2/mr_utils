'''Compare Gini index to l1, l0.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.utils import gini

def make_signal(n, vals, idx=None):
    '''Make piecewise constant signal.

    Parameters
    ----------
    idx : array_like, optional
        Order of vals (groups).
    '''

    N = np.sum(n) # length of signal
    if idx is None:
        idx = np.arange(N).astype(int)

    x = np.zeros(int(N))
    for ii, _nn in enumerate(n):
        begin = np.sum(n[idx[:ii]])
        end = begin + n[idx[ii]]
        x[begin:end] = vals[idx[ii]]
    return x

if __name__ == '__main__':

    # Create piecewise constant signal
    k = 10 # number of groups
    n = np.random.randint(1, 10, k) # length of groups
    vals = np.random.random(k)
    x = make_signal(n, vals)

    # plt.plot(x)
    # plt.title('Piecewise constant signal')
    # plt.show()

    # # Make sure sorting does what we think it does
    # a = np.sort(x)
    # b = make_signal(n, vals, np.argsort(vals))
    # plt.plot(x)
    # plt.plot(a)
    # plt.plot(b, '--')
    # plt.show()

    print(gini(np.diff(x)))
    print(gini(np.diff(np.sort(x))))
