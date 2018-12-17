import numpy as np
from tqdm import tqdm,trange
import warnings
from scipy.optimize import line_search
from scipy.optimize.linesearch import LineSearchWarning

def gd(f,grad,x0,alpha=None,iter=1e6,tol=1e-8):
    '''Gradient descent algorithm.

    f -- Function to be optimized.
    grad -- Function that computes the gradient of f.
    x0 -- Initial point to start to start descent.
    alpha -- Either a fixed step size or a function that returns step size.
    iter -- Do not exceed this number of iterations.
    tol -- Run until change in step size within this number.
    '''

    if type(x0) is not np.ndarray:
        x0 = np.atleast_1d(x0).astype(float)

    # Use scipy.optimize.line_search by default
    if alpha is None:
        alpha = line_search

    # If stepsize is constant, package it in a constant function
    if not callable(alpha):
        alpha0 = alpha
        def alpha(*args,**kwargs):
            return(alpha0,0,0,None,None,None)

    # Set up everything we need for the loop
    cur_x = x0.copy()
    previous_step_size = np.inf
    f_prev = None
    f_prev_prev = None
    alpha0_default = 0.5
    alpha0_backup = alpha0_default

    # Do the thing!
    pbar = tqdm(total=100,desc='GD',leave=False)
    for ii in range(int(iter)):

        prev_x = cur_x.copy()

        # Compute the search direction
        g0 = grad(f,prev_x)
        s0 = -g0

        # Get step size
        # Sometimes line_search doesn't converge - silently ignore this
        with warnings.catch_warnings():
            warnings.filterwarnings('error',category=LineSearchWarning)
            try:
                alpha0,fc,gc,f_prev,f_prev_prev,derphi_star = alpha(f,lambda x: grad(f,x),prev_x,s0,g0,f_prev,f_prev_prev)
                alpha0_backup = alpha0_default
            except LineSearchWarning:
                alpha0 = alpha0_backup
                alpha0_backup /= 2

        # Take the step
        cur_x += alpha0*s0

        # Figure out if we can end
        previous_step_size = np.abs(cur_x - prev_x)
        pbar.n = 0
        val = np.clip(np.round(100*tol/np.max(previous_step_size + np.finfo(float).eps)),0,100)
        pbar.update(val)

        if np.all(previous_step_size < tol):
            break

    if np.any(previous_step_size > tol):
        warnings.warn('GD hit maxiters! Change in step size is not < %g' % tol)

    # return the solution
    return(cur_x,ii+1)

if __name__ == '__main__':
    pass
