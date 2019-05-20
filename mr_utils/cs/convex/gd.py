'''General gradient descent framework.'''

import numpy as np
from scipy.optimize import minimize
from tqdm import trange, tqdm

def gd(shape, updates, x0=None, alphas=None, costs=None, maxiter=200,
       tol=1e-8, disp=False):
    '''Gradient descent to solve compressed sensing reconstruction.

    Parameters
    ----------
    shape : tuple
        Shape of output.
    updates : list of callable
        List of gradient functions to be used as updates each step.
    x0 : array_like
        Initial guess.  If x0=None, start at zeros.
    alphas : list of float
        List of weights for each update term.  If None, then alphas
        will be chosen to minimize the cost function at each step.
    cost : list of callable
        The cost function terms corresponding to each update entry.
        Required if alphas=None.
    maxiter : int
        Maximum number of iterations.
    tol : float
        If maximum change in estimate is less than tol, break out of
        loop.
    disp : bool
        Show progress in real-time.  Will be slower.

    Returns
    -------
    x : array_like
        Final image estimate.
    costs : values of the cost function

    Notes
    -----
    Use this function if you know the gradients of the cost terms.
    If note, proximal gradient descent may be used without knowledge
    of gradients.

    For image reconstruction, fixed alpha is probably the way to go.
    '''

    # Initializations
    if x0 is None:
        x = np.zeros(shape)
    else:
        x = x0.copy()
    if alphas is not None:
        alphas0 = alphas
    else:
        alphas0 = np.ones(len(updates))
    cost = np.zeros(maxiter)

    for ii in trange(maxiter, leave=False):

        # Do linesearch if alphas are not specified
        if alphas is None:
            def obj(a0):
                '''Objective to minimize to find good weights.'''
                update = sum([a*u(x) for u, a in zip(updates, a0)])
                xtest = x - update
                return sum([c(xtest) for c in costs])
            a0 = alphas0
            res = minimize(obj, a0)
            alphas0 = res['x']

        # Do update for each update in list
        update = sum([a*u(x) for u, a in zip(updates, alphas0)])
        x -= update

        # Get cost at this iteration
        cost[ii] = sum([a*c(x) for c, a in zip(costs, alphas0)])

        if disp:
            tqdm.write(str(cost[ii]))

        # Break out if update is small enough
        if np.max(np.abs(update)) < tol:
            tqdm.write(('Breaking out of loop after %d iters! '
                        'Tolerance reached!' % (ii+1)))
            cost = cost[:ii+1] # truncate cost
            break

    return(x, cost)
