'''Methods for orderings for signals.

Methods return flattened indices.
Hopefully these orderings make the signals more sparse in some domain.
'''

from math import factorial
from itertools import permutations
import logging

import numpy as np
from tqdm import tqdm
from pywt import threshold

from mr_utils.utils import find_nearest

def get_gini_sort(vals):
    '''Sort groups so that we get largest possible coefficients.'''

    M = int(vals.size/2)
    tmp = np.argsort(vals)
    idx = np.zeros(vals.size, dtype=int)
    idx[::2] = tmp[:M]
    idx[1::2] = tmp[M:][::-1]
    return idx

def get_gini_sort2(vals):
    '''Sort groups to get highest possible single coefficient.

    Notes
    -----
    Get the largest coefficient we can and then minimize the others.
    '''

    tmp = np.argsort(vals)
    idx = np.zeros(vals.size, dtype=int)
    idx[0] = tmp[0]
    idx[1] = tmp[-1]
    idx[2:] = tmp[1:-1][::-1]
    return idx


def col_stacked_order(x):
    '''Find ordering of monotonically varying flattened array, x.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.

    Notes
    =====
    Note that you might want to provide abs(x) if x is a complex array.
    '''
    idx = np.argsort(x.flatten())
    return idx

def colwise(x):
    '''Find ordering of monotonically varying columns.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.
    '''
    indicies = np.arange(x.size).reshape(x.shape)
    idx = np.argsort(x, axis=0)
    for ii in range(x.shape[1]):
        indicies[:, ii] = indicies[:, ii][idx[:, ii]]
    return indicies.flatten()

def rowwise(x):
    '''Find ordering of monotonically varying rows.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.
    '''
    indicies = np.arange(x.size).reshape(x.shape)
    idx = np.argsort(x, axis=1)
    for ii in range(x.shape[0]):
        indicies[ii, :] = indicies[ii, :][idx[ii, :]]
    return indicies.flatten()

def inverse_permutation(ordering):
    '''Given some permutation, find the inverse permutation.

    Parameters
    ==========
    ordering : array_like
        Flattened indicies, such as output of np.argsort.

    Returns
    =======
    inverse_ordering
        Inverse permutation.
    '''
    inverse_ordering = [0]*len(ordering)
    for send_from, send_to in enumerate(ordering):
        inverse_ordering[send_to] = send_from
    return inverse_ordering


def brute_force1d(x, T):
    '''Given transform matrix, T, sort 1d signal exhaustively.

    Parameters
    ==========
    x : array_like
        1D signal to find ordering of.
    T : array_like
        Transform matrix.

    Returns
    =======
    array_like
        Flattened indices giving sorted order.

    .. warning::
        This IS NOT A GOOD IDEA.
    '''

    idx = range(x.size)
    winner_metric = np.linalg.norm(T.dot(x), ord=1)
    for p in tqdm(permutations(idx), total=factorial(x.size)):
        metric = np.linalg.norm(T.dot(x[np.array(p)]), ord=1)
        if metric < winner_metric:
            winner = np.array(p)
            winner_metric = metric
            tqdm.write('New winner: %g' % winner_metric)

    return winner


def random_search(x, T, k, compare='l1', compare_opts=None, disp=False):
    '''Given transform T, find the best of k permutations.

    Parameters
    ==========
    x : array_like
        Array to find the ordering of.
    T : array_like or callable
        Transform matrix/function that we want x to be sparse under.
    k : int
        Number of permutations to try (randomly selected).
    compare : {'nonzero', 'l1'} or callable, optional
        How to compare two permutations.
    compare_opts : dict, optional
        Arguments to pass to compare function.
    disp : bool, optional
        Verbose mode.

    Returns
    =======
    array_like
        Flattened indices giving sorted order.

    Raises
    ======
    NotImplementedError
        If compare is not valid option or callable.
    '''

    # Make sure we only look for what we can get
    max_perms = factorial(x.size)
    if k > max_perms:
        k = max_perms
        logging.warning('%s permutations does not exist! Clipping to %g.',
                        str(k), max_perms)

    # Make sure we can handle both transform matrices and transform functions
    if isinstance(T, np.ndarray):
        T0 = lambda x0: T.dot(x0)
    else:
        T0 = T

    # Make sure we know how to compare
    if compare == 'nonzero':
        def compare0(T0, x0, p0, opts=compare_opts):
            '''Comparison metric.'''

            # Set threshold
            if opts and 'thresh' in opts:
                thresh = opts['thresh']
            else:
                thresh = 1e-8

            return np.sum(np.abs(T0(x0[np.unravel_index(
                p0, x0.shape)].reshape(x0.shape))) > thresh, axis=(0, 1))
    elif compare == 'l1':
        def compare0(T0, x0, p0):
            '''Make a comparison metric.'''
            # return np.sum(x[np.unravel_index(p0, x.shape)] > 1e-8)
            return np.linalg.norm(
                T0(x[np.unravel_index(p0, x0.shape)].reshape(x0.shape)), ord=1)
    elif callable(compare):
        compare0 = compare
    else:
        raise NotImplementedError()

    # Find k permutations and choose the best one
    idx = range(x.size)
    winner = list(idx)
    winner_metric = compare0(T0, x, winner)
    ps = set()
    len_ps = 0
    with tqdm(desc='Ordering', total=k, leave=False) as pbar:
        while len_ps < k:
            p = np.random.permutation(idx)
            ps.add(p.tostring())
            metric = compare0(T0, x, p)
            # pbar.write('%g %g' % (winner_metric, metric))
            if metric < winner_metric:
                winner = p
                winner_metric = metric

                if disp:
                    pbar.write('New winner: %g' % winner_metric)

            len_ps = len(ps)
            pbar.update(len_ps - pbar.n)

    return winner

