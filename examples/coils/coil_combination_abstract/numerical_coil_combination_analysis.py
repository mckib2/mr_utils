'''Numerical simulations for coil analysis presentation.
'''

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from skimage.filters import threshold_li
from skimage.measure import compare_mse

from ismrmrdtools.simulation import (
    generate_birdcage_sensitivities as gbs)

from mr_utils.test_data.phantom import bssfp_2d_cylinder
from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

from examples.coils.coil_combination_abstract.coil_combine_funs import get_coil_combine_funs

if __name__ == '__main__':

    # Simple numerical phantom
    X, Y = 512, 256
    # X, Y = 64, 32
    # num_coils = [2, 4, 8, 12, 16]
    num_coils = [4]
    see_coil_images = [4]
    N = np.max([X, Y])
    M = np.min([X, Y])
    radius = M/N
    pcs = [0, np.pi/2, np.pi, 3*np.pi/2]
    npcs = len(pcs)
    ims = dict()
    coil_ims = dict()
    for nc in num_coils:
        # Generate coil sensitivities for this number of coils
        coil_sens = gbs(N, number_of_coils=nc)

        # Now get phase-cycles
        ims[nc] = np.zeros((N, N, npcs), dtype='complex')
        coil_ims[nc] = np.zeros((nc, N, N, len(pcs)), dtype='complex')
        for ii, pc in enumerate(pcs):
            ims[nc][..., ii] = bssfp_2d_cylinder(
                dims=(N, N), phase_cyc=pc, radius=radius)

            # Apply coil sensitivities to coil images
            coil_ims[nc][:, ..., ii] = (
                ims[nc][..., ii]*coil_sens)

        # Trim down to correct size
        if X < Y:
            trim = int((Y - X)/2)
            coil_ims[nc] = coil_ims[nc][:, trim:-trim, ...]
        elif X > Y:
            trim = int((X - Y)/2)
            coil_ims[nc] = coil_ims[nc][:, :, trim:-trim, ...]
        # view(coil_ims[nc])

    # # See coil images for ESM block diagram
    # demo_cc_then_gs = True
    # recon = np.zeros((4, M, M), dtype='complex')
    # for ii in range(4):
    #     if demo_cc_then_gs:
    #         recon[ii, ...] = view(
    #             coil_ims[4][:, trim:-trim, :, ii], fft_axes=(1, 2),
    #             is_imspace=True, coil_combine_axis=0)
    #     else:
    #         view(coil_ims[4][ii, trim:-trim, ...])
    #         recon[ii, ...] = gs_recon(
    #             coil_ims[4][ii, trim:-trim, ...], pc_axis=-1)
    # if not demo_cc_then_gs:
    #     view(recon, fft_axes=(1, 2), is_imspace=True,
    #          coil_combine_axis=0)
    # else:
    #     view(recon)
    #     view(gs_recon(recon, pc_axis=0))

    # Get truth image
    pcs_true = np.linspace(0, 2*np.pi, 16, endpoint=False)
    ngs = int(pcs_true.size/4)
    im_true = np.zeros((N, N, ngs), dtype='complex')
    tmp = np.zeros((N, N, pcs_true.size), dtype='complex')
    for ii, pc in enumerate(pcs_true):
        tmp[..., ii] = bssfp_2d_cylinder(
            dims=(N, N), phase_cyc=pc, radius=radius)
    for ii in range(ngs):
        im_true[..., ii] = gs_recon(tmp[..., ii::ngs], pc_axis=-1)
    im_true = np.mean(im_true, axis=-1)

    # Trim down to correct size
    if X < Y:
        trim = int((Y - X)/2)
        im_true = im_true[trim:-trim, ...]
    elif X > Y:
        trim = int((X - Y)/2)
        im_true = im_true[:, trim:-trim, ...]
    # view(im_true)

    # Get a mask so we only look at phantom for comparisons
    thresh = threshold_li(np.abs(im_true))
    mask = np.abs(im_true) > thresh
    # view(mask)

    # Define coil combination functions
    ccs, cc_list = get_coil_combine_funs(M)

    # Do coil combine then ESM
    res = np.zeros((len(num_coils), len(ccs), X, Y), dtype='complex')
    err_cc_then_gs = np.zeros((len(num_coils), len(ccs)))
    for coil, nc in enumerate(num_coils):
        for fun, cc in enumerate(ccs):

            tmp = np.zeros((X, Y, npcs), dtype='complex')
            for ii in range(npcs):
                tmp[..., ii] = cc(coil_ims[nc][..., ii])
            res[coil, fun, ...] = gs_recon(tmp, pc_axis=-1)*mask
            # view(res[coil, fun, ...])

            err_cc_then_gs[coil, fun] = compare_mse(
                np.abs(im_true),
                np.abs(np.nan_to_num(res[coil, fun, ...])))

        if nc in see_coil_images:
            view(np.concatenate((
                res[coil, :, trim:-trim, ...],
                im_true[None, trim:-trim, :]), axis=0))

    # error plot
    for fun, cc in enumerate(ccs):
        linestyle_cycler = cycler('linestyle', ['-', '--', ':', '-.'])
        color_cycler = cycler('color', list('rbg'))
        plt.rc('axes', prop_cycle=(linestyle_cycler*color_cycler))
        plt.semilogy(
            num_coils, err_cc_then_gs[:, fun], marker='.',
            label=cc_list[fun])
    plt.title('log(MSE) vs # coils')
    plt.xlabel('Number of coils')
    plt.ylabel('log(MSE)')
    plt.legend()
    plt.show()

    # Do ESM then coil combine
    res = np.zeros((len(num_coils), len(ccs), X, Y), dtype='complex')
    err_gs_then_cc = np.zeros((len(num_coils), len(ccs)))
    for coil, nc in enumerate(num_coils):
        for fun, cc in enumerate(ccs):

            tmp = np.zeros((nc, X, Y), dtype='complex')
            for ii in range(nc):
                tmp[ii, ...] = gs_recon(
                    coil_ims[nc][ii, ..., :], pc_axis=-1)

            res[coil, fun, ...] = cc(tmp)
            # view(res[coil, fun, ...])

            err_gs_then_cc[coil, fun] = compare_mse(
                np.abs(im_true),
                np.abs(np.nan_to_num(res[coil, fun, ...])))

        if nc in see_coil_images:
            view(np.concatenate((
                res[coil, :, trim:-trim, ...],
                im_true[None, trim:-trim, :]), axis=0))

    # error plot
    for fun, cc in enumerate(ccs):
        linestyle_cycler = cycler('linestyle', ['-', '--', ':', '-.'])
        color_cycler = cycler('color', list('rbg'))
        plt.rc('axes', prop_cycle=(linestyle_cycler*color_cycler))
        plt.semilogy(
            num_coils, err_gs_then_cc[:, fun], marker='.',
            label=cc_list[fun])
    plt.title('log(MSE) vs # coils')
    plt.xlabel('Number of coils')
    plt.ylabel('log(MSE)')
    plt.legend()
    plt.show()
