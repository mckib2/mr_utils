'''Enforce temporal TV sparisty using a gradient descent algorithm.'''

# import logging

import numpy as np
from tqdm import trange, tqdm
from skimage.measure import compare_mse, compare_ssim

from mr_utils.utils.printtable import Table
from mr_utils.cs.convex.temporal_gd_tv.sort_real_imag_parts import \
    sort_real_imag_parts

def GD_temporal_TV(
        prior,
        kspace_u,
        mask,
        weight_fidelity,
        weight_temporal,
        use_reorder=False,
        beta_sqrd=1e-8,
        x=None,
        maxiter=200):
    '''Gradient descent for generic encoding model and temporal TV constraint.
    '''

    measuredImgDomain = np.fft.fftshift(np.fft.ifft2(
        kspace_u, axes=(1, 2)), axes=(1, 2))

    # reduced_data = np.abs(measuredImgDomain)
    img_est = measuredImgDomain.copy()
    W_img_est = measuredImgDomain.copy()

    sort_order_real, sort_order_imag = sort_real_imag_parts(prior)

    # path = '/home/nicholas/Downloads/Temporal_reordering/'
    # sor = load_mat('%s/sort_order_real.mat' % path, key='sort_order_real').T
    # soi = load_mat('%s/sort_order_imag.mat' % path, key='sort_order_imag').T
    # assert np.allclose(sor - 1, sort_order_real)
    # assert np.allclose(soi - 1, sort_order_imag)

    # nIdx_real = sort_order_real
    # nIdx_imag = sort_order_imag

    # Intialize output
    table = Table(
        ['iter', 'norm', 'MSE', 'SSIM'],
        [len(repr(maxiter)), 8, 8, 8],
        ['d', 'e', 'e', 'e'])
    print(table.header())
    # for line in hdr.split('\n'):
    #     logging.info(line)
    if x is None:
        xabs = 0
    else:
        xabs = np.abs(x)
    stop_criteria = 0

    unsort_real_data = np.zeros(img_est.shape, dtype=np.single)
    unsort_imag_data = np.zeros(img_est.shape, dtype=np.single)

    temporal_term_update_real = np.zeros(img_est.shape, dtype=np.single)
    temporal_term_update_imag = np.zeros(img_est.shape, dtype=np.single)

    nIdx_real = np.unravel_index(sort_order_real, img_est.shape)
    nIdx_imag = np.unravel_index(sort_order_imag, img_est.shape)
    # path = '/home/nicholas/Downloads/Temporal_reordering/'
    # sor = load_mat('%s/nIdx_real.mat' % path, key='nIdx_real').T
    # soi = load_mat('%s/nIdx_imag.mat' % path, key='nIdx_imag').T
    # assert np.allclose(sor - 1, nIdx_real)
    # assert np.allclose(soi - 1, nIdx_imag)


    for ii in trange(maxiter, leave=False):

        fidelity_update = weight_fidelity*(measuredImgDomain - W_img_est)

        ## computing TV term update for real and imag parts with reordering
        # real part
        temp_b = np.diff(img_est.real[nIdx_real], axis=0)
        temp_b /= np.sqrt(beta_sqrd + (np.abs(temp_b)**2))
        temp_c = np.diff(temp_b, axis=0)

        temporal_term_update_real[0, :, :] = temp_b[0, :, :]
        temporal_term_update_real[1:-1, :, :] = temp_c
        temporal_term_update_real[-1, :, :] = -temp_b[-1, :, :]

        temporal_term_update_real *= weight_temporal
        unsort_real_data[nIdx_real] = temporal_term_update_real

        # imag part
        temp_b = np.diff(img_est.imag[nIdx_imag], axis=0)
        temp_b /= np.sqrt(beta_sqrd + (np.abs(temp_b)**2))
        temp_c = np.diff(temp_b, axis=0)

        temporal_term_update_imag[0, :, :] = temp_b[0, :, :]
        temporal_term_update_imag[1:-1, :, :] = temp_c
        temporal_term_update_imag[-1, :, :] = -temp_b[-1, :, :]

        temporal_term_update_imag *= weight_temporal
        unsort_imag_data[nIdx_imag] = temporal_term_update_imag

        temporal_term_update = unsort_real_data + 1j*unsort_imag_data
        img_est += fidelity_update + temporal_term_update
        W_img_est = np.fft.ifft2(np.fft.fft2(
            img_est, axes=(1, 2))*mask, axes=(1, 2))

        curxabs = np.abs(img_est)
        tqdm.write(
            table.row(
                [ii, stop_criteria, compare_mse(curxabs, xabs),
                 compare_ssim(curxabs, xabs)]))


    return img_est
