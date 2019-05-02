'''Try using out of the box denoising approaches.'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange, tqdm
import prox_tv as ptv # tv2_1d, tv1_1d

from mr_utils.test_data import load_test_data
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.cs import ordinator1d, relaxed_ordinator
from mr_utils.utils import Sparsify
from mr_utils import view

if __name__ == '__main__':

    # Load in STCR recon
    sl0 = 0 # which of the two slices to use
    skip = 11 # skip beginning to reduce computational burden
    slash = 25 # skip end ""
    path = ('mr_utils/test_data/examples/cs/temporal/')
    imspace_true = load_test_data(
        path, ['stcr_recon'])[0][..., skip:-slash, sl0]
    sx, sy, st = imspace_true.shape[:]
    # view(imspace_true)

    # We want to mask out the areas we want, start with a simple
    # circle
    xx = np.linspace(0, sx, sx)
    yy = np.linspace(0, sy, sy)
    X, Y = np.meshgrid(xx, yy)
    radius = 9
    ctr = (128, 130)
    roi = (X - ctr[0])**2 + (Y - ctr[1])**2 < radius**2
    roi0 = np.tile(roi, (st, 1, 1)).transpose((1, 2, 0))
    print('%d curves in roi' % int(np.sum(roi.flatten())))
    # view(roi)
    S = Sparsify()
    # view(S.forward_dct(imspace_true[ctr[0], ctr[1], :]))
    # view(imspace_true*roi0)

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
    roi_cnt = 0
    for idx in tqdm(np.ndindex((sx, sy)), total=sx*sy, leave=False):
        ii, jj = idx[:]

        # TODO:
        # Mask out small ROIs to do run ordinator in
        if roi[ii, jj]:
            # sord = ordinator1d(
            #     np.abs(imspace_true[ii, jj, :]), k=10,
            #     forward=S.forward_wvlt, inverse=S.inverse_wvlt,
            #     chunksize=10, pdf=None, pdf_metric=None,
            #     sparse_metric=None, disp=False)
            sord = relaxed_ordinator(
                np.abs(imspace_true[ii, jj, :]), lam=.05, k=10,
                unsparsify=S.inverse_wvlt, norm=False, warm=False,
                transform_shape=None, disp=False)
            roi_cnt += 1
            tqdm.write('ROI counter: %d' % roi_cnt)
        else:
            # Sorting doesn't suppress motion!
            sord = np.argsort(np.abs(imspace_true[ii, jj, :]))

        recon_sort[ii, jj, sord] = ptv.tv1_1d( #pylint: disable=E1137
            np.abs(imspace_u[ii, jj, sord]), w)

    plt.plot(np.abs(imspace_true[ctr[0], ctr[1], :]))
    plt.plot(np.abs(recon_sort[ctr[0], ctr[1], :]))
    plt.plot(np.abs(recon_l1[ctr[0], ctr[1], :]))
    plt.show()

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
