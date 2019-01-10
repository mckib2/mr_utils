import numpy as np
from mr_utils.utils import dTV
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def GD_FE_TV(kspace,samp,alpha=.5,lam=.01,im_true=None,ignore_residual=False,disp=False,maxiter=200):
    '''Gradient descent for Fourier encoding model and TV constraint.

    kspace -- Measured image.
    samp -- Sampling mask.
    alpha -- Step size.
    lam -- TV constraint weight.
    im_true -- The true image we are trying to reconstruct.
    ignore_residual -- Whether or not to break out of loop if resid increases.
    disp -- Whether or not to display iteration info.
    maxiter -- Maximum number of iterations.

    Solves the problem:
        min_x || kspace - FFT(im*samp) ||^2_2  + lam*TV(im)

    If im_true=None, then MSE will not be calculated.
    '''

    # Make sure compare_mse is defined
    if im_true is None:
        compare_mse = lambda x,y: 0
        logging.info('No true x provided, MSE will not be calculated.')
    else:
        from skimage.measure import compare_mse
        im_true = np.abs(im_true)

    # Get some display stuff happening
    if disp:
        from mr_utils.utils.printtable import Table
        table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    # Initialize
    m_hat = np.zeros(kspace.shape,dtype=kspace.dtype)
    r = -kspace.copy()
    prev_stop_criteria = np.inf

    # Do the thing
    for ii in range(int(maxiter)):

        # Fidelity term
        fidelity = np.fft.ifft2(r)

        # Sparsity term
        second_term = dTV(m_hat)

        # Compute stop criteria
        stop_criteria = np.linalg.norm(r)
        if not ignore_residual and stop_criteria > prev_stop_criteria:
            logging.warning('Breaking out of loop after %d iterations. Norm of residual increased!' % ii)
            break
        prev_stop_criteria = stop_criteria

        # Take the step
        m_hat -= alpha*(fidelity + lam*second_term)

        # Tell the user what happened
        if disp:
            logging.info(table.row([ ii,stop_criteria,compare_mse(np.abs(m_hat),im_true) ]))

        # Compute residual
        r = np.fft.fft2(m_hat)*samp - kspace


    return(m_hat)
