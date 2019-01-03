import numpy as np
import matplotlib.pyplot as plt
import logging
from mr_utils.utils.printtable import Table

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def IHT(A,y,k,mu=1,maxiter=500,tol=1e-8,x=None,disp=False):
    '''Iterative hard thresholding algorithm (IHT).

    A -- Measurement matrix.
    y -- Measurements (i.e., y = Ax).
    k -- Number of expected nonzero coefficients.
    mu -- Step size.
    maxiter -- Maximum number of iterations.
    tol -- Stopping criteria.
    x -- True signal we are trying to estimate.
    disp -- Whether or not to display iterations.

    Solves the problem:
        min_x || y - Ax ||^2_2  s.t.  ||x||_0 <= k

    If disp=True, then MSE will be calculated using provided x. mu=1 seems to
    satisfy Theorem 8.4 often, but might need to be adjusted (usually < 1).
    See normalized IHT for adaptive step size.

    Implements Algorithm 8.5 from:
        Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
        and applications. Cambridge University Press, 2012.
    '''

    # length of measurement vector and original signal
    n,N = A.shape[:]

    # Make sure we have everything we need for disp
    if disp and x is None:
        logging.warning('No true x provided, using x=0 for MSE calc.')
        x = np.zeros(N)

    # Some fancy, asthetic touches...
    if disp:
        table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
        range_fun = range
    else:
        from tqdm import trange
        range_fun = lambda x: trange(x,leave=False,desc='IHT')

    # Initial estimate of x, x_hat
    x_hat = np.zeros(N,dtype=y.dtype)

    # Get initial residue
    r = y.copy()

    # Set up header for logger
    if disp:
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    # Run until tol reached or maxiter reached
    for tt in range_fun(int(maxiter)):
        # Update estimate using residual scaled by step size
        x_hat += mu*np.dot(A.conj().T,r)

        # Leave only k coefficients nonzero (hard threshold)
        x_hat[np.argsort(np.abs(x_hat))[:-k]] = 0

        stop_criteria = np.linalg.norm(r)/np.linalg.norm(y)

        # Show MSE at current iteration if we wanted it
        if disp:
            logging.info(table.row([ tt,stop_criteria,np.mean((np.abs(x - x_hat)**2)) ]))

        # update the residual
        r = y - np.dot(A,x_hat)

        # Check stopping criteria
        if stop_criteria < tol:
            break

    # Regroup and debrief...
    if tt == (maxiter-1):
        logging.warning('Hit maximum iteration count, estimate may not be accurate!')
    else:
        if disp:
            logging.info('Final || r || . || y ||^-1 : %g' % (np.linalg.norm(r)/np.linalg.norm(y)))

    return(x_hat)

if __name__ == '__main__':
    pass
