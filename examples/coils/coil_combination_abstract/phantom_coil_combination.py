'''Same thing as numerical, but with phantom data.'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_li
from skimage.measure import compare_mse

from mr_utils.test_data import load_test_data
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import sos
from mr_utils import view

from examples.coils.coil_combination_abstract.coil_combine_funs import get_coil_combine_funs

if __name__ == '__main__':

    # Load in phantom data, shape: (512, 256, 4, 16)
    path = 'mr_utils/test_data/examples/coils/'
    imspace, kspace = load_test_data(path, ['imspace', 'kspace'])
    print(imspace.shape)
    nx, ny, nc, npcs = imspace.shape[:]
    trim = int(nx/4)
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)

    # Get mask
    ngs = int(npcs/4)
    tmp = np.zeros((nx, ny, nc, ngs), dtype='complex')
    for coil in range(nc):
        for ii in range(ngs):
            tmp[..., coil, ii] = gs_recon(
                imspace[..., coil, ii::4], pc_axis=-1)
    im_true = np.mean(tmp, axis=-1)
    im_true = sos(im_true, axes=-1)
    thresh = threshold_li(im_true)
    mask = im_true > thresh
    # view(im_true)
    # view(mask)

    # Define coil combination functions
    ccs, cc_list = get_coil_combine_funs(np.min([nx, ny]), v='')

    # Do coil combine then ESM
    res = np.zeros((len(ccs), nx, ny), dtype='complex')
    err_cc_then_gs = np.zeros(len(ccs))
    for fun, cc in enumerate(ccs):

        tmp = np.zeros((nx, ny, ngs), dtype='complex')
        idx = list(range(npcs))[::4]
        for ii, jj in enumerate(idx):
            tmp[..., ii] = cc(imspace[..., jj].transpose((2, 0, 1)))
        res[fun, ...] = gs_recon(tmp, pc_axis=-1)*mask
        # view(res[fun, ...])

        # view(np.stack((im_true, res[fun, ...])))
        err_cc_then_gs[fun] = compare_mse(
            im_true,
            np.abs(np.nan_to_num(res[fun, ...])))
    view(np.concatenate(
        (res[:, trim:-trim, ...], im_true[trim:-trim, :][None, ...]),
        axis=0))
    # plt.bar(list(range(len(ccs))), err_cc_then_gs)
    # plt.show()

    # Do ESM then coil combine
    res = np.zeros((len(ccs), nx, ny), dtype='complex')
    err_gs_then_cc = np.zeros(len(ccs))
    for fun, cc in enumerate(ccs):

        tmp = np.zeros((nc, nx, ny), dtype='complex')
        for ii in range(nc):
            tmp[ii, ...] = gs_recon(
                imspace[..., ii, ::4], pc_axis=-1)

        res[fun, ...] = cc(tmp)*mask
        # view(res[coil, fun, ...])

        # err_gs_then_cc[fun] = compare_mse(
        #     np.abs(im_true),
        #     np.abs(np.nan_to_num(res[fun, ...])))

    view(np.concatenate(
        (res[:, trim:-trim, ...], im_true[trim:-trim, :][None, ...]),
        axis=0))
