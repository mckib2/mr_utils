import numpy as np
from mr_utils.utils import dTV
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def GD_TV(y,forward_fun,inverse_fun,alpha=.5,lam=.01,do_reordering=False,x=None,ignore_residual=False,disp=False,maxiter=200):
    '''Gradient descent for a generic encoding model and TV constraint.

    y -- Measured data (i.e., y = Ax).
    forward_fun -- A, the forward transformation function.
    inverse_fun -- A^H, the inverse transformation function.
    alpha -- Step size.
    lam -- TV constraint weight.
    do_reordering -- Whether or not to reorder for sparsity constraint.
    x -- The true image we are trying to reconstruct.
    ignore_residual -- Whether or not to break out of loop if resid increases.
    disp -- Whether or not to display iteration info.
    maxiter -- Maximum number of iterations.

    Solves the problem:
        min_x || y - Ax ||^2_2  + lam*TV(x)

    If x=None, then MSE will not be calculated.
    '''

    # Make sure compare_mse is defined
    if x is None:
        compare_mse = lambda xx,yy: 0
        logging.info('No true x provided, MSE will not be calculated.')
    else:
        from skimage.measure import compare_mse
        x = np.abs(x)

        # Get the reordering indicies ready
        if do_reordering:
            from mr_utils.utils.sort2d import sort2d
            from mr_utils.utils.orderings import inverse_permutation
            _,reordering = sort2d(x)
            inverse_reordering = inverse_permutation(reordering)

    # Get some display stuff happening
    if disp:
        from mr_utils.utils.printtable import Table
        table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    # Initialize
    x_hat = np.zeros(y.shape,dtype=y.dtype)
    r = -y.copy()
    prev_stop_criteria = np.inf
    norm_y = np.linalg.norm(y)

    # Do the thing
    for ii in range(int(maxiter)):

        # Fidelity term
        fidelity = inverse_fun(r)

        # Let's reorder if we said that was going to be a thing
        if do_reordering:
            x_hat = x_hat.flatten()[reordering].reshape(x.shape)

        # Sparsity term
        second_term = dTV(x_hat)

        # Put the pixels back where they belong
        if do_reordering:
            x_hat = x_hat.flatten()[inverse_reordering].reshape(x.shape)
            second_term = second_term.flatten()[inverse_reordering].reshape(x.shape)

        # Compute stop criteria
        stop_criteria = np.linalg.norm(r)/norm_y
        if not ignore_residual and stop_criteria > prev_stop_criteria:
            logging.warning('Breaking out of loop after %d iterations. Norm of residual increased!' % ii)
            break
        prev_stop_criteria = stop_criteria

        # Take the step
        x_hat -= alpha*(fidelity + lam*second_term)

        # Tell the user what happened
        if disp:
            logging.info(table.row([ ii,stop_criteria,compare_mse(np.abs(x_hat),x) ]))

        # Compute residual
        r = forward_fun(x_hat) - y

    return(x_hat)
