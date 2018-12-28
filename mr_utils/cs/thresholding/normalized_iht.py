import numpy as np
from skimage.measure import compare_mse
import logging
from mr_utils.utils.printtable import Table

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def nIHT(A,y,k,c=0.1,kappa=None,x=None,maxiter=200,tol=1e-8,disp=False):
    '''Normalized iterative hard thresholding.

    A -- Measurement matrix
    y -- Measurements (i.e., y = Ax)
    k -- Number of nonzero coefficients preserved after thresholding.
    c -- Small, fixed constant. Tunable.
    kappa -- Constant, > 1/(1 - c).
    x -- True signal we want to estimate.
    maxiter -- Maximum number of iterations (of the outer loop).
    tol -- Stopping criteria.
    dip -- Whether or not to display iteration info.

    Implements Algorithm 8.6 from:
        Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
        and applications. Cambridge University Press, 2012.
    '''

    # Basic checks
    assert 0 < c < 1, 'c must be in (0,1)'

    # length of measurement vector and original signal
    n,N = A.shape[:]

    # Make sure we have everything we need for disp
    if disp and x is None:
        logging.warning('No true x provided, using x=0 for MSE calc.')
        x = np.zeros(N)

    if disp:
        table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    # Initializations
    x_hat = np.zeros(N)

    # Inital calculation of support
    val = A.T.dot(y)
    thresh = -np.sort(-np.abs(val))[k-1]
    val[np.abs(val) < thresh] = 0
    T = np.nonzero(val)

    # Find suitable kappa if the user didn't give us one
    if kappa is None:
        # kappa must be > 1/(1 - c), so try 2 times the lower bound
        kappa = 2/(1 - c)
    else:
        assert kappa > 1/(1 - c),'kappa must be > 1/(1 - c)'

    # Do the iterative part of the thresholding...
    for ii in range(maxiter):

        # Compute residual
        r = y - np.dot(A,x_hat)

        # Check stopping criteria
        stop_criteria = np.linalg.norm(r)/np.linalg.norm(y)
        if stop_criteria < tol:
            break

        # Let's check out what's going on
        if disp:
            logging.info(table.row([ ii,stop_criteria,compare_mse(x,x_hat) ]))

        # Compute step size
        g = np.dot(A.T,r)
        mu = np.linalg.norm(g)**2/np.linalg.norm(np.dot(A,g))**2

        # Hard thresholding
        xn = x_hat + mu*g
        xn[np.argsort(np.abs(xn))[:-k]] = 0

        # Compute support of xn
        Tn = np.nonzero(xn)

        # Decide what to do
        if np.array_equal(Tn,T):
            x_hat = xn
        else:
            cond = (1 - c)*np.linalg.norm(xn - x_hat)**2/np.linalg.norm(np.dot(A,xn - x_hat))**2
            if mu <= cond:
                x_hat = xn
            else:
                while mu > cond:
                    mu /= kappa*(1 - c)
                    xn = x_hat + mu*g
                    thresh = -np.sort(-np.abs(xn))[k-1]
                    xn[np.abs(xn) < thresh] = 0
                    cond = (1 - c)*np.linalg.norm(xn - x_hat)**2/np.linalg.norm(np.dot(A,xn - x_hat))**2

                Tn = np.nonzero(xn)
                x_hat = xn

    return(x_hat)

if __name__ == '__main__':
    pass
