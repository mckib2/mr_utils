'''Enforce temporal TV sparisty using a gradient descent algorithm.'''

# import logging
from ctypes import c_float

import numpy as np
from tqdm import trange, tqdm
from skimage.measure import compare_mse, compare_ssim

from mr_utils.utils.printtable import Table
from mr_utils.cs.convex.temporal_gd_tv.sort_real_imag_parts import (
    sort_real_imag_parts)

def GD_temporal_TV(
        prior,
        kspace_u,
        mask,
        weight_fidelity,
        weight_temporal,
        forward_fun,
        inverse_fun,
        temporal_axis=-1,
        beta_sqrd=1e-7,
        x=None,
        maxiter=200):
    '''Gradient descent for generic encoding model, temporal TV.

    Notes
    -----

    '''
    # Make sure that the temporal axis is last
    if (temporal_axis != -1) and (temporal_axis != mask.ndim-1):
        prior = np.moveaxis(prior, temporal_axis, -1)
        kspace_u = np.moveaxis(kspace_u, temporal_axis, -1)
        mask = np.moveaxis(mask, temporal_axis, -1)

    # Get the image space of the data we did measure
    measuredImgDomain = inverse_fun(kspace_u)

    # Initialize estimates
    img_est = measuredImgDomain.copy()
    W_img_est = measuredImgDomain.copy()

    # Get monotonic ordering
    sort_order_real, sort_order_imag = sort_real_imag_parts(
        prior, axis=-1)

    # # Construct R and C (rows and columns, I assume)
    # rows, cols, pages = img_est.shape[:]
    # R = np.tile(
    #     np.arange(rows), (cols, pages, 1)).transpose((2, 0, 1))
    # C = np.tile(
    #     np.arange(cols), (rows, pages, 1)).transpose((0, 2, 1))
    #
    # # Get the actual indices
    # nIdx_real = R + C*rows + (sort_order_real)*rows*cols
    # nIdx_imag = R + C*rows + (sort_order_imag)*rows*cols

    # Intialize output
    table = Table(
        ['iter', 'norm', 'MSE', 'SSIM'],
        [len(repr(maxiter)), 8, 8, 8],
        ['d', 'e', 'e', 'e'])
    print(table.header())
    if x is None:
        xabs = 0
    else:
        xabs = np.abs(x)
    stop_criteria = 0

    unsort_real_data = np.zeros(img_est.shape, dtype=c_float)
    unsort_imag_data = np.zeros(img_est.shape, dtype=c_float)
    temporal_term_update_real = np.zeros(img_est.shape, dtype=c_float)
    temporal_term_update_imag = np.zeros(img_est.shape, dtype=c_float)

    # Do the thing
    for ii in trange(maxiter, leave=False):

        fidelity_update = weight_fidelity*(
            measuredImgDomain - W_img_est)

        ## computing TV term update for real and imag parts with
        # reordering
        real_smooth_data = np.take_along_axis( #pylint: disable=E1101
            img_est.real, sort_order_real, axis=-1)
        imag_smooth_data = np.take_along_axis( #pylint: disable=E1101
            img_est.imag, sort_order_imag, axis=-1)

        # Real part
        temp_a = np.diff(real_smooth_data, axis=-1)
        temp_b = temp_a/np.sqrt(beta_sqrd + (np.abs(temp_a)**2))
        temp_c = np.diff(temp_b, axis=-1)

        temporal_term_update_real[..., 0] = temp_b[..., 0]
        temporal_term_update_real[..., 1:-1] = temp_c
        temporal_term_update_real[..., -1] = -temp_b[..., -1]

        temporal_term_update_real *= weight_temporal
        np.put_along_axis( #pylint: disable=E1101
            unsort_real_data, sort_order_real,
            temporal_term_update_real, axis=-1)


        # Imag part
        temp_a = np.diff(imag_smooth_data, axis=-1)
        temp_b = temp_a/np.sqrt(beta_sqrd + (np.abs(temp_a)**2))
        temp_c = np.diff(temp_b, axis=-1)

        temporal_term_update_imag[..., 0] = temp_b[..., 0]
        temporal_term_update_imag[..., 1:-1] = temp_c
        temporal_term_update_imag[..., -1] = -temp_b[..., -1]

        temporal_term_update_imag *= weight_temporal
        np.put_along_axis( #pylint: disable=E1101
            unsort_imag_data, sort_order_imag,
            temporal_term_update_imag, axis=-1)

        # Do the updates
        temporal_term_update = unsort_real_data + 1j*unsort_imag_data
        img_est += fidelity_update + temporal_term_update

        # W_img_est = inverse_fun(forward_fun(img_est))
        W_img_est = np.fft.ifft2(np.fft.fft2(
            img_est, axes=(0, 1))*mask, axes=(0, 1))

        # from mr_utils import view
        # view(np.stack((prior, img_est)))

        # Give user an update
        curxabs = np.abs(img_est)
        tqdm.write(
            table.row(
                [ii, stop_criteria, compare_mse(curxabs, xabs),
                 compare_ssim(curxabs, xabs)]))


    return img_est
