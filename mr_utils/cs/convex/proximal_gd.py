'''Proximal Gradient Descent.

Flexible encoding model, flexible sparsity model, and flexible reordering
model.  This is the one I would use out of all the ones I've coded up.
Might be slower than the others as there's a little more checking to do each
iteration.
'''

import logging

import numpy as np
from pywt import threshold

from mr_utils.utils.orderings import inverse_permutation

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def proximal_GD(
        y,
        forward_fun,
        inverse_fun,
        sparsify,
        unsparsify,
        reorder_fun=None,
        mode='soft',
        alpha=.5,
        selective=None,
        x=None,
        ignore_residual=False,
        disp=False,
        maxiter=200):
    '''Proximal gradient descent for a generic encoding, sparsity models.

    y -- Measured data (i.e., y = Ax).
    forward_fun -- A, the forward transformation function.
    inverse_fun -- A^H, the inverse transformation function.
    sparsify -- Sparsifying transform.
    unsparsify -- Inverse sparsifying transform.
    reorder_fun --
    unreorder_fun --
    mode -- Thresholding mode: {'soft','hard','garotte','greater','less'}.
    alpha -- Step size, used for thresholding.
    selective -- Function returning indicies of update to keep at each iter.
    x -- The true image we are trying to reconstruct.
    ignore_residual -- Whether or not to break out of loop if resid increases.
    disp -- Whether or not to display iteration info.
    maxiter -- Maximum number of iterations.

    Solves the problem:
        min_x || y - Ax ||^2_2  + lam*TV(x)

    If x=None, then MSE will not be calculated. You probably want mode='soft'.
    For the other options, see docs for pywt.threshold.  selective=None will
    not throw away any updates.
    '''

    # Make sure compare_mse is defined
    if x is None:
        compare_mse = lambda xx, yy: 0
        logging.info('No true x provided, MSE will not be calculated.')
    else:
        from skimage.measure import compare_mse
        xabs = np.abs(x) # Precompute absolute value of true image

    # Get some display stuff happening
    if disp:
        # Don't use tqdm
        range_fun = range

        from mr_utils.utils.printtable import Table
        table = Table(
            ['iter', 'norm', 'MSE'],
            [len(repr(maxiter)), 8, 8],
            ['d', 'e', 'e'])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)
    else:
        # Use tqdm to give us an idea of how fast we're going
        from tqdm import trange
        range_fun = trange

    # Initialize
    x_hat = np.zeros(y.shape, dtype=y.dtype)
    r = -y.copy()
    prev_stop_criteria = np.inf
    norm_y = np.linalg.norm(y)

    # Do the thing
    for ii in range_fun(int(maxiter)):

        # Compute stop criteria
        stop_criteria = np.linalg.norm(r)/norm_y
        if not ignore_residual and stop_criteria > prev_stop_criteria:
            logging.warning('Breaking out of loop after %d iterations. \
                Norm of residual increased!', ii)
            break
        prev_stop_criteria = stop_criteria

        # Compute gradient descent step in prep for reordering
        grad_step = x_hat - inverse_fun(r)

        # Do reordering if we asked for it
        if reorder_fun is not None:
            reorder_idx = reorder_fun(grad_step)
            reorder_idx_r = reorder_idx.real.astype(int)
            reorder_idx_i = reorder_idx.imag.astype(int)
            unreorder_idx_r = inverse_permutation(reorder_idx_r)
            unreorder_idx_i = inverse_permutation(reorder_idx_i)
            grad_step = (
                grad_step.real[np.unravel_index(reorder_idx_r, y.shape)] \
                +1j*grad_step.imag[np.unravel_index(reorder_idx_i, y.shape)]) \
                .reshape(y.shape)

        # Take the step, we would normally assign x_hat directly, but because
        # we might be reordering and selectively updating, we'll store it in
        # a temporary variable...
        update = unsparsify(
            threshold(sparsify(grad_step), value=alpha, mode=mode))

        # Undo the reordering if we did it
        if reorder_fun is not None:
            update = (
                update.real[np.unravel_index(unreorder_idx_r, y.shape)] \
                + 1j*update.imag[np.unravel_index(unreorder_idx_i, y.shape)]) \
                .reshape(y.shape)

        # Look at where we want to take the step - tread carefully...
        if selective is not None:
            selective_idx = selective(x_hat, update)

        # Update image estimae
        if selective is not None:
            x_hat[selective_idx] = update[selective_idx]
        else:
            x_hat = update

        # Tell the user what happened
        if disp:
            logging.info(
                table.row(
                    [ii, stop_criteria, compare_mse(np.abs(x_hat), xabs)]))

        # Compute residual
        r = forward_fun(x_hat) - y

    return x_hat
