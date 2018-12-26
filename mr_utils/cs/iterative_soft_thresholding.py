import numpy as np
from skimage.measure import compare_mse
import matplotlib.pyplot as plt
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def table_hdr(tt,stop_criteria,theta,err):
    hdr = ''.join(['{:8s}  '.format(tt),'{:12s}  '.format(stop_criteria),'{:12s}  '.format(theta),'{:12s}'.format(err)])
    return(hdr)

def table_line(tt,stop_criteria,theta,err):
    return(''.join(['{:8d}  '.format(tt),'{:8e}  '.format(stop_criteria),'{:8e}  '.format(theta),'{:8e}'.format(err)]))

def IST(A,y,mu=0.8,theta0=None,k=None,maxiter=500,tol=1e-8,x=None,disp=False):
    '''Iterative soft thresholding algorithm (IST).

    A -- Measurement matrix.
    y -- Measurements (i.e., y = Ax).
    mu -- Step size (theta contraction factor, 0 < mu <= 1).
    theta0 -- Initial threshold, decreased by factor of mu each iteration.
    k -- Number of expected nonzero coefficients.
    maxiter -- Maximum number of iterations.
    tol -- Stopping criteria.
    x -- True signal we are trying to estimate.
    disp -- Whether or not to display iterations.

    Solves the problem:
        min_x || y - Ax ||^2_2  s.t.  ||x||_0 <= k

    If disp=True, then MSE will be calculated using provided x. If theta0=None,
    the initial threshold of the IHT will be used as the starting theta.

    TODO: add full citation here
    Implements Equations [22-23] from:
        "A Systematic Review of Compressive Sensing: Concepts, Implementations
        and Applications"
    '''

    # Check to make sure we have good mu
    assert 0 < mu <= 1,'mu should be 0 < mu <= 1!'

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
        range_fun = lambda x: trange(x,leave=False,desc='IST')

    # Initial estimate of x, x_hat
    x_hat = np.zeros(N)

    # Get initial residue
    r = y.copy()

    # Start theta at specified theta0 or use IHT first threshold
    if theta0 is None:
        assert k is not None,'k (measure of sparsity) required to compute initial threshold!'
        theta = -np.sort(-np.abs(np.dot(A.T,r)))[k-1]
    else:
        assert theta0 > 0,'Threshold must be positive!'
        theta = theta0

    # Set up header for logger
    if disp:
        # logging.info('iter \tnorm \ttheta \tMSE')
        hdr = table_hdr('iter','norm','theta','MSE')
        logging.info(hdr)
        logging.info('#'*len(hdr))

    # Run until tol reached or maxiter reached
    for tt in range_fun(maxiter):
        # Update estimate using residual scaled by step size
        x_hat += np.dot(A.T,r)

        # Just like IHT, but use soft thresholding operator
        # It is unclear to me what sign function needs to be used: count 0 as 0?
        x_hat = np.maximum(np.abs(x_hat) - theta,np.zeros(x_hat.shape))*np.sign(x_hat)

        # update the residual
        r = y - np.dot(A,x_hat)

        # Check stopping criteria
        stop_criteria = np.linalg.norm(r)/np.linalg.norm(y)
        if stop_criteria < tol:
            break

        # Show MSE at current iteration if we wanted it
        if disp:
            logging.info(table_line(tt,stop_criteria,theta,compare_mse(x,x_hat)))

        # Contract theta before we go back around the horn
        theta *= mu

    # Regroup and debrief...
    if tt == (maxiter-1):
        logging.warning('Hit maximum iteration count, estimate may not be accurate!')
    else:
        if disp:
            logging.info('Final || r || . || y ||^-1 : %g' % (np.linalg.norm(r)/np.linalg.norm(y)))

    return(x_hat)

if __name__ == '__main__':
    pass
