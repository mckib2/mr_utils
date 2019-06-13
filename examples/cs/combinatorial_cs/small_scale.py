'''Try a small scale subset of the larger problem.'''

import numpy as np
import matplotlib.pyplot as plt
from sigpy import shepp_logan
from sigpy.mri.app import TotalVariationRecon

from mr_utils.utils import undersample

class FD(object):
    '''Finite differences transformation.'''

    def __init__(self):
        self.x00 = None
        self.x01 = None

    def forward(self, x0):
        '''Forward transformation.'''
        self.x00 = x0[0, :][None, :]
        self.x01 = x0[1:, 0][:, None]
        return np.diff(np.diff(x0, axis=1), axis=0)

    def inverse(self, x0):
        '''Inverse transformation.'''

        xr = np.concatenate((self.x01, x0), axis=1).cumsum(axis=1)
        xr = np.concatenate((self.x00, xr), axis=0).cumsum(axis=0)
        return xr

if __name__ == '__main__':

    # Sample image
    N = 128
    x = shepp_logan((N, N))

    # FFT/IFFT
    forward_fun = lambda x0: np.fft.fftshift(np.fft.fft2(
        np.fft.fftshift(x0, axes=(1, 2)), axes=(1, 2)), axes=(1, 2))
    inverse_fun = lambda x0: np.fft.ifftshift(np.fft.ifft2(
        np.fft.ifftshift(x0, axes=(1, 2)), axes=(1, 2)), axes=(1, 2))

    # Now we want a set of images to compute T1 from
    T1 = 1.2
    num_ims = 6
    t = np.linspace(0, 3*T1, num_ims+1)[1:]
    t1_relax = 1 - np.exp(-t/T1)
    ims = np.zeros((num_ims, N, N), dtype='complex')
    for ii in range(num_ims):
        ims[ii, ...] = x*t1_relax[ii]
    ims /= np.max(np.abs(ims.flatten()))
    # from mr_utils import view
    # view(ims)
    # plt.plot(t1_relax, '-.')
    # plt.show()

    # # Now undersample using the same mask for each time point
    # kspace_u, masks = undersample(
    #     ims, R=(1, 4, 1), acs=(1, .1, 1),
    #     forward_fun=forward_fun,
    #     inverse_fun=inverse_fun,
    #     ret_kspace=True,
    #     ret_mask=True)

    # Use this for different sampling masks each image:
    kspace_u = np.zeros(ims.shape, dtype='complex')
    masks = np.zeros(ims.shape, dtype=bool)
    for ii in range(num_ims):
        kspace_u[ii, ...], masks[ii, ...] = undersample(
            ims[ii, ...],
            R=(4, 1),
            acs=(.1, 1),
            forward_fun=lambda x0: forward_fun(
                x0[None, ...]).squeeze(),
            inverse_fun=lambda x0: inverse_fun(
                x0[None, ...]).squeeze(),
            ret_kspace=True,
            ret_mask=True)
    # from mr_utils import view
    # view(masks)

    # We might try reconstructing with spatial TV
    recons_TV = np.zeros(kspace_u.shape, dtype=kspace_u.dtype)
    lamda = 2.0
    for ii in range(num_ims):
        mps = np.array([np.ones(kspace_u[ii, ...].shape)])
        recons_TV[ii, ...] = TotalVariationRecon(
            kspace_u[ii, ...], mps, lamda, weights=masks[ii, ...],
            coord=None, show_pbar=True).run()
    recons_TV /= np.max(np.abs(recons_TV.flatten()))
    from mr_utils import view
    view(recons_TV)

    # from mr_utils.cs import proximal_GD
    # recons_TV = np.zeros(kspace_u.shape, dtype=kspace_u.dtype)
    # for ii in range(num_ims):
    #     fd = FD()
    #     recons_TV[ii, ...] = proximal_GD(
    #         kspace_u[ii, ...],
    #         forward_fun=lambda x0: forward_fun(
    #             x0[None, ...])*masks[ii, ...].squeeze(),
    #         inverse_fun=lambda x0: inverse_fun(
    #             x0[None, ...]).squeeze(),
    #         sparsify=fd.forward,
    #         unsparsify=fd.inverse,
    #         reorder_fun=None,
    #         mode='soft',
    #         alpha=.0002,
    #         thresh_sep=True,
    #         selective=None,
    #         x=ims[ii, ...],
    #         ignore_residual=False,
    #         ignore_mse=True,
    #         ignore_ssim=True,
    #         disp=False,
    #         maxiter=200,
    #         strikes=50)
    # recons_TV /= np.max(np.abs(recons_TV.flatten()))

    # Look at an aliased time curve
    xx, yy = int(N*2/3), int(N*1/3)
    px = ims[:, xx, yy]
    px_u = inverse_fun(kspace_u)[:, xx, yy]
    px_TV = recons_TV[:, xx, yy]
    plt.plot(np.abs(px))
    plt.plot(np.abs(px_u), '--')
    plt.plot(np.abs(px_TV), ':')
    plt.show()
