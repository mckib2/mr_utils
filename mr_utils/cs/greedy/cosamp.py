'''Compressive sampling matching pursuit (CoSaMP) algorithm.

This implementation currently does not handle complex signals.
'''

import logging

import numpy as np

from mr_utils.utils.printtable import Table

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def cosamp(
        A,
        y,
        k,
        lstsq='exact',
        tol=1e-8,
        maxiter=500,
        x=None,
        disp=False):
    '''Compressive sampling matching pursuit (CoSaMP) algorithm.

    A -- Measurement matrix.
    y -- Measurements (i.e., y = Ax).
    k -- Number of expected nonzero coefficients.
    lstsq -- How to solve intermediate least squares problem.
    tol -- Stopping criteria.
    maxiter -- Maximum number of iterations.
    x -- True signal we are trying to estimate.
    disp -- Whether or not to display iterations.

    lstsq function:
        lstsq = { 'exact', 'lm', 'gd' }.

        'exact' solves it using numpy's linalg.lstsq method.
        'lm' uses solves with the Levenberg-Marquardt algorithm.
        'gd' uses 3 iterations of a gradient descent solver.

    Implements Algorithm 8.7 from:
        Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
        and applications. Cambridge University Press, 2012.
    '''

    # length of measurement vector and original signal
    _n, N = A.shape[:]

    # Initializations
    x_hat = np.zeros(N, dtype=y.dtype)
    r = y.copy()
    ynorm = np.linalg.norm(y)

    if x is None:
        x = np.zeros(x_hat.shape, dtype=y.dtype)
    elif x.size < x_hat.size:
        x = np.hstack(([0], x))

    # Decide how we want to solve the intermediate least squares problem
    if lstsq == 'exact':
        lstsq_fun = lambda A0, y: np.linalg.lstsq(A0, y, rcond=None)[0]
    elif lstsq == 'lm':
        # # This also doesn't work very well currently....
        # from scipy.optimize import least_squares
        # lstsq_fun = lambda A0, y: least_squares(
        #     lambda x: np.linalg.norm(y - np.dot(A0, x)),
        #     np.zeros(A0.shape[1], dtype=y.dtype))['x']
        raise NotImplementedError()
    elif lstsq == 'gd':
        # # This doesn't work very well...
        # from mr_utils.optimization import gd, fd_complex_step
        # lstsq_fun = lambda A0, y: gd(
        #     lambda x: np.linalg.norm(y - np.dot(A0, x)),
        #     fd_complex_step,
        #     np.zeros(A0.shape[1], dtype=y.dtype), maxiter=3)[0]
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    # Start up a table
    if disp:
        table = Table(
            ['iter', 'norm', 'MSE'],
            [len(repr(maxiter)), 8, 8],
            ['d', 'e', 'e'])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    for ii in range(maxiter):

        # Get step direction
        g = np.dot(A.conj().T, r)

        # Add 2*k largest elements of g to support set
        Tn = np.union1d(x_hat.nonzero()[0], np.argsort(np.abs(g))[-(2*k):])

        # Solve the least squares problem
        xn = np.zeros(N, dtype=y.dtype)
        xn[Tn] = lstsq_fun(A[:, Tn], y)

        xn[np.argsort(np.abs(xn))[:-k]] = 0
        x_hat = xn.copy()

        # Compute new residual
        r = y - np.dot(A, x_hat)

        # Compute stopping criteria
        stop_criteria = np.linalg.norm(r)/ynorm

        # Show MSE at current iteration if we wanted it
        if disp:
            logging.info(
                table.row(
                    [ii, stop_criteria, np.mean((np.abs(x - x_hat)**2))]))

        # Check stopping criteria
        if stop_criteria < tol:
            break

    return x_hat
