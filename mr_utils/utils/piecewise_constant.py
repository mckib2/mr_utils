'''Construct a sample, random, piecewise constant signal.
'''

import numpy as np

def piecewise(n, vals, idx=None):
    '''Make piecewise constant signal.

    Parameters
    ----------
    n : array_like
        Length of each group/flat-piece.
    vals : array_like
        Values of each group.  Should be same size as n.
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
