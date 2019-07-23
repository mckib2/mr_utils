'''Simulate VC+ESPIRiT+ESM.'''

import numpy as np
from bart import bart
from phantominator import shepp_logan
from sigpy.mri import birdcage_maps

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.coils.coil_combine import gcc

if __name__ == '__main__':

    # Generate fake sensitivity maps: mps
    N = 128
    ncoils = 32
    mps = birdcage_maps((ncoils, N, N))
    mps = np.moveaxis(mps, 0, -1)

    # Make phase-cycled bSSFP phantom
    ph = shepp_logan(N)
    TR, alpha = 6e-3, np.deg2rad(30)
    pcs = np.linspace(0, 2*np.pi, 4, endpoint=False)
    min_df, max_df = -1/TR, 1/TR
    fx = np.linspace(min_df, max_df, N)
    fy = np.zeros(N)
    df, _ = np.meshgrid(fx, fy)
    ph = ssfp(
        ph, ph/2, TR, alpha, df, phase_cyc=pcs, M0=ph, delta_cs=0,
        phi_rf=0, phi_edd=0, phi_drift=0)
    print(ph.shape)

    # Apply sensitivities
    imspace = ph[..., None]*mps
    print(imspace.shape)

    # Put 'er into  kspace
    ax = (1, 2)
    kspace = 1/np.sqrt(N**2)*np.fft.ifftshift(np.fft.fft2(
        np.fft.fftshift(imspace, axes=ax), axes=ax), axes=ax)

    # crop 20x20 window from the center of k-space for calibration
    pd = 10
    ctr = int(N/2)
    calib = kspace[:, ctr-pd:ctr+pd, ctr-pd:ctr+pd, :].copy()

    # undersample by a factor of 2 in both x and y
    kspace0 = kspace.copy()
    kspace0[:, ::2, 1::2, :] = 0
    kspace0[:, 1::2, ::2, :] = 0

    # Put ACS back in
    kspace0[:, ctr-pd:ctr+pd, ctr-pd:ctr+pd, :] = calib.copy()

    # Put back in imspace
    imspace_u = np.sqrt(N**2)*np.fft.ifftshift(np.fft.fft2(
        np.fft.fftshift(kspace0, axes=ax), axes=ax), axes=ax)

    from mr_utils.coils.coil_combine import (
        rigid_composite_ellipse, simple_composite_ellipse)
    # phase = simple_composite_ellipse(
    #     imspace_u, coil_axis=-1, pc_axis=0)
    # phase = rigid_composite_ellipse(
    #     imspace_u, coil_axis=-1, pc_axis=0)

    from skimage.util import pad
    print(calib.shape, kspace.shape)
    _, cx, cy, _ = calib.shape[:]
    pd = int((N - cx)/2)
    pcalib = pad( # pylint: disable=E1102
        calib, ((0, 0), (pd, pd), (pd, pd), (0, 0)), mode='constant')
    print(pcalib.shape, kspace.shape)
    lowres = np.sqrt(N**2)*np.fft.ifftshift(np.fft.fft2(
        np.fft.fftshift(pcalib, axes=ax), axes=ax), axes=ax)
    phase = simple_composite_ellipse(
        lowres, coil_axis=-1, pc_axis=0)
    # phase = rigid_composite_ellipse(
    #     lowres, coil_axis=-1, pc_axis=0)

    phase = np.unwrap(phase, axis=0)
    print(phase.shape)

    # Combine to a number of virtual coils
    nvcs = 6
    imspace0 = np.zeros((4, N, N, nvcs), dtype=imspace.dtype)
    for ii in range(imspace.shape[0]):
        imspace0[ii, ...] = gcc(
            imspace_u[ii, ...], vcoils=nvcs, coil_axis=-1)
    imspace_u = imspace0

    # Do espirit recon for each PC
    recon = np.zeros((4, N, N), dtype=kspace.dtype)
    for ii in range(kspace.shape[0]):

        # Put empty z axis for BART
        kspace00 = kspace0[ii, :, :, None, :].copy()

        # Estimate coil sensitivities
        espirit_mps = bart(1, 'ecalib -r20 -m1', kspace00)

        # Do the recon
        recon[ii, ...] = bart(1, 'pics -r0.01', kspace00, espirit_mps)

    # Run lGS on recon
    recon = np.abs(recon)*np.exp(1j*phase)
    lgs = gs_recon(recon, pc_axis=0)

    from mr_utils import view
    view(lgs)
