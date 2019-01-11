import numpy as np
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def IHT_FE_TV(kspace,samp,k,mu=1,tol=1e-8,do_reordering=False,x=None,ignore_residual=False,disp=False,maxiter=500):
    '''IHT for Fourier encoding model and TV constraint.

    kspace -- Measured image.
    samp -- Sampling mask.
    k -- Sparsity measure (number of nonzero coefficients expected).
    mu -- Step size.
    tol -- Stop when stopping criteria meets this threshold.
    do_reordering -- Reorder column-stacked true image.
    x -- The true image we are trying to reconstruct.
    ignore_residual -- Whether or not to break out of loop if resid increases.
    disp -- Whether or not to display iteration info.
    maxiter -- Maximum number of iterations.

    Solves the problem:
        min_x || kspace - FFT(x) ||^2_2  s.t.  || FD(x) ||_0 <= k

    If im_true=None, then MSE will not be calculated.
    '''

    # Make sure we have a defined compare_mse and Table for printing
    if disp:
        from mr_utils.utils.printtable import Table

        if x is not None:
            from skimage.measure import compare_mse
            x = np.abs(x)
        else:
            compare_mse = lambda x,y: 0

    # Right now we are doing absolute values on updates
    x_hat = np.zeros(kspace.shape)
    r = kspace.copy()
    prev_stop_criteria = np.inf
    norm_kspace = np.linalg.norm(kspace)

    # Initialize display table
    if disp:
        table = Table([ 'iter','norm','MSE' ],[ len(repr(maxiter)),8,8 ],[ 'd','e','e' ])
        hdr = table.header()
        for line in hdr.split('\n'):
            logging.info(line)

    # Find perfect reordering (column-stacked-wise)
    if do_reordering:
        reordering = np.argsort(x.flatten())
        inverse_reordering = [0]*len(reordering)
        for send_from,send_to in enumerate(reordering):
            inverse_reordering[send_to] = send_from

        # Find new sparsity measure
        if x is not None:
            k = np.sum(np.abs(np.diff(x.flatten()[reordering])) > 0)
        else:
            logging.warning('Make sure sparsity level k is adjusted for reordering!')

    # Do the thing
    for ii in range(int(maxiter)):

        # Density compensation!!!!
        #

        # Take step
        val = (x_hat + mu*np.abs(np.fft.ifft2(r))).flatten()

        # Do the reordering
        if do_reordering:
            val = val[reordering]

        # Finite differences transformation
        first_samp = val[0] # save the first sample for inverse transform
        fd = np.diff(val)

        # Hard thresholding
        fd[np.argsort(np.abs(fd))[:-k]] = 0

        # Inverse finite differences transformation
        res = np.hstack((first_samp,fd)).cumsum()
        if do_reordering:
            res = res[inverse_reordering]

        # Compute stopping criteria
        stop_criteria = np.linalg.norm(r)/norm_kspace

        # If the stop_criteria gets worse, get out of dodge
        if not ignore_residual and (stop_criteria > prev_stop_criteria):
            logging.warning('Residual increased! Not continuing!')
            break
        prev_stop_criteria = stop_criteria

        # Update x
        x_hat = res.reshape(x_hat.shape)

        # Show the people what they asked for
        if disp:
            logging.info(table.row([ ii,stop_criteria,compare_mse(x,x_hat) ]))
        if stop_criteria < tol:
            break

        # update the residual
        r = kspace - np.fft.fftshift(np.fft.fft2(x_hat))*samp

    return(x_hat)
