'''Get indices for STR recon.'''

import numpy as np
from tqdm import tqdm

from mr_utils.load_data import load_mat
from mr_utils.cs import relaxed_ordinator
from mr_utils.utils import Sparsify

if __name__ == '__main__':

    # Load data
    x = load_mat('/home/nicholas/Downloads/Temporal_reordering/prior.mat',
                 key='prior')
    print(x.shape)

    rpi = np.zeros(x.shape, dtype=int)
    ipi = np.zeros(x.shape, dtype=int)
    for idx in tqdm(np.ndindex(x.shape[:2]), leave=False):
        ii, jj = idx[0], idx[1]

        xr = x[ii, jj, :].real/np.max(np.abs(x[ii, jj, :].real))
        xi = x[ii, jj, :].imag/np.max(np.abs(x[ii, jj, :].imag))
        Sr = Sparsify(xr)
        Si = Sparsify(xi)

        rpi[ii, jj, :] = relaxed_ordinator(
            xr, lam=.08, k=10, unsparsify=Sr.inverse_fd, transform_shape=(xr.size-1,))
        ipi[ii, jj, :] = relaxed_ordinator(
            xi, lam=0.1, k=13, unsparsify=Si.inverse_fd, transform_shape=(xi.size-1,))

    np.save('rpi.npy', rpi)
    np.save('ipy.npy', ipi)
