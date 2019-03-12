'''Self calibrating GROG implementation.

Based on the MATLAB GROG implementation found here:
https://github.com/edibella/Reconstruction
'''

from multiprocessing import Pool
from functools import partial

import numpy as np
from tqdm import tqdm, trange
from scipy.linalg import fractional_matrix_power

def fracpowers(idx, Gx, Gy, dkxs, dkys):
    '''Wrapper function to use during parallelization.

    Parameters
    ==========
    idx : array_like
        Indices of current fractioinal power GRAPPA kernels
    Gx : array_like
        GRAPPA kernel in x
    Gy : array_like
        GRAPPA kernel in y
    dkxs : array_like
        Differential x k-space coordinates
    dkys : array_like
        Differential y k-space coordinates

    Returns
    =======
    ii : array_like
        row indices
    jj : array_like
        col indices
    Gxf : array_like
        Fractional power of GRAPPA kernel in x
    Gyf : array_like
        Fractional power of GRAPPA kernel in y
    '''
    ii, jj = idx[0], idx[1]
    Gxf = fractional_matrix_power(Gx, dkxs[ii, jj])
    Gyf = fractional_matrix_power(Gy, dkys[ii, jj])
    return(ii, jj, Gxf, Gyf)

def grog_interp(kspace, Gx, Gy, traj, cartdims):
    '''Moves radial k-space points onto a cartesian grid via the GROG method.

    Parameters
    ==========
    kspace : array_like
        A 3D (sx, sor, soc) slice of k-space
    Gx : array_like
        The unit horizontal cartesian GRAPPA kernel
    Gy : array_like
        Unit vertical cartesian GRAPPA kernel
    traj : array_like
        k-space trajectory
    cartdims : tuple
        (nrows, ncols), size of Cartesian grid

    Returns
    =======
    array_like
        Interpolated cartesian kspace.
    '''

    sx, nor, noc = kspace.shape[:]
    nrows, ncols = cartdims[0:2]

    kxs = np.real(traj)*nrows
    kys = np.imag(traj)*ncols

    # Pre-allocate kspace_out with an extra row,col
    kspace_out = np.zeros((nrows+1, ncols+1, noc), dtype='complex')
    countMatrix = np.zeros((nrows+1, ncols+1), dtype='int')

    # Find nearest integer coordinates
    kxs_round = np.round(kxs)
    kys_round = np.round(kys)

    # Find distance between kxys and rounded kxys, these will be Gx,Gy powers
    dkxs = kxs_round - kxs
    dkys = kys_round - kys

    # Compute fractional matrix powers - this part takes a long time
    # Let's parallelize this since it doesn't matter what order we do it in and
    # elements don't depend on previous elements. Notice that order is not
    # preserved here -- instead we just keep track of indices at each compute.
    fracpowers_partial = partial(
        fracpowers, Gx=Gx, Gy=Gy, dkxs=dkxs, dkys=dkys)
    tot = len(list(np.ndindex((sx, nor))))
    with Pool() as pool:
        res = list(tqdm(pool.imap_unordered(
            fracpowers_partial, np.ndindex((sx, nor)), chunksize=100),
                        total=tot, leave=False,
                        desc='Frac mat pwr'))

    # Now we need to stick the results where they belong and get a density
    # estimation
    for r in res:
        # Look up the indices associated with this result
        ii, jj = r[0], r[1]

        # Find matrix indices corresponding to kspace coordinates while we're
        # at it:
        xx = int(kxs_round[ii, jj] + nrows/2)
        yy = int(kys_round[ii, jj] + ncols/2)

        # Load result into output matrix and bump the counter
        kspace_out[xx, yy, :] += np.linalg.multi_dot(
            [r[2], r[3], kspace[ii, jj, :]])
        countMatrix[xx, yy] += 1


    # Lastly, use point-wise division of kspace_out by weightMatrix to average
    nonZeroCount = countMatrix > 0
    countMatrixMasked = countMatrix[nonZeroCount]
    kspace_out[nonZeroCount] /= np.tile(countMatrixMasked[:, None], noc)

    # Regridding results in +1 size increase so drop first row,col arbitrarily
    return kspace_out[1:, 1:]

def scgrog(kspace, traj, Gx, Gy, cartdims=None):
    '''Self calibrating GROG interpolation.

    Parameters
    ==========
    kspace : array_like
        A 4D (sx, sor, nof, soc) matrix of complex k-space data
    traj : array_like
        k-space trajectory
    Gx : array_like
        The unit horizontal cartesian GRAPPA kernel
    Gy : array_like
        Unit vertical cartesian GRAPPA kernel
    cartdims : tuple
         Size of Cartesian grid.

    Returns
    =======
    kspace_cart : array_like
        Cartesian gridded k-space.
    mask : array_like
        Boolean mask where kspace is nonzero.

    Notes
    =====
    If cartdims=None, we'll guess the Cartesian dimensions are
    (kspace.shape[0], kspace.shape[0], kspace.shape[2], kspace.shape[3]).
    '''

    # If the user didn't give us the desired cartesian dimensions, guess
    if cartdims is None:
        cartdims = (kspace.shape[0], kspace.shape[0], kspace.shape[2],
                    kspace.shape[3])

    # Permute time to end of 4D data for convenience
    if kspace.ndim == 4:
        kspace = np.transpose(kspace, (0, 1, 3, 2))
        tmp = list(cartdims)
        tmp[2], tmp[3] = tmp[3], tmp[2]
        cartdims = tuple(tmp)

    # Interpolate frame-by-frame
    kspace_cart = np.zeros(cartdims, dtype='complex')
    for ii in trange(kspace.shape[-1], desc='Frame', leave=False):
        time_frame = kspace[:, :, :, ii]
        traj_frame = traj[:, :, ii]
        kspace_cart[:, :, :, ii] = grog_interp(
            time_frame, Gx, Gy, traj_frame, cartdims)

    # Permute back if needed
    if kspace_cart.ndim == 4:
        kspace_cart = np.transpose(kspace_cart, (0, 1, 3, 2))

    # Create mask
    mask = (np.abs(kspace_cart) > 0)

    return(kspace_cart, mask)

if __name__ == '__main__':
    pass
