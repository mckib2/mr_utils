'''Comparison of reordering methods on cardiac reconstruction.

Compares:
    None
    Bulk up
    Whittle down
    sort2d
    colwise
    rowwise

Uses selective updating, as that really seems to get the job done.

Needs tunable params:
    level -- levels of decomposition for wavelet transform
    percent_to_keep -- how selective the update is
    maxiter -- how long to run the recon
    alpha -- step size
    k -- percent of coefficients to bulk up/whittle

In general, sort2d seems to win everytime, but they all perform similarly.
Perhaps if you had a strange transform that sorting didn't work with, you'd
want to give bulk/whittle a try, otherwise, it doesn't seem like it's worth
the hassle.

If the prior is the true image, then sort2d wins by a landslide, followed by
col-wise, row-wise, a tie with Bulk/Whittle, and then the not-sorted image.
If the prior is the corrupted image, then Bulk trends lower for longer.

It's kind of a mixed bag and hard to say with so many tuning parameters and
the need for cross validation.

Note: there's something strange with the cardiac data, so might want to try
out a different data set.  See fourier transform, strange phase.
'''

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from skimage.measure import compare_mse, compare_ssim

from mr_utils.test_data import load_test_data
from mr_utils import view
from mr_utils.cs import proximal_GD
from mr_utils.cs.models import UFT
from mr_utils.utils.wavelet import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.utils.orderings import bulk_up, whittle_down, colwise, rowwise
from mr_utils.utils.sort2d import sort2d

