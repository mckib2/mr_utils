import numpy as np
from skimage.measure import compare_mse
import matplotlib.pyplot as plt
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def IHT(A,y,k,maxiter=500,tol=1e-8,x=None,disp=False):
    '''Iterative hard thresholding algorithm (IHT).

    A -- Measurement matrix.
    y -- Measurements (i.e., y = Ax).
    k -- Number of expected nonzero coefficients.
    maxiter -- Maximum number of iterations.
    tol -- Stopping criteria.
    x -- True signal we are trying to estimate.
    disp -- Whether or not to display iterations.

    If disp=True, then MSE will be calculated using provided x.
    '''

    # length of measurement vector and original signal
    n,N = A.shape[:]

    # Make sure we have everything we need for disp
    if disp and x is None:
        logging.warning('No true x provided, using x=0 for MSE calc.')
        x = np.zeros(N)

    # Some fancy, asthetic touches...
    if disp:
        range_fun = range
    else:
        from tqdm import trange
        range_fun = lambda x: trange(x,leave=False,desc='IHT')

    # Initial estimate of x, x_hat
    x_hat = np.zeros(N)

    # Gte initial residue
    r = y.copy()

    # Set up header for logger
    if disp:
        logging.info('iter\tMSE')
        logging.info('#'*40)

    # Run until tol reached or maxiter reached
    for tt in range_fun(maxiter):
        # Pre-threshold value
        x_hat += np.dot(A.T,r)

        # Find the k'th largest coefficient of gamma, use it as threshold
        thresh = -np.sort(-np.abs(x_hat))[k-1]

        # Estimate the signal (by hard thresholding)
        x_hat[np.abs(x_hat) < thresh] = 0

        # Show MSE at current iteration if we wanted it
        if disp:
            logging.info('%d \t%g' % (tt,compare_mse(x,x_hat)))

        # update the residual
        r = y - np.dot(A,x_hat)

        # Stopping criteria
        if np.linalg.norm(r)/np.linalg.norm(y) < tol:
            break

    if tt == (maxiter-1):
        logging.warning('Hit maximum iteration count, estimate may not be accurate!')
    else:
        if disp:
            logging.info('Final || r || . || y ||^-1 : %g' % (np.linalg.norm(r)/np.linalg.norm(y)))

    return(x_hat)

if __name__ == '__main__':
    pass
