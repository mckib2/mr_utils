'''Simulate VC+GRAPPA+ESM.'''

import numpy as np
from pygrappa import grappa
from phantominator import shepp_logan
from sigpy.mri import birdcage_maps

from mr_utils.sim.ssfp import ssfp
from mr_utils.coils.coil_combine import gcc
from mr_utils.recon.ssfp import gs_recon

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

    # Combine to a number of virtual coils
    nvcs = 6
    imspace0 = np.zeros((4, N, N, nvcs), dtype=imspace.dtype)
    for ii in range(imspace.shape[0]):
        imspace0[ii, ...] = gcc(
            imspace[ii, ...], vcoils=nvcs, coil_axis=-1)
    imspace = imspace0

    from mr_utils import view
    view(imspace[0, ...])

    # Put 'er into  kspace
    ax = (1, 2)
    kspace = 1/np.sqrt(N**2)*np.fft.ifftshift(np.fft.fft2(
        np.fft.fftshift(imspace, axes=ax), axes=ax), axes=ax)

    recon = np.zeros((4, N, N, nvcs), dtype=kspace.dtype)
    for ii in range(imspace.shape[0]):
        # crop 20x20 window from the center of k-space for calibration
        pd = 10
        ctr = int(N/2)
        calib = kspace[ii, ctr-pd:ctr+pd, ctr-pd:ctr+pd, :].copy()

        # calibrate a kernel
        kernel_size = (5, 5)

        # undersample by a factor of 2 in both x and y
        kspace0 = kspace[ii, ...].copy()
        kspace0[::2, 1::2, :] = 0
        kspace0[1::2, ::2, :] = 0

        # reconstruct:
        res0 = grappa(
            kspace0, calib, kernel_size, coil_axis=-1,
            lamda=0.01, memmap=False)

        # Put back into image space
        ax0 = (0, 1)
        recon[ii, ...] = np.sqrt(N**2)*np.fft.fftshift(
            np.fft.ifft2(np.fft.ifftshift(
                res0, axes=ax0), axes=ax0), axes=ax0)

    from mr_utils import view
    view(recon[0, ...])

    # Do lGS coil by coil
    lgs = np.zeros((N, N, nvcs), dtype=recon.dtype)
    for cc in range(nvcs):
        lgs[..., cc] = gs_recon(recon[..., cc], pc_axis=0)

    from mr_utils import view
    view(lgs)
