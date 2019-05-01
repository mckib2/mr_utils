'''Lagrangian relaxation of ordinator.'''

from functools import partial
import os

import numpy as np
from scipy.optimize import minimize
from scipy.optimize import linear_sum_assignment as lsa
from scipy.spatial.distance import cdist

def make_xhat(c0, unsparsify, norm=False):
    '''Construct xhat from coefficients c0.'''
    xhat = unsparsify(c0)
    if norm:
        return xhat/np.max(np.abs(xhat.flatten()))
    return xhat


def obj1(c0, x, lam, norm):
    '''Find the cost between current xhat and x using lsa.

    Notes
    -----
    This bakes the cost of linear sum assignment right into the
    objectve function and adds a regularizing l1 term to encourage
    the solution to be sparse.
    '''
    xhat = make_xhat(c0, norm)
    C = cdist(xhat[:, None], x[:, None])
    row, col = lsa(C)
    return C[row, col].sum() + lam*np.linalg.norm(c0, ord=1)

def obj(c0, x, lam, unsparsify, norm, transform_shape):
    '''Find cost between current xhat and x using sort.

    Notes
    -----
    This is a reduction of the histogram case to a bin-width of 1,
    also adding an l1 term to encourage a sparse solution.

    Might consider using Gini index instead?
    '''
    xhat = make_xhat(c0.reshape(transform_shape), unsparsify, norm)
    return np.linalg.norm(
        np.sort(x.flatten()) - np.sort(
            xhat.flatten())) + lam*np.linalg.norm(c0, ord=1)

def save_intermediate(c, fval, saveit=False, disp=False):
    '''Save the intermediate solutions and print update message.'''

    if saveit:
        np.save('c_intermediate.npy', c)
    if disp:
        print('fval: %g' % fval)

def load_intermediate():
    '''Load any saved intermediate values to do warm start.'''
    if os.path.isfile('c_intermediate.npy'):
        return np.load('c_intermediate.npy')
    return None

def relaxed_ordinator(x, lam, k, unsparsify, norm=False,
                      warm=False, transform_shape=None, disp=False):
    '''Find ordering pi that makes x[pi] sparse.

    Parameters
    ----------
    x : array_like
        Signal to find ordering of.
    lam : float
        Lagrangian weight on l1 term of objective function.
    k : int
        Expected sparsity level (number of nonzero coefficients) of
        ordererd signal, x[pi].
    unsparsify : callable
        Function that computes inverse sparsifying transform.
    norm : bool, optional
        Normalize xhat at each step (probably don't do this.)
    warm : bool
        Whether to look for warm start file and save intermedate
        results.
    transform_shape : int
        Shape of transform coefficients (if different than x.shape).
        None will use x.shape.
    disp : bool
        Display progress messages.

    Returns
    -------
    pi : array_like
        Flattened ordering array (like is returned by numpy.argsort).

    Notes
    -----
    `size_transform` will be x.size - 1 for finite differences
    transform.
    '''

    # If size of coefficients is different than x.shape, make note
    if transform_shape is None:
        transform_shape = x.shape

    # Check to see if we can warm start
    c0 = load_intermediate()
    if not warm or c0 is None:
        c0 = np.ones(transform_shape).flatten()
    else:
        print('WARM START')

    pobj = partial(
        obj, x=x, lam=lam, unsparsify=unsparsify, norm=norm,
        transform_shape=transform_shape)
    res = minimize(pobj, c0, callback=lambda x: save_intermediate(
        x, pobj(x), disp))
    # print(res)

    # Go ahead and hard threshold here
    c_est = res['x']
    c_est[np.abs(c_est) < np.sort(np.abs(c_est))[-k]] = 0

    # plt.plot(res['x'])
    # plt.plot(c_true)
    # plt.show()

    # Do the assignment and try to recover x
    xhat = make_xhat(c_est.reshape(transform_shape), unsparsify, norm)
    C = cdist(xhat.flatten()[:, None], x.flatten()[:, None])
    _row, pi = lsa(C)

    return pi