def gen_sort1d(x, T):
    '''Given 1D transform T, sort 1d signal, x.

    Parameters
    ==========
    x : array_like
        1D signal to find ordering of.
    T : array_like
        Transform matrix.

    Returns
    =======
    array_like
        Flattened indices giving sorted order.
    '''

    M, N = T.shape[:]
    assert x.size == N, 'T, x must be conformal!'

    # Get a list of all columns
    cols = list(range(N))

    f = np.zeros(T.shape, dtype=x.dtype)
    indices = np.tile(np.arange(x.size)[:, None], (1, N))

    # Order x to approximate a single column of T
    for col in cols:
        xk = x.copy()
        for row in range(M):
            ind, f[row, col] = find_nearest(xk, T[row, col])
            indices[row, col] = ind
            xk[ind] = np.inf

    min_err = np.abs((f - T)**2).mean(axis=0).argsort()

    return indices[:, min_err[0]]

def bulk_up(x, T, Ti, k):
    '''Given existing nonzero coefficients, try to make large ones larger.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.
    T : callable
        Transform function.
    Ti : callable
        Inverse transform function.
    k : float
        Percent of coefficients to shoot for.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.

    Notes
    =====
    Uses random_match(), should probably use min linear assignment.
    '''

    # Keep the largest coefficients
    t = T(x)
    idx = np.argsort(-np.abs(t.flatten()))[int(k*t.size)]
    t0 = np.abs(t[np.unravel_index(idx, t.shape)])
    t = threshold(t, value=t0, mode='hard')

    # Now reorder with the intent to match the thresholded image
    target = Ti(t)
    idx = random_match(x, target)
    return idx

def whittle_down(x, T, Ti, k):
    '''Given existing nonzero coefficients, try to remove lower ones.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.
    T : callable
        Transform function.
    Ti : callable
        Inverse transform function.
    k : float
        Percent of coefficients to shoot for.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.

    Notes
    =====
    Uses random_match(), should probably use min linear assignment.
    '''

    t = T(x)
    idx = np.argsort(np.abs(t.flatten()))[int(k*t.size)]
    t0 = 1/np.abs(t[np.unravel_index(idx, t.shape)])
    ti = np.divide(1, t, out=np.zeros_like(t), where=t != 0)
    ti = threshold(ti, value=t0, mode='hard')
    t = np.divide(1, ti, out=np.zeros_like(ti), where=ti != 0)

    target = x - Ti(t)
    idx = random_match(x, target)
    return idx

def random_match(x, T, return_sorted=False):
    '''Match x to T as closely as possible pixel by pixel.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.
    T : array_like
        Target matrix.
    return_sorted : bool, optional
        Whether or not to return the sorted matrix.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.
    array_like, optional
        Sorted array.
    '''

    # Pick a random pixel and place in recon
    idx = np.zeros(T.size, dtype=int)
    recon = np.zeros(T.size, dtype=x.dtype)
    T0 = T.flatten().astype(x.dtype)
    x0 = x.flatten()
    for px in tqdm(np.random.permutation(np.arange(T.size)), desc='Matching',
                   leave=False):
        ii = np.nanargmin(np.abs(T0 - x0[px]))
        T0[ii] = np.nan
        recon[ii] = x0[px]
        idx[ii] = px
    if return_sorted:
        return(idx, recon.reshape(T.shape))
    return idx


def random_match_by_col(x, T, return_sorted=False):
    '''Given matrix T, choose reordering of x that matches it col by col.

    Parameters
    ==========
    x : array_like
        Array to find ordering of.
    T : array_like
        Target matrix.
    return_sorted : bool, optional
        Whether or not to return the sorted matrix.

    Returns
    =======
    idx : array_like
        Flattened indices giving sorted order.
    array_like, optional
        Sorted array.
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
    with tqdm(desc='Matching', total=M, leave=False) as pbar:
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
            min_err = np.abs((f - T)**2).mean(axis=0).argsort().tolist()
            min_err = [me for me in min_err if me in fijs]
            fijs.remove(min_err[0])

            # Check the stopping condition
            if not fijs:
                done = True
            pbar.update(1)

    # If we asked for the sorted matrix, send it back, too
    if return_sorted:
        return(indices.flatten(), f)
    return indices.flatten()

if __name__ == '__main__':
    pass
