'''Proximal Gradient Descent.

Flexible encoding model, flexible sparsity model, and flexible
reordering model.  This is the one I would use out of all the ones
I've coded up.  Might be slower than the others as there's a little
more checking to do each iteration.
'''

import logging
import importlib

import numpy as np
from pywt import threshold

# from mr_utils.utils.orderings import inverse_permutation

logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.DEBUG)

def proximal_GD(
        y,
        forward_fun,
        inverse_fun,
        sparsify,
        unsparsify,
        reorder_fun=None,
        mode='soft',
        alpha=.5,
        alpha_start=.5,
        thresh_sep=True,
        selective=None,
        x=None,
        ignore_residual=False,
        ignore_mse=True,
        disp=False,
        maxiter=200):
    r'''Proximal gradient descent for generic encoding/sparsity model.

    Parameters
    ----------
    y : array_like
        Measured data (i.e., y = Ax).
    forward_fun : callable
        A, the forward transformation function.
    inverse_fun : callable
        A^H, the inverse transformation function.
    sparsify : callable
        Sparsifying transform.
    unsparsify : callable
        Inverse sparsifying transform.
    reorder_fun : callable, optional
        Reordering function.
    unreorder_fun : callable, optional
        Inverse reordering function.
    mode : {'soft', 'hard', 'garotte', 'greater', 'less'}, optional
        Thresholding mode.
    alpha : float or callable, optional
        Step size, used for thresholding.
    alpha_start : float, optional
        Initial alpha to start with if alpha is callable.
    thresh_sep : bool, optional
        Whether or not to threshold real/imag individually.
    selective : bool, optional
        Function returning indicies of update to keep at each iter.
    x : array_like, optional
        The true image we are trying to reconstruct.
    ignore_residual : bool, optional
        Whether or not to break out of loop if resid increases.
    ignore_mse : bool, optional
        Whether or not to break out of loop if MSE increases.
    disp : bool, optional
        Whether or not to display iteration info.
    maxiter : int, optional
        Maximum number of iterations.

    Returns
    -------
    x_hat : array_like
        Estimate of x.

    Notes
    -----
    Solves the problem:

    .. math::

        \min_x || y - Ax ||^2_2  + \lambda \text{Sparsify}(x)

    If `x=None`, then MSE will not be calculated. You probably want
    `mode='soft'`.  For the other options, see docs for
    pywt.threshold. `selective=None` will not throw away any updates.
    '''

    # Make sure compare_mse, compare_ssim is defined
    if x is None:
        compare_mse = lambda xx, yy: 0
        logging.info(
            'No true x provided, MSE/SSIM will not be calculated.')
    else:
        from skimage.measure import compare_mse, compare_ssim
        # Precompute absolute value of true image
        xabs = np.abs(x.astype(y.dtype))

    # Get some display stuff happening
    if disp:
        # Don't use tqdm
        range_fun = range

        from mr_utils.utils.printtable import Table
        table = Table(
            ['iter', 'norm', 'MSE', 'SSIM'],
            [len(repr(maxiter)), 8, 8, 8],
            ['d', 'e', 'e', 'e'])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)
    else:
        # Use tqdm to give us an idea of how fast we're going
        from tqdm import trange, tqdm
        range_fun = lambda x: trange(
            x, leave=False, desc='Proximal GD')

    # Initialize
    x_hat = np.zeros(y.shape, dtype=y.dtype)
    r = -y.copy()
    prev_stop_criteria = np.inf
    cur_mse = 0
    prev_mse = compare_mse(xabs, np.abs(inverse_fun(y)))
    norm_y = np.linalg.norm(y)
    if isinstance(alpha, float):
        alpha0 = alpha
    else:
        alpha0 = alpha_start

    # Do the thing
    for ii in range_fun(int(maxiter)):

        # Compute stop criteria
        stop_criteria = np.linalg.norm(r)/norm_y
        if not ignore_residual and stop_criteria > prev_stop_criteria:
            msg = ('Breaking out of loop after %d iterations. '
                   'Norm of residual increased!' % ii)
            if importlib.util.find_spec("tqdm") is None:
                tqdm.write(msg)
            else:
                logging.warning(msg)
            break
        prev_stop_criteria = stop_criteria

        # Compute gradient descent step in prep for reordering
        grad_step = x_hat - inverse_fun(r)

        # Do reordering if we asked for it
        if reorder_fun is not None:
            reorder_idx = reorder_fun(grad_step)
            reorder_idx_r = reorder_idx.real.astype(int)
            reorder_idx_i = reorder_idx.imag.astype(int)

            # unreorder_idx_r = inverse_permutation(reorder_idx_r)
            # unreorder_idx_i = inverse_permutation(reorder_idx_i)
            # unreorder_idx_r = np.arange(
            #     reorder_idx_r.size).astype(int)
            # unreorder_idx_r[reorder_idx_r] = reorder_idx_r
            # unreorder_idx_i = np.arange(
            #     reorder_idx_i.size).astype(int)
            # unreorder_idx_i[reorder_idx_i] = reorder_idx_i

            grad_step = (
                grad_step.real[np.unravel_index(
                    reorder_idx_r, y.shape)] \
                + 1j*grad_step.imag[np.unravel_index(
                    reorder_idx_i, y.shape)]).reshape(y.shape)

        # Take the step, we would normally assign x_hat directly, but
        # because we might be reordering and selectively updating,
        # we'll store it in a temporary variable...
        if thresh_sep:
            tmp = sparsify(grad_step)
            # Take a half step in each real/imag after talk with Ed
            tmp_r = threshold(tmp.real, value=alpha0/2, mode=mode)
            tmp_i = threshold(tmp.imag, value=alpha0/2, mode=mode)
            update = unsparsify(tmp_r + 1j*tmp_i)
        else:
            update = unsparsify(
                threshold(
                    sparsify(grad_step), value=alpha0, mode=mode))

        # Undo the reordering if we did it
        if reorder_fun is not None:
            # update = (
            #     update.real[np.unravel_index(
            #         unreorder_idx_r, y.shape)] \
            #     + 1j*update.imag[np.unravel_index(
            #         unreorder_idx_i, y.shape)]).reshape(y.shape)

            update_r = np.zeros(y.shape)
            update_r[np.unravel_index(
                reorder_idx_r, y.shape)] = update.real.flatten()
            update_i = np.zeros(y.shape)
            update_i[np.unravel_index(
                reorder_idx_i, y.shape)] = update.imag.flatten()
            update = update_r + 1j*update_i

        # Look at where we want to take the step - tread carefully...
        if selective is not None:
            selective_idx = selective(x_hat, update, ii)

        # Update image estimae
        if selective is not None:
            x_hat[selective_idx] = update[selective_idx]
        else:
            x_hat = update

        # Tell the user what happened
        if disp:
            curxabs = np.abs(x_hat)
            cur_mse = compare_mse(curxabs, xabs)
            logging.info(
                table.row(
                    [ii, stop_criteria, cur_mse,
                     compare_ssim(curxabs, xabs)]))
        prev_mse = cur_mse

        if not ignore_mse and cur_mse > prev_mse:
            msg = ('Breaking out of loop after %d iterations. '
                   'MSE increased!' % ii)
            if importlib.util.find_spec("tqdm") is None:
                tqdm.write(msg)
            else:
                logging.warning(msg)
            break

        # Compute residual
        r = forward_fun(x_hat) - y

        # Get next step size
        if callable(alpha):
            alpha0 = alpha(alpha0, ii)

    return x_hat
