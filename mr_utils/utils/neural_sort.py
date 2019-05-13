'''Differentiable sort function.'''

import numpy as np
from scipy.special import softmax
from scipy.spatial.distance import cdist

def neural_sort(s, tau=1):
    '''Continuous relaxation of sorting operator.

    Parameters
    ----------
    s : array_like
        Real valued input vector to be sorted.
    tau : float
        Temperature parameter.

    Returns
    -------


    Notes
    -----
    Implements equation [5] from [1]_.

    References
    ----------
    .. [1] Grover, Aditya, et al. "Stochastic optimization of sorting
           networks via continuous relaxations." arXiv preprint
           arXiv:1903.08850 (2019).
    '''

    N = s.size
    # As = np.zeros((N, N))
    # for ii in range(N):
    #     for jj in range(N):
    #         As[ii, jj] = np.abs(s[ii] - s[jj])
    As = cdist(s[:, None], s[:, None], 'cityblock')

    # This could be optimized using einsum:
    P = np.zeros(As.shape)
    for ii in range(N):
        iii = ii + 1
        val0 = (N + 1 - 2*iii)*s
        val1 = np.dot(As, np.ones((N, 1))).squeeze()
        val = (val0 - val1)/tau
        P[ii, :] = softmax(val)
    return P
