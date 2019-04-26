'''Do the temporal 1d reconstruction pixel by pixel.

We want to do temporally constrained compressed sensing, so we'll
do the dumb thing and do each time curve individually because that
can be handled by the tools I currently have.
'''

import numpy as np
from tqdm import trange

from mr_utils.test_data import load_test_data
from mr_utils.cs import proximal_GD
from mr_utils.cs.models import UFT
from mr_utils.sim.traj import radial
from mr_utils.utils import Sparsify
from mr_utils import view

# Decide how we'll be selective in our updates
def select_n(x_hat, update, cur_iter, tot_iter):
    '''Return indices of n largest updates each iteration.'''
    percent_to_keep = cur_iter/tot_iter
    num_to_keep = int(percent_to_keep*x_hat.size)
    return np.unravel_index(np.argpartition(
        np.abs(x_hat - update).flatten(),
        -num_to_keep)[-num_to_keep:], x_hat.shape)

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

    # Undersample to N rays
    num_spokes = 24
    samp0 = np.zeros((sx, sy, st))
    offsets = np.random.randint(0, high=st, size=st)
    for ii in trange(st, leave=False, desc='Making sampling mask'):
        samp0[..., ii] = radial(
            (sx, sy), num_spokes, offset=offsets[ii], extend=False)
    # view(samp0)

    # Set up the recon
    ax = (0, 1)
    uft = UFT(samp0, axes=ax, scale=True)
    forward = uft.forward_ortho
    inverse = uft.inverse_ortho
    sl0 = 1 # which of the two slices to use
    kspace_u = forward(imspace_true[..., sl0])
    imspace_u = inverse(kspace_u)


    # Try to do proximal gradient descent using finite differences
    y = kspace_u
    x = imspace_true[..., sl0]
    S = Sparsify(axis=-1)
    sparsify = S.forward_fd
    unsparsify = S.inverse_fd
    # sparsify = S.forward_dct
    # unsparsify = S.inverse_dct
    # sparsify = S.forward_wvlt
    # unsparsify = S.inverse_wvlt
    alpha = .002
    maxiter = 500
    selective = lambda x_hat, update, cur_iter: select_n(
        x_hat, update, cur_iter, tot_iter=maxiter)
    ignore_residual = True
    thresh_sep = True
    disp = True

    # Do recon no ordering
    recon_fd = proximal_GD(
        y,
        forward_fun=forward,
        inverse_fun=inverse,
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=None,
        mode='soft',
        alpha=alpha,
        thresh_sep=thresh_sep,
        selective=selective,
        x=x,
        ignore_residual=ignore_residual,
        disp=disp,
        maxiter=maxiter)

    # Find true ordering
    prior = x.copy()
    idx = np.arange(prior.size).reshape(prior.shape)
    ord_r = np.argsort(prior.real, axis=-1)[..., ::-1]
    ord_r = np.take_along_axis(idx, ord_r, axis=-1).flatten() # pylint: disable=E1101

    ord_i = np.argsort(prior.imag, axis=-1)[..., ::-1]
    ord_i = np.take_along_axis(idx, ord_i, axis=-1).flatten() # pylint: disable=E1101

    # Do ordering
    order = ord_r + 1j*ord_i
    recon_fd_mono = proximal_GD(
        y,
        forward_fun=forward,
        inverse_fun=inverse,
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=lambda xx: order,
        mode='soft',
        alpha=alpha,
        thresh_sep=thresh_sep,
        selective=selective,
        x=x,
        ignore_residual=ignore_residual,
        disp=disp,
        maxiter=maxiter)

    import matplotlib.pyplot as plt
    plt.plot(np.abs(x[ctr[0], ctr[1], :]))
    plt.plot(np.abs(recon_fd[ctr[0], ctr[1], :]))
    plt.plot(np.abs(recon_fd_mono[ctr[0], ctr[1], :]))
    plt.show()

    # Take a look
    ims = [
        inverse(y),
        imspace_nufft16[..., sl0],
        recon_fd,
        recon_fd_mono,
        x,
        np.abs(x - recon_fd),
        np.abs(x - recon_fd_mono)
    ]
    ims0 = list()
    for im in ims:
        norm = np.linalg.norm(im)
        im /= norm
        ims0.append(im)
    ims = np.array(ims0)
    view(ims)
