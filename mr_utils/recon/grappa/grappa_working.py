'''Get a simple GRAPPA implementation up and running.'''

import numpy as np
from skimage.util import view_as_windows, pad as skipad

from mr_utils import view

def grappa2d(x, R, acs, kx, coil_axis=0, R_axis=1):
    '''GRAPPA.

    Parameters
    ----------
    x : array_like
        Undersampled k-space data.
    R : int
        Undersampling factor.
    acs : array_like
        Boolean mask indicating where auto-calibration signal is
        located in x.
    kx : int
        Kernel size along the fully sampled dimension.  Kernel size
        in R_axis will always be 2 (the lines below and above).
    coil_axis : int
        Dimension of coil data.
    R_axis : int
        Dimension that has been undersampled by a factor R.
    '''

    # Do some rearranging to get things where we want them:
    #     (coil, x, y), where y is the dimension that is undersampled
    x = np.moveaxis(x, (coil_axis, R_axis), (0, -1))
    nc, nx, ny = x.shape[:]

    # Pad x so we get boundary patches
    x = skipad(x, 1, mode='constant')
    print(x.shape)

    # We need to train the weights
    ky = 2
    # w = np.zeros((nc*(R-1), nc*kx*ky), dtype=np.complex64)
    # print(w.shape)

    # Split the auto-calibration signal into patches.  This is built
    # for ky=2!
    coords = np.argwhere(acs)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    ACS = x[:, x0:x1, y0:y1].copy()

    # Get all possible patches in the ACS
    P = view_as_windows(ACS, (1, kx, R+1))[..., 0, :, :]
    print(P.shape)

    # Get the source matrices
    S = P[..., [0, -1]] # upper and lower fully sampled lines
    print(S.shape)

    # Get the target matrices
    if np.mod(kx, 2): # if odd
        ctr = int(kx/2)
        T = P[..., [ctr], 1:-1] # only want center inset line
    else: # if even
        raise NotImplementedError('kx must be odd!')
    print(T.shape)

    # move coil to end for stacking
    S = np.moveaxis(S, 0, -1)
    T = np.moveaxis(T, 0, -1)

    # Make the columns be from each patch
    S = S.reshape((-1, nc*kx*ky))
    T = T.reshape((-1, nc*(R-1)))
    print(S.shape, T.shape)

    # __                     __     __                     __
    # | T0,0     T1,0     ... |     | S0       S0       ... |
    # | T0,1     T1,1     ... | = W | S1       S1       ... |
    # |   .        .      ... |     | .        .        ... |
    # | T0,{R-1} T1,{R-1} ... |     | S{kx*ky} S{kx*ky} ... |
    # --                     --     --                     --

    w = np.linalg.lstsq(S, T, rcond=None)[0]
    print(w.shape)

    # Get all patches
    # P = view_as_windows(x, (1, kx, R+1))[..., 0, :, :]
    # view(P[:, 10, 10, ...])
    # print(P.shape)
    #
    # # Get the source matrices
    # S = P[..., [0, -1]] # upper and lower fully sampled lines
    # print(S.shape)
    #
    # sh = S.shape[1:3]
    # S = np.moveaxis(S, 0, -1)
    # S = S.reshape((-1, nc*kx*ky))
    # T = np.dot(S, w)
    # T = np.moveaxis(T.reshape((*sh, 1, R-1, nc)), -1, 0)
    # print(T.shape)
    #
    # recon = np.zeros(x.shape, dtype=x.dtype)
    # for ii in range(nx-2):
    #     for jj in range(ny-3):
    #         recon[:, ii, jj] = T[:, ii, jj, 0, 0]
    # view(recon, log=True)


    # # Get all patches not in the ACS, assuming ACS is rectangular:
    # # _____________________
    # # |      ____0___      |
    # # |  2   | ACS  |   3  |
    # # |      --------      |
    # # ----------1----------
    # nACS0 = x[:, :, :y0].copy()
    # nACS1 = x[:, :, y1:].copy()
    # nACS2 = x[:, :x0, :].copy()
    # nACS3 = x[:, y1:, :].copy()
    # print(nACS0.shape, y0, y1)
    #
    # S0 = view_as_windows(
    #     nACS0, (1, kx, 2), step=(1, 1, R))[..., 0, :, :]
    # S1 = view_as_windows(
    #     nACS1, (1, kx, 2), step=(1, 1, R))[..., 0, :, :]
    # # S2 = view_as_windows(
    # #     nACS2, (1, kx, 2), step=(1, 1, R))[..., 0, :, :]
    # # S3 = view_as_windows(
    # #     nACS3, (1, kx, 2), step=(1, 1, R))[..., 0, :, :]
    # print(S0.shape)
    #
    # # move coil to end for stacking
    # sh = S0.shape[1:3]
    # S0 = np.moveaxis(S0, 0, -1)
    # S1 = np.moveaxis(S1, 0, -1)
    # S0 = S0.reshape((-1, nc*kx*ky))
    # S1 = S1.reshape((-1, nc*kx*ky))
    # print(S0.shape)
    #
    # # Make targets by applying weights to sources
    # T0 = np.dot(S0, w)
    # T1 = np.dot(S1, w)
    # print(T0.shape)
    #
    # # Un-reshape
    # T0 = np.moveaxis(T0.reshape((*sh, 1, R-1, nc)), -1, 0)
    # T1 = np.moveaxis(T1.reshape((*sh, 1, R-1, nc)), -1, 0)
    # print(T0.shape)
    #
    # # Now put the targets in the right place
    # recon = np.zeros(x.shape, dtype=x.dtype)
    # for ii in range(T0.shape[2]):
    #
    #     # nACS0
    #     recon[:, 1:-1, (ii*R+1):(ii*R + R)] = T0[:, :, ii, 0, :]
    #
    #     # nACS1
    #     recon[:, 1:-1, y1+(ii*R+1):y1+(ii*R + R)] = T1[:, :, ii, 0, :]
    #
    # # Add in measured lines and the ACS
    # recon += x
    #
    # view(x, log=True)
    # view(recon, log=True)
    # view(recon, fft=True)
    # # view(x - recon, log=True)


if __name__ == '__main__':

    from sigpy import shepp_logan
    from sigpy.mri import birdcage_maps
    N = 128
    nc = 4
    im = shepp_logan((N, N))
    mps = birdcage_maps((nc, N, N))
    im = im[None, ...]*mps

    # Undersample kspace
    ax = (1, 2)
    kspace = 1/np.sqrt(N**2)*np.fft.fftshift(np.fft.fft2(
        np.fft.fftshift(im, axes=ax), axes=ax), axes=ax)
    mask = np.zeros(im.shape, dtype=bool)
    R = 3
    mask[..., ::R, :] = True
    kspace_u = kspace*mask
    # view(mask)

    # Add ACS
    acs = np.zeros((N, N), dtype=bool)
    ctr = int(N/2)
    pad = 10
    acs[ctr-pad:ctr+pad, :] = True
    kspace_u[:, ctr-pad:ctr+pad, :] = kspace[:, ctr-pad:ctr+pad, :]
    # view(kspace_u, fft=True)

    # view(kspace_u, log=True)
    grappa2d(kspace_u, R, acs, kx=3, coil_axis=0, R_axis=1)
