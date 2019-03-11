'''2D implementation of Approximate message passing algorithms.

See docstring of amp2d for reference implementation details.  It's companion
is LCAMP.  What's interesting is that they circular shift in the transform
domain.  I'm not sure why they do that, but empirically it seems to work!

The wavelet transform is about what they are using.  I'm trying to keep the
implementation as simple as possible, so I used a built in transform from
PyWavelets that is close, but I'm not sure why it doesn't match up completely.
'''

import logging
from os.path import dirname

import numpy as np
from scipy.io import loadmat

from mr_utils.utils import cdf97_2d_forward, cdf97_2d_inverse

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def amp2d(
        y,
        forward_fun,
        inverse_fun,
        sigmaType=2,
        randshift=False,
        tol=1e-8,
        x=None,
        ignore_residual=False,
        disp=False,
        maxiter=100):
    r'''Approximate message passing using wavelet sparsifying transform.

    Parameters
    ==========
    y : array_like
        Measurements, i.e., y = Ax.
    forward_fun : callable
        A, the forward transformation function.
    inverse_fun : callable
        A^H, the inverse transformation function.
    sigmaType : int
        Method for determining threshold.
    randshift : bool, optional
        Whether or not to randomly circular shift every iteration.
    tol : float, optional
        Stop when stopping criteria meets this threshold.
    x : array_like, optional
        The true image we are trying to reconstruct.
    ignore_residual : bool, optional
        Whether or not to ignore stopping criteria.
    disp : bool, optional
        Whether or not to display iteration info.
    maxiter : int, optional
        Maximum number of iterations.

    Returns
    =======
    wn : array_like
        Estimate of x.

    Notes
    =====
    Solves the problem:

    .. math::

        \min_x || \Psi(x) ||_1 \text{ s.t. } || y -
        \text{forward}(x) ||^2_2 < \epsilon^2

    The CDF-97 wavelet is used.  If `x=None`, then MSE will not be calculated.

    Algorithm described in [1]_, based on MATLAB implementation found at [2]_.

    References
    ==========
    .. [1] "Message Passing Algorithms for CS" Donoho et al., PNAS
           2009;106:18914

    .. [2] http://kyungs.bol.ucla.edu/Site/Software.html
    '''

    # Make sure we have a defined compare_mse and Table for printing
    if disp:
        # Initialize display table
        from mr_utils.utils.printtable import Table
        if disp:
            table = Table(
                ['iter', 'resid', 'resid diff', 'MSE'],
                [len(repr(maxiter)), 8, 8, 8],
                ['d', 'e', 'e', 'e'])
            hdr = table.header()
            for line in hdr.split('\n'):
                logging.info(line)

        if x is not None:
            from skimage.measure import compare_mse
            xabs = np.abs(x)
        else:
            xabs = 0
            compare_mse = lambda xx, yy: 0

    # Do some initial calculations...
    mm = np.sum(abs(y) > np.finfo(float).eps)
    rfact = y.size/mm

    # I'm currently not sure how we found these optimim lambdas...
    OptimumLambdaSigned = loadmat(dirname(__file__) \
        + '/OptimumLambdaSigned.mat')  # has the optimal values of lambda
    delta_vec = OptimumLambdaSigned['delta_vec'][0]
    lambda_opt = OptimumLambdaSigned['lambda_opt'][0]
    delta = 1/rfact
    lambdas = np.interp(delta, delta_vec, lambda_opt)

    # Initial values
    wn = np.zeros(y.shape, dtype=y.dtype)
    zn = y - forward_fun(wn)
    abc = 0
    nx, ny = y.shape[:]

    res_norm = np.zeros(maxiter+1)
    nn = np.zeros(maxiter+1)
    res_diff = np.zeros(maxiter)

    res_norm[0] = np.linalg.norm(zn)
    norm_y = np.linalg.norm(y)
    nn[0] = res_norm[0]/norm_y

    for abc in range(int(maxiter)):

        # First-order Approximate Message Passing
        temp_z = inverse_fun(zn) + wn

        # Randomly shift left, right if we asked for it
        if randshift:
            rand_shift_x = np.random.randint(0, nx)
            rand_shift_y = np.random.randint(0, ny)
            temp_z = np.roll(temp_z, (rand_shift_x, rand_shift_y))

        # Sparsify with wavelet transform
        temp_z, locations = cdf97_2d_forward(temp_z, level=5)

        # Compute sigma hat
        if sigmaType == 1:
            sigma_hat = np.median(np.abs(temp_z.flatten()))/.6745
        else:
            sigma_hat = res_norm[abc]/np.sqrt(mm)

        # If sigma is zero put any VERY small number
        if sigma_hat == 0:
            sigma_hat = .1

        # Soft Thresholding
        wn1 = (np.abs(temp_z) > lambdas*sigma_hat)*(np.abs(temp_z) \
            - lambdas*sigma_hat)*np.sign(temp_z)

        # Compute a sparsity/measurement ratio
        amp_weight = np.sum(np.abs(wn1) > np.finfo(float).eps)/mm

        # Un-sparsify
        wn1 = cdf97_2d_inverse(wn1, locations)

        # random shift back
        if randshift:
            wn1 = np.roll(wn1, (-rand_shift_x, -rand_shift_y))

        # Update the residual term
        residual = y - forward_fun(wn1)

        # Normalized data fidelity term
        res_norm[abc+1] = np.linalg.norm(residual)
        nn[abc+1] = res_norm[abc+1]/norm_y
        res_diff[abc] = np.abs(nn[abc+1] - nn[abc])

        # Give the people what they asked for!
        if disp:
            logging.info(
                table.row([
                    abc,
                    nn[abc+1],
                    res_diff[abc],
                    compare_mse(xabs, np.abs(wn1))]))

        # Check stopping criteria
        if not ignore_residual and (res_diff[abc] < tol):
            break

        # Update Estimation
        wn = wn1

        # Weight the residual with a little extra sauce
        if amp_weight > 1:
            zn = residual + 0.25*zn
        else:
            zn = residual + amp_weight*zn


    return wn
