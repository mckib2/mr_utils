'''Simulate ESPIRiT+ESM.'''

import numpy as np
from bart import bart
from phantominator import shepp_logan

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon

if __name__ == '__main__':

    # Generate fake sensitivity maps: mps
    N = 128
    ncoils = 4
    xx = np.linspace(0, 1, N)
    x, y = np.meshgrid(xx, xx)
    mps = np.zeros((N, N, ncoils))
    mps[..., 0] = x**2
    mps[..., 1] = 1 - x**2
    mps[..., 2] = y**2
    mps[..., 3] = 1 - y**2

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

    # Do espirit recon for each PC
    recon = np.zeros((4, N, N), dtype=kspace.dtype)
    for ii in range(kspace.shape[0]):

        # crop 20x20 window from the center of k-space for calibration
        pd = 10
        ctr = int(N/2)
        calib = kspace[ii, ctr-pd:ctr+pd, ctr-pd:ctr+pd, :].copy()

        # undersample by a factor of 2 in both x and y
        kspace0 = kspace[ii, ...].copy()
        kspace0[::2, 1::2, :] = 0
        kspace0[1::2, ::2, :] = 0

        # Put ACS back in
        kspace0[ctr-pd:ctr+pd, ctr-pd:ctr+pd, :] = calib

        # Put empty z axis for BART
        kspace0 = kspace0[:, :, None, :]

        # Estimate coil sensitivities
        espirit_mps = bart(1, 'ecalib -r20 -m1', kspace0)

        # Do the recon
        recon[ii, ...] = bart(1, 'pics -r0.01', kspace0, espirit_mps)

        # from mr_utils import view
        # view(recon[ii, ...])

    # Run lGS on recon
    lgs = gs_recon(recon, pc_axis=0)

    from mr_utils import view
    view(lgs)