if __name__ == '__main__':

    # We need a mask
    mask = load_test_data('mr_utils/test_data/tests/recon/reordering',
                          ['mask'])[0]
    mask = np.fft.fftshift(mask)

    # Get the encoding model
    uft = UFT(mask)

    # Load in the test data
    kspace = load_test_data('mr_utils/test_data/tests/recon/reordering',
                            ['coil1'])[0]
    kspace = np.fft.fftshift(kspace)
    imspace = uft.inverse(kspace)

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = uft.inverse(kspace_u)

    # Sparsifying transforms
    level = 3
    wvlt, locations = cdf97_2d_forward(imspace, level)
    sparsify = lambda x: cdf97_2d_forward(x, level)[0]
    unsparsify = lambda x: cdf97_2d_inverse(x, locations)

    # Decide how we'll be selective in our updates
    percent_to_keep = .05
    num_to_keep = int(percent_to_keep*imspace.size)
    def select_n(x_hat, update):
        '''Return indices of n largest updates each iteration.'''
        return np.unravel_index(np.argpartition(
            np.abs(x_hat - update).flatten(),
            -num_to_keep)[-num_to_keep:], x_hat.shape)

    # Shared recon params
    prior = imspace_u.copy()
    maxiter = 200
    alpha = .008
    selective = select_n  # or None
    ignore = False
    disp = False

    # Reordering strategies
    k = .99
    with tqdm(total=3, desc='Bulk up/Whittle down', leave=False) as pbar:

        # Bulk up/Whittle down come up with similar performing orderings.
        #
        # There's a few ways we could do the reodering:
        #     Order complex prior
        #     Order abs prior
        #     Order real/imag
        # abs prior doesn't work very well, and complex seems to do better
        # than real as demonstrated below:

        # Calculate complex reordering
        idx_bu = bulk_up(prior, sparsify, unsparsify, k)
        idx_bu = idx_bu + 1j*idx_bu
        pbar.update()
        reorder_bu = lambda x: idx_bu

        # Calculate real/imag reordering
        idx_r = whittle_down(prior.real, sparsify, unsparsify, 1-k)
        pbar.update()
        idx_i = whittle_down(prior.imag, sparsify, unsparsify, 1-k)
        pbar.update()
        idx_wd = idx_r + 1j*idx_i
        reorder_wd = lambda x: idx_wd

        # Do 2d reordering
        _, reordering_r = sort2d(prior.real)
        _, reordering_i = sort2d(prior.imag)
        idx_ro = reordering_r + 1j*reordering_i
        reorder_ro = lambda x: idx_ro

        ## Col/row-wise seem to do the best in general.
        # Column wise reordering
        idx_r = colwise(prior.real)
        idx_i = colwise(prior.imag)
        idx_cw = idx_r + 1j*idx_i
        reorder_cw = lambda x: idx_cw

        # Row wise reordering
        idx_r = rowwise(prior.real)
        idx_i = rowwise(prior.imag)
        idx_rw = idx_r + 1j*idx_i
        reorder_rw = lambda x: idx_rw

        # Composite reordering
        tmp = prior.real[np.unravel_index(reordering_r, prior.shape)] \
            + 1j*prior.imag[np.unravel_index(reordering_i, prior.shape)]
        idx2 = bulk_up(tmp.reshape(prior.shape), sparsify, unsparsify, k)
        idx_cp = reordering_r[idx2] + 1j*reordering_i[idx2]
        reorder_cp = lambda x: idx_cp

        # How good did we reorder?
        sh = imspace.shape
        def get_true(idx):
            '''Get reordering of true image.'''
            idx_r = idx.real.astype(int)
            idx_i = idx.imag.astype(int)
            true = imspace.real[np.unravel_index(idx_r, sh)].reshape(sh) \
                + imspace.imag[np.unravel_index(idx_i, sh)].reshape(sh)
            return true

        # Get reordering of the true image for each ordering strategy
        bu_true = get_true(idx_bu)
        wd_true = get_true(idx_wd)
        s2d_true = get_true(idx_ro)
        col_true = get_true(idx_cw)
        row_true = get_true(idx_rw)
        comp_true = get_true(idx_cp)

        # Get the sorted coefficients
        coeffs0 = -np.sort(-np.abs(sparsify(imspace).flatten()))
        coeffs_bu = -np.sort(-np.abs(sparsify(bu_true).flatten()))
        coeffs_wd = -np.sort(-np.abs(sparsify(wd_true).flatten()))
        coeffs_2d = -np.sort(-np.abs(sparsify(s2d_true).flatten()))
        coeffs_col = -np.sort(-np.abs(sparsify(col_true).flatten()))
        coeffs_row = -np.sort(-np.abs(sparsify(row_true).flatten()))
        coeffs_comp = -np.sort(-np.abs(sparsify(comp_true).flatten()))

        # Plot them on a log axis so we can see what's going on
        plt.semilogy(coeffs0, '-', label='True coeffs')
        plt.semilogy(coeffs_bu, '--', label='BU coeffs')
        plt.semilogy(coeffs_wd, '-.', label='WD coeffs')
        plt.semilogy(coeffs_2d, label='sort2d coeffs')
        plt.semilogy(coeffs_col, label='CW coeffs')
        plt.semilogy(coeffs_row, label='RW coeffs')
        plt.semilogy(coeffs_comp, label='CP coeffs')
        plt.legend()
        plt.show(block=True)


    # Do the things
    x_no = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=None,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_ro = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=reorder_ro,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_bu = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=reorder_bu,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_wd = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=reorder_wd,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_cw = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=reorder_cw,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_rw = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=reorder_rw,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_cp = proximal_GD(kspace_u, forward_fun=uft.forward,
                       inverse_fun=uft.inverse, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=reorder_cp,
                       alpha=alpha, selective=selective, x=imspace,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    # Let's see how we did
    ys = [x_no, x_ro, x_bu, x_wd, x_cw, x_rw, x_cp]
    xs = ['None', 'sort2d', 'BU', 'WD', 'Col', 'Row', 'Comp']
    absx = np.abs(imspace)
    plt.figure()
    plt.scatter(xs, [compare_mse(absx, np.abs(x)) for x in ys])
    plt.title('MSE')
    plt.show(block=False)
    plt.figure()
    plt.scatter(xs, [compare_ssim(absx, np.abs(x)) for x in ys])
    plt.title('SSIM')
    plt.show()

    view(np.stack((imspace, imspace_u, *xs)))
