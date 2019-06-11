'''Try running 7T data.'''

import numpy as np

from mr_utils.test_data import load_test_data
from mr_utils.definitions import ROOT_DIR
from mr_utils.recon.ssfp import gs_recon
from mr_utils import view

if __name__ == '__main__':

    path = 'mr_utils/test_data/examples/coils/'
    filename = 'knee_bssfp_7t.npy'
    load_test_data(path, [filename], do_return=False) # too big

    fullpath = '%s/%s/%s' % (ROOT_DIR, path, filename)
    pcs = np.memmap(
        fullpath, dtype=np.complex64, mode='r',
        shape=(4, 384, 384, 40, 28))

    ax = (1, 2)
    pcs0 = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(
        pcs[..., 10, 0], axes=ax), axes=ax), axes=ax)
    recon = gs_recon(pcs0, pc_axis=0)
    view(recon)
