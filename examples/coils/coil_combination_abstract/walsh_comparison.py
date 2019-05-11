'''Compare matched filter coil combination with ESM.'''

import numpy as np
from skimage.measure import compare_mse
from skimage.filters import threshold_li

from ismrmrdtools.simulation import (
    generate_birdcage_sensitivities as gbs)

from mr_utils.test_data.phantom import bssfp_2d_cylinder
from mr_utils.coils.coil_combine import walsh, walsh_gs
from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

def cc_then_gs_no_avg(coil_ims, noise_ims):
    '''Coil combine using individual csm then GS recon.'''

    # How many phase-cycles?
    npcs = coil_ims.shape[-1]

    # Coil combine each phase-cycle separately
    cc1 = np.zeros(coil_ims.shape[1:], dtype='complex')
    for ii in range(npcs):
        csm = walsh(coil_ims[..., ii], noise_ims[..., ii])
        cc1[..., ii] = np.sum(csm*np.conj(coil_ims[..., ii]), axis=0)
    return gs_recon(cc1, pc_axis=-1)

def cc_then_gs_avg_csm(coil_ims, noise_ims):
    '''Coil combine using averaged csm then GS recon.
    '''

    # How many phase-cycles?
    npcs = coil_ims.shape[-1]

    # Average the coil sensitivities for each phase-cycle
    csm0 = np.zeros(coil_ims.shape, dtype='complex')
    for ii in range(npcs):
        csm0[..., ii] = walsh(coil_ims[..., ii], noise_ims[..., ii])
    csm0 = np.mean(csm0, axis=-1)

    # Apply to each phase-cycle
    cc0 = np.zeros(coil_ims.shape[1:], dtype='complex')
    for ii in range(npcs):
        cc0[..., ii] = np.sum(csm0*np.conj(coil_ims[..., ii]), axis=0)
    return gs_recon(cc0, pc_axis=-1)

def cc_then_gs_avg_cov(coil_ims, noise_ims):
    '''Do coil combine averaging covariance matrices then do GS.'''

    # How many phase-cycles?
    npcs = coil_ims.shape[-1]

    # Average the correlation matrices
    csm0 = walsh_gs(
        coil_ims, coil_axis=0, pc_axis=-1, avg_method='cov')

    # Apply to each phase-cycle
    cc0 = np.zeros(coil_ims.shape[1:], dtype='complex')
    for ii in range(npcs):
        cc0[..., ii] = np.sum(csm0*np.conj(coil_ims[..., ii]), axis=0)
    return gs_recon(cc0, pc_axis=-1)

def cc_then_gs_avg_pc(coil_ims, noise_ims):
    '''Do coil combine averaging correcting for PCs then do GS.'''

    # How many phase-cycles?
    npcs = coil_ims.shape[-1]

    # Average the correlation matrices
    csm0 = walsh_gs(
        coil_ims, coil_axis=0, pc_axis=-1, avg_method='pc')

    # Apply to each phase-cycle
    cc0 = np.zeros(coil_ims.shape[1:], dtype='complex')
    for ii in range(npcs):
        cc0[..., ii] = np.sum(csm0*np.conj(coil_ims[..., ii]), axis=0)
    return gs_recon(cc0, pc_axis=-1)

def gs_then_cc(coil_ims, noise_ims):
    '''Do GS recon on each coil then coil combine.'''

    # How many coils?
    nc = coil_ims.shape[0]

    # Now the other way
    gs = np.zeros(coil_ims.shape[:-1], dtype='complex')
    n = np.zeros(noise_ims.shape[:-1], dtype='complex')
    for ii in range(nc):
        gs[ii, ...] = gs_recon(coil_ims[ii, ...], pc_axis=-1)

        # GS recon for the noise, too, to make sure we track what
        # happens to the noise characteristics
        n[ii, ...] = gs_recon(noise_ims[ii, ...], pc_axis=-1)

    csm1 = walsh(gs, n)
    return np.sum(csm1*np.conj(gs), axis=0)

