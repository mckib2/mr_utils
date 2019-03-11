'''Gradient descent algorithm for Fourier encoding model and TV constraint.'''

import logging

import numpy as np

from mr_utils.utils import dTV

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def GD_FE_TV(
        kspace,
        samp,
        alpha=.5,
        lam=.01,
        do_reordering=False,
        im_true=None,
        ignore_residual=False,
        disp=False,
        maxiter=200):
    r'''Gradient descent for Fourier encoding model and TV constraint.

    Parameters
    ==========
    kspace : array_like
        Measured image.
    samp : array_like
        Sampling mask.
    alpha : float, optional
        Step size.
    lam : float, optional
        TV constraint weight.
    do_reordering : bool, optional
        Whether or not to reorder for sparsity constraint.
    im_true : array_like, optional
        The true image we are trying to reconstruct.
    ignore_residual : bool, optional
        Whether or not to break out of loop if resid increases.
    disp : bool, optional
        Whether or not to display iteration info.
    maxiter : int, optional
        Maximum number of iterations.

    Returns
    =======
    m_hat : array_like
        Estimate of im_true.

    Notes
    =====
    Solves the problem:

    .. math::

        \min_x || d - \text{FT}(I \odot S) ||^2_2  + \lambda \text{TV}(I)

    where d is measured k-space, I is the image estimate, S is the
    undersampling mask, and TV is the total variation operator.

    If `im_true=None`, then MSE will not be calculated.
    '''

    # Make sure compare_mse is defined
    if im_true is None:
        compare_mse = lambda x, y: 0
        logging.info('No true x provided, MSE will not be calculated.')
    else:
        from skimage.measure import compare_mse
        im_true = np.abs(im_true)

        # Get the reordering indicies ready
        if do_reordering:
            from mr_utils.utils.sort2d import sort2d
            from mr_utils.utils.orderings import inverse_permutation
            _, reordering = sort2d(im_true)
            inverse_reordering = inverse_permutation(reordering)

    # Get some display stuff happening
    if disp:
        from mr_utils.utils.printtable import Table
        table = Table(
            ['iter', 'norm', 'MSE'],
            [len(repr(maxiter)), 8, 8],
            ['d', 'e', 'e'])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    # Initialize
    m_hat = np.zeros(kspace.shape, dtype=kspace.dtype)
    r = -kspace.copy()
    prev_stop_criteria = np.inf
    norm_kspace = np.linalg.norm(kspace)

    # Do the thing
    for ii in range(int(maxiter)):

        # Fidelity term
        fidelity = np.fft.ifft2(r)

        # Let's reorder if we said that was going to be a thing
        if do_reordering:
            m_hat = m_hat.flatten()[reordering].reshape(im_true.shape)

        # Sparsity term
        second_term = dTV(m_hat)

        if do_reordering:
            m_hat = m_hat.flatten()[inverse_reordering].reshape(im_true.shape)
            second_term = second_term \
                .flatten()[inverse_reordering].reshape(im_true.shape)

        # Compute stop criteria
        stop_criteria = np.linalg.norm(r)/norm_kspace
        if not ignore_residual and stop_criteria > prev_stop_criteria:
            logging.warning('Breaking out of loop after %d iterations. \
                Norm of residual increased!', ii)
            break
        prev_stop_criteria = stop_criteria

        # Take the step
        m_hat -= alpha*(fidelity + lam*second_term)

        # Tell the user what happened
        if disp:
            logging.info(
                table.row(
                    [ii, stop_criteria, compare_mse(np.abs(m_hat), im_true)]))

        # Compute residual
        r = np.fft.fft2(m_hat)*samp - kspace


    return m_hat
