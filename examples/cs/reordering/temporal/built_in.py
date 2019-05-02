'''Try using out of the box denoising approaches.'''

import numpy as np
from tqdm import trange, tqdm
import prox_tv as ptv # tv2_1d, tv1_1d

from mr_utils.test_data import load_test_data
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils import view

if __name__ == '__main__':

    # Load in STCR recon
    sl0 = 0 # which of the two slices to use
    path = ('mr_utils/test_data/examples/cs/temporal/')
    imspace_true = load_test_data(
        path, ['stcr_recon'])[0][..., sl0]
    sx, sy, st = imspace_true.shape[:]

    # Undersampling pattern
    samp0 = np.zeros((sx, sy, st))
    desc = 'Making sampling mask'
    num_spokes = 16
    offsets = np.random.randint(0, high=st, size=st)
    for ii in trange(st, leave=False, desc=desc):
        samp0[..., ii] = radial(
            (sx, sy), num_spokes, offset=offsets[ii],
            extend=True, skinny=False)
    # view(samp0)

    # Set up the recon
    x = imspace_true.copy()
    ax = (0, 1)
    uft = UFT(samp0, axes=ax, scale=True)
    forward = uft.forward_ortho
    inverse = uft.inverse_ortho
    y = forward(x)
    # view(y, log=True)
    imspace_u = inverse(y)

    # from mr_utils.cs import SpatioTemporalTVSB
    # recon, err = SpatioTemporalTVSB(
    #     samp0, y, betaxy=1/4, betat=1, mu=1, lam=1, gamma=1/2,
    #     nInner=1, niter=3, x=x)
    # view(recon)


    w = 50
    recon_l1 = ptv.tvgen(
        np.abs(imspace_u), np.array([w]), [3], np.array([1]))
    recon_l2 = ptv.tvgen(
        np.abs(imspace_u), np.array([w]), [3], np.array([2]))

    recon_sort = np.zeros_like(imspace_u)
    for idx in tqdm(np.ndindex((sx, sy)), total=sx*sy, leave=False):
        ii, jj = idx[:]

        # TODO:
        # Mask out small ROIs to do run ordinator in

        # Sorting doesn't suppress motion!
        sord = np.argsort(np.abs(imspace_true[ii, jj, :]))
        recon_sort[ii, jj, sord] = ptv.tv1_1d( #pylint: disable=E1137
            np.abs(imspace_u[ii, jj, sord]), w)

    # Take a look
    ims = [
        imspace_u,
        # recon,
        recon_l1,
        recon_l2,
        recon_sort,
        imspace_true,
        # np.abs(imspace_true - recon0),
        # np.abs(imspace_true - recon1)
    ]
    ims0 = list()
    for im in ims:
        norm = np.linalg.norm(im)
        im /= norm
        ims0.append(im)
    ims = np.array(ims0)
    view(ims)