def get_ims(N, npcs, nc, radius, SNR=np.inf):
    '''Generate coil images and truth image.'''

    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    coil_sens = gbs(N, number_of_coils=nc)

    # Now get phase-cycles
    coil_ims = np.zeros((nc, N, N, len(pcs)), dtype='complex')
    for ii, pc in enumerate(pcs):
        ims = bssfp_2d_cylinder(
            dims=(N, N), phase_cyc=pc, radius=radius)

        # Apply coil sensitivities to coil images
        coil_ims[:, ..., ii] = ims*coil_sens

    # Add noise
    if SNR != np.inf:
        im_r = np.mean(np.abs(coil_ims.real)[
            np.nonzero(coil_ims.real)])
        im_i = np.mean(np.abs(coil_ims.imag)[
            np.nonzero(coil_ims.imag)])

        noise_std_r = im_r/SNR
        noise_std_i = im_i/SNR
        nr = np.random.normal(0, noise_std_r, coil_ims.shape)
        ni = np.random.normal(0, noise_std_i, coil_ims.shape)
        coil_ims += nr + 1j*ni

        nr = np.random.normal(0, noise_std_r, coil_ims.shape)
        ni = np.random.normal(0, noise_std_i, coil_ims.shape)
        noise_ims = nr + 1j*ni
    else:
        noise_ims = np.zeros(coil_ims.shape)
    # view(coil_ims)


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

    return(coil_ims, noise_ims, im_true)

if __name__ == '__main__':

    N = 64
    nc = 6
    radius = .9
    npcs = 4
    SNR = 5
    # SNR = np.inf
    coil_ims, noise_ims, im_true = get_ims(N, npcs, nc, radius, SNR)
    # view(coil_ims)

    # Get a mask so we only look at phantom for comparisons
    thresh = threshold_li(np.abs(im_true))
    mask = np.abs(im_true) > thresh

    # Generate all the variants
    cc_then_gs_no_avg0 = cc_then_gs_no_avg(coil_ims, noise_ims)*mask
    cc_then_gs_avg_csm0 = cc_then_gs_avg_csm(coil_ims, noise_ims)*mask
    cc_then_gs_avg_cov0 = cc_then_gs_avg_cov(coil_ims, noise_ims)*mask
    cc_then_gs_avg_pc0 = cc_then_gs_avg_pc(coil_ims, noise_ims)*mask
    gs_then_cc0 = gs_then_cc(coil_ims, noise_ims)*mask

    # # Sanity check
    # assert np.allclose(cc_then_gs_avg_cov0, cc_then_gs_avg_pc0)

    # Check out the damage:
    err_fac = 5
    ims = np.stack((
        cc_then_gs_no_avg0,
        cc_then_gs_avg_csm0,
        cc_then_gs_avg_cov0,
        cc_then_gs_avg_pc0,
        gs_then_cc0,

        (np.abs(im_true) - np.abs(cc_then_gs_no_avg0))*err_fac,
        (np.abs(im_true) - np.abs(cc_then_gs_avg_csm0))*err_fac,
        (np.abs(im_true) - np.abs(cc_then_gs_avg_cov0))*err_fac,
        (np.abs(im_true) - np.abs(cc_then_gs_avg_pc0))*err_fac,
        (np.abs(im_true) - np.abs(gs_then_cc0))*err_fac,
    ))

    mse = lambda x: compare_mse(
        im_true.real, x.real) + compare_mse(im_true.imag, x.imag)
    mseabs = lambda x: compare_mse(np.abs(im_true), np.abs(x))
    msepha = lambda x: compare_mse(np.angle(im_true), np.angle(x))
    print('cc_then_gs_no_avg0:   %.20f' % mse(cc_then_gs_no_avg0))
    print('cc_then_gs_avg_csm0:  %.20f' % mse(cc_then_gs_avg_csm0))
    print('cc_then_gs_avg_cov0:  %.20f' % mse(cc_then_gs_avg_cov0))
    print('cc_then_gs_avg_pc0:   %.20f' % mse(cc_then_gs_avg_pc0))
    print('gs_then_cc0:          %.20f' % mse(gs_then_cc0))

    print('cc_then_gs_no_avg0:   %.20f' % (
        mseabs(cc_then_gs_no_avg0)), msepha(cc_then_gs_no_avg0))
    print('cc_then_gs_avg_csm0:  %.20f' % (
        mseabs(cc_then_gs_avg_csm0)), msepha(cc_then_gs_avg_csm0))
    print('cc_then_gs_avg_cov0:  %.20f' % (
        mseabs(cc_then_gs_avg_cov0)), msepha(cc_then_gs_avg_cov0))
    print('cc_then_gs_avg_pc0:   %.20f' % (
        mseabs(cc_then_gs_avg_pc0)), msepha(cc_then_gs_avg_pc0))
    print('gs_then_cc0:          %.20f' % (
        mseabs(gs_then_cc0)), msepha(gs_then_cc0))

    view(ims, montage_axis=0)
