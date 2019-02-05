'''Methods for orderings for signals.

Methods return flattened indices.
Hopefully these orderings make the signals more sparse in some domain.
'''

import numpy as np

from mr_utils.utils import find_nearest

def col_stacked_order(x):
    '''Find ordering of monotonically varying flattened array, x.

    x -- Array to find ordering of.

    Note that you might want to provide abs(x) if x is a complex array.
    '''
    idx = np.argsort(x.flatten())
    return idx

def colwise(x):
    '''Find ordering of monotonically varying columns.

    x -- Array to find ordering of.
    '''
    indicies = np.arange(x.size).reshape(x.shape)
    idx = np.argsort(x, axis=0)
    for ii in range(x.shape[1]):
        indicies[:, ii] = indicies[:, ii][idx[:, ii]]
    return indicies.flatten()

def rowwise(x):
    '''Find ordering of monotonically varying rows.

    x -- Array to find ordering of.
    '''
    indicies = np.arange(x.size).reshape(x.shape)
    idx = np.argsort(x, axis=1)
    for ii in range(x.shape[0]):
        indicies[ii, :] = indicies[ii, :][idx[ii, :]]
    return indicies.flatten()

def inverse_permutation(ordering):
    '''Given some permutation, find the inverse permutation.

    ordering -- Flattened indicies, such as output of np.argsort.
    '''
    inverse_ordering = [0]*len(ordering)
    for send_from, send_to in enumerate(ordering):
        inverse_ordering[send_to] = send_from
    return inverse_ordering

def random_boarding(x, T, return_sorted=False):
    '''Given transform matrix T, choose reordering of x that sparsifies.

    x -- Array to find ordering of.
    T -- Transform matrix, columns are basis functions.
    return_sorted -- Whether or not to return the sorted matrix.
    '''

    # Find number of basis functions, fi, and number of samples, M
    M, N = T.shape[:]

    # Keep a list of fij that we haven't done yet
    fijs = list(range(M))

    # Find a good ordering for each basis function
    done = False
    xk = x.copy()
    f = np.zeros(T.shape, dtype=x.dtype)
    indices = np.arange(x.size).reshape(x.shape)
    while not done:

        # Choose a row
        idx = np.random.choice(np.arange(len(fijs)))
        jj = fijs[idx]

        # Choose a column
        for ii in np.random.permutation(list(range(N))):
            ind, f[ii, jj] = find_nearest(xk, T[ii, jj])
            indices[ii, jj] = ind
            xk[np.unravel_index(ind, x.shape)] = np.inf

        # Finalize the best fit, i.e., min || f[:, jj] - X[jj] ||
        min_err = np.abs((f - T)**2).mean(axis=0).argsort()
        for me in min_err:
            try:
                fijs.remove(me)
                break
            except ValueError:
                pass

        # Check the stopping condition
        if not fijs:
            done = True

    # If we asked for the sorted matrix, send it back, too
    if return_sorted:
        return(indices.flatten(), f)
    return indices.flatten()

if __name__ == '__main__':
    pass
