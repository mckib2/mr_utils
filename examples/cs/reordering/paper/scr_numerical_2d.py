'''Spatially constrained reconstruction of 2D image using reordering.
'''

from functools import partial

import numpy as np
from scipy.optimize import minimize
from skimage.measure import compare_mse

from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.cs import proximal_GD
from mr_utils.cs import relaxed_ordinator
from mr_utils.utils.wavelet import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.utils.sort2d import sort2d
from mr_utils import view

if __name__ == '__main__':

    # Sim params
    N = 64 # x is NxN
    num_spokes = 16
    run = ['monosort', 'lagrangian'] # none is always run to get prior!

    # Need a reasonable numerical phantom
    x = np.rot90(modified_shepp_logan((N, N, N))[:, :, int(N/2)])
    # view(x)

    # Sparsifying transform
    level = 3
    wvlt, locations = cdf97_2d_forward(x, level)
    sparsify = lambda x: cdf97_2d_forward(x, level)[0]
    unsparsify = lambda x: cdf97_2d_inverse(x, locations)

    # Do radial golden-angle sampling
    mask = radial(x.shape, num_spokes, skinny=True, extend=False)
    uft = UFT(mask)
    kspace_u = uft.forward_ortho(x)
    view(kspace_u, fft=True)

    # # We need to find the best alpha for the no ordering recon
    # pGD = partial(
    #     proximal_GD, y=kspace_u, forward_fun=uft.forward_ortho,
    #     inverse_fun=uft.inverse_ortho, sparsify=sparsify,
    #     unsparsify=unsparsify, mode='soft', thresh_sep=True,
    #     selective=None, x=x, ignore_residual=False, disp=False, maxiter=500)
    # obj = lambda alpha0: compare_mse(np.abs(x), np.abs(pGD(alpha=alpha0)))
    # alpha0 = 0.05
    # res = minimize(obj, alpha0)
    # print(res)
    # The best is alpha0 = 0.01743203 for 500 iterations, N=64
    # The best alpha0 = 0.01328549 for 500 iters, N=16
    if N == 64:
        alpha0 = .01743203
    elif N == 16:
        alpha0 = 0.01328549
    recon_none = proximal_GD(
        kspace_u, uft.forward_ortho, uft.inverse_ortho, sparsify, unsparsify,
        reorder_fun=None, mode='soft', alpha=alpha0, thresh_sep=True,
        selective=None, x=x, ignore_residual=False, disp=True, maxiter=500)
    view(recon_none)

    if 'monosort' in run:
        # We need to find the best alpha for the monotonically sorted recon,
        # use the recon_none as the CS reconstruction prior
        _, reordering_r = sort2d(recon_none.real)
        _, reordering_i = sort2d(recon_none.imag)
        idx_ro = reordering_r + 1j*reordering_i
        monosort = lambda x: idx_ro
        # alpha = 0.05
        # pGD = partial(
        #     proximal_GD, y=kspace_u, forward_fun=uft.forward_ortho,
        #     inverse_fun=uft.inverse_ortho, sparsify=sparsify,
        #     unsparsify=unsparsify, reorder_fun=monosort, mode='soft',
        #     thresh_sep=True, selective=None, x=x, ignore_residual=False,
        #     disp=False, maxiter=200)
        # obj = lambda alpha0: compare_mse(
        #     np.abs(x), np.abs(pGD(alpha=alpha0)))
        # res = minimize(obj, alpha0)
        # print(res)
        # # Best alpha0 = 0.09299786 for 500 iterations, N=64
        # Best alpha0 = 0.01328549 for 500 iters, N=16
        if N == 64:
            alpha0 = 0.09299786
        elif N == 16:
            alpha0 = 0.01328549
        recon_sort2d = proximal_GD(
            kspace_u, uft.forward_ortho, uft.inverse_ortho, sparsify,
            unsparsify, reorder_fun=monosort, mode='soft', alpha=alpha0,
            thresh_sep=True, selective=None, x=x, ignore_residual=False,
            disp=True, maxiter=500)
        view(recon_sort2d)

        # Find k for recon_sort2d
        idx_r = np.unravel_index(idx_ro.real.astype(int), recon_sort2d.shape)
        idx_i = np.unravel_index(idx_ro.imag.astype(int), recon_sort2d.shape)
        coeffs = sparsify((
            recon_sort2d.real[idx_r] + 1j*recon_sort2d.imag[idx_i]).reshape(
                recon_sort2d.shape)).flatten()
        sorted_coeffs = -np.sort(-np.abs(coeffs))
        k_recon_sort2d = np.where(np.abs(sorted_coeffs) < 1e-5)[0][0]
        print('k_recon_sort2d is: %d' % k_recon_sort2d)

    if 'combinatorical' in run:
        print('2D problem is too large for combinatorical!')

    if 'lagrangian' in run:
        # This is actually quite hard to do, since it takes a while to run and
        # there are 3 parameters to tune: lam, k for relaxed_ordinator and
        # alpha for step size...
        # Choose k to be 80% of k_recon_sort2d.
        k = int(.8*k_recon_sort2d)
        print('k is: %d' % k)
        pi_real = relaxed_ordinator(recon_none.real, lam=.5, k=k,
                                    unsparsify=unsparsify)
        np.save('pi_real.npy', pi_real)
        print('done with pi_real')
        pi_imag = relaxed_ordinator(recon_none.imag, lam=.5, k=k,
                                    unsparsify=unsparsify)
        np.save('pi_imag.npy', pi_imag)
        print('done with pi_imag')
        idx_ls = pi_real + 1j*pi_imag
        lagrangesort = lambda x: idx_ls
        # alpha0 = .05
        recon_ls = proximal_GD(
            kspace_u, uft.forward_ortho, uft.inverse_ortho, sparsify,
            unsparsify, reorder_fun=lagrangesort, mode='soft', alpha=alpha0,
            thresh_sep=True, selective=None, x=x, ignore_residual=False,
            disp=True, maxiter=500)
        np.save('recon_ls.npy', recon_ls)
        # view(recon_ls)
