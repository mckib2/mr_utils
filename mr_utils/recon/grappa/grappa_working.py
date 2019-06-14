'''Get a simple GRAPPA implementation up and running.'''

import numpy as np
from skimage.util.shape import view_as_windows

def grappa2d(x, R, acs, kx, coil_axis=0, R_axis=1):
    '''Generalized autocalibrating partially parallel acquisiton.

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

    # We need to train the weights
    ky = 2
    w = np.zeros((nc*(R-1), nc*kx*ky), dtype=np.complex64)

    # Split the auto-calibration signal into patches.  This is built
    # for ky=2!
    coords = np.argwhere(acs)
    x0, y0 = coords.min(axis=0)
    x1, y1 = coords.max(axis=0) + 1
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
    T = T.reshape((-1, kx*(R-1)))
    print(S.shape, T.shape)

    # __                     __     __                     __
    # | T0,0     T1,0     ... |     | S0       S0       ... |
    # | T0,1     T1,1     ... | = W | S1       S1       ... |
    # |   .        .      ... |     | .        .        ... |
    # | T0,{R-1} T1,{R-1} ... |     | S{kx*ky} S{kx*ky} ... |
    # --                     --     --                     --

if __name__ == '__main__':

    from sigpy import shepp_logan
    from sigpy.mri import birdcage_maps
    # from mr_utils import view
    N = 64
    nc = 2
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
    # view(kspace_u)

    grappa2d(kspace_u, R, acs, kx=3, coil_axis=0, R_axis=1)
