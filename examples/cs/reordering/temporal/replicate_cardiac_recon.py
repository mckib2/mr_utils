'''Replicate STCR recon.'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from sigpy.fourier import nufft_adjoint

from mr_utils.test_data import load_test_data

def get_k_coor(sx, theta, kCenter):
    '''Get kspace coordinates.'''
    xcoor = np.arange(sx) - kCenter
    ycoor = xcoor.copy()
    xcoor = xcoor[:, None, None]*np.cos(np.tile(theta, (sx, 1, 1)))
    ycoor = ycoor[:, None, None]*np.sin(np.tile(theta, (sx, 1, 1)))
    return(xcoor, ycoor)

if __name__ == '__main__':

    # Load in rays
    path = ('mr_utils/test_data/examples/cs/temporal/')
    rays = load_test_data(path, ['raw_rays'])[0]
    print(rays.shape)
    sx, nor, ncoil, nof, nslice = rays.shape[:]

    # Get sampling angle
    theta0, dtheta = np.linspace(
        0, np.pi, nor, endpoint=True, retstep=True)
    dtheta /= 4
    theta = theta0.copy()
    for ii in range(1, 4):
        theta = np.concatenate((theta, theta0 + ii*dtheta))
    theta = np.tile(theta, int(np.ceil(nof/4)))
    theta = theta[:nor*nof]
    theta = theta.reshape((1, nor, nof))

    # Get k-space coordinates for samples in each frame
    kx, ky = get_k_coor(sx, theta, sx/2-1)

    # plt.scatter(kx[..., 0], ky[..., 0], np.abs(rays[..., 0, 0, 0]))
    # plt.axis('square')
    # plt.show()

    # Do NUFFT recon
    regrid = np.zeros((sx, sx, ncoil, nof), dtype=rays.dtype)
    for ii in trange(nof, leave=False):
        coord = np.concatenate((
            kx[..., ii][..., None],
            ky[..., ii][..., None]), axis=-1)
        for cc in range(ncoil):
            r = rays[..., cc, ii, 0]
            regrid[..., cc, ii] = nufft_adjoint(
                r, coord, oshape=(sx, sx), oversamp=2.0, width=4.0,
                n=128)

    from mr_utils import view
    view(regrid)

    # input0 = np.moveaxis(rays[..., 0, :, 0], -1, 0)
    # oshape = (nof, sx, sx)
    # width = 1.25
    # n = 256
    # oversamp = 2.0
    #
    # from sigpy import backend, interp, util
    # from sigpy.fourier import (
    #     _get_oversamp_shape, _scale_coord,
    #      _get_kaiser_bessel_kernel)
    #
    # device = backend.get_device(input0)
    # ndim = coord.shape[-1]
    # beta = np.pi*(((width/oversamp)*(oversamp - 0.5))**2 - 0.8)**0.5
    # oshape = list(oshape)
    #
    # os_shape = _get_oversamp_shape(oshape, ndim, oversamp)
    #
    # with device:
    #     # Gridding
    #     coord = _scale_coord(backend.to_device(
    #         coord, device), oshape, oversamp)
    #     kernel = _get_kaiser_bessel_kernel(
    #         n, width, beta, coord.dtype, device)
    #     output = interp.gridding(
    #         input, os_shape, width, kernel, coord)
    #
    #     # # IFFT
    #     # output = ifft(output, axes=range(-ndim, 0), norm=None)
    #
    #     # Crop
    #     output = util.resize(output, oshape)
    #     output *= util.prod(os_shape[-ndim:])/util.prod(
    #         oshape[-ndim:])**0.5
    #
    #     # # Apodize
    #     # _apodize(output, ndim, oversamp, width, beta)
    # regrid = output
