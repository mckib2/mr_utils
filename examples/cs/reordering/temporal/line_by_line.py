'''Do the temporal 1d reconstruction pixel by pixel.

We want to do temporally constrained compressed sensing, so we'll
do the dumb thing and do each time curve individually because that
can be handled by the tools I currently have.
'''

import numpy as np

from mr_utils.test_data import load_test_data
from mr_utils.cs import proximal_GD
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.utils import Sparsify
from mr_utils import view

if __name__ == '__main__':

    # Load in STCR recon
    path = ('mr_utils/test_data/examples/cs/temporal/')
    imspace_true = load_test_data(path, ['stcr_recon'])[0]

    # Load in 16 nufft recon
    imspace_nufft16 = load_test_data(path, ['nufft16rays'])[0]
    # view(imspace)

    # We want to mask out the areas we want, start with a simple
    # circle
    sx, sy, st, sl = imspace_true.shape[:]
    x = np.linspace(0, sx, sx)
    y = np.linspace(0, sy, sy)
    X, Y = np.meshgrid(x, y)
    radius = 9
    ctr = (128, 130)
    mask = (X - ctr[0])**2 + (Y - ctr[1])**2 < radius**2
    # view(mask)
    # mask0 = np.tile(mask, (st, 1, 1)).transpose((1, 2, 0))
    # view(imspace[..., 0]*mask0)

    # Undersample to 16 rays
    sl0 = 1
    ax = (0, 1)
    num_spokes = 16
    samp = radial((sx, sy), num_spokes, extend=False)
    samp0 = np.tile(samp, (st, 1, 1)).transpose((1, 2, 0))
    uft = UFT(samp0, axes=ax)
    # kspace = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(
    #     imspace_true, axes=ax), axes=ax), axes=ax)
    kspace_u = uft.forward_ortho(imspace_true[..., sl0])
    # imspace_u = uft.inverse_ortho(kspace_u)
    # view(imspace_u)

    # Try to do proximal gradient descent using finite differences
    y = kspace_u
    x = imspace_true[..., sl0]
    S = Sparsify(x, axis=-1)
    sparsify = S.forward_fd
    unsparsify = S.inverse_fd
    # sparsify = S.forward_dct
    # unsparsify = S.inverse_dct
    alpha = .5
    maxiter = 1
    ignore_residual = False
    disp = True

    recon_fd = proximal_GD(
        y,
        forward_fun=uft.forward_ortho,
        inverse_fun=uft.inverse_ortho,
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=None,
        mode='soft',
        alpha=alpha,
        thresh_sep=True,
        selective=None,
        x=x,
        ignore_residual=ignore_residual,
        disp=disp,
        maxiter=maxiter)

    prior = x.copy()
    ord_r = np.argsort(prior.real, axis=-1) # [..., ::-1]
    idx = np.arange(ord_r.size).astype(int).reshape(ord_r.shape)
    ord_r = np.take_along_axis(idx, ord_r, -1).flatten() # pylint: disable=E1101
    ord_i = np.argsort(prior.imag, axis=-1) # [..., ::-1]
    ord_i = np.take_along_axis(idx, ord_i, -1).flatten() # pylint: disable=E1101
    order = ord_r + 1j*ord_i
    recon_fd_mono = proximal_GD(
        y,
        forward_fun=uft.forward_ortho,
        inverse_fun=uft.inverse_ortho,
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=lambda xx: order,
        mode='soft',
        alpha=alpha,
        thresh_sep=True,
        selective=None,
        x=x,
        ignore_residual=ignore_residual,
        disp=disp,
        maxiter=maxiter)
    # This does a better job of suppressing motion.  Desirable?

    # Take a look
    ims = [
        uft.inverse_ortho(y),
        imspace_nufft16[..., sl0],
        recon_fd,
        recon_fd_mono,
        x
    ]
    ims0 = list()
    for im in ims:
        norm = np.linalg.norm(im)
        im /= norm
        ims0.append(im)
    ims = np.array(ims0)
    view(ims)
