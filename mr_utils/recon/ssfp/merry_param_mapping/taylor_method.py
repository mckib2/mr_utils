'''Python port of Merry's bSSFP parameter mapping code.

This is an alternative to PLANET.
'''

from multiprocessing import Pool
from functools import partial

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from mr_utils.recon.ssfp import gs_recon
from mr_utils.recon.ssfp.merry_param_mapping.optimize import optimize
from mr_utils import view

def optim_wrapper(idx, Is, TR, dphis, offres_est, alpha):
    '''Wrapper for parallelization.

    Parameters
    ==========
    idx : array_like
        Indices of current pixels, must be provided as parallelization is non-
        sequential
    Is : array_like
        Array of phase-cycled images, (dphi, x, y).
    TR : float
        Repetition time (in sec).
    dphis : array_like
        Phase-cycles (in radians).
    offres_est : array_like
        Off-resonance map estimation (in Hz).
    alpha : array_like
        Flip angle map (in rad).

    Returns
    =======
    ii : int
        Row index
    jj : int
        Column index
    xopt : array_like
        Optimized parameters: [T1, T2, offres, M0]
    '''
    ii, jj = idx[0], idx[1]
    I = Is[:, ii, jj]
    xopt, _fopt = optimize(
        I, TR, dphis, offres_est[ii, jj], 1.2, alpha[ii, jj], 1, .1)
    return(ii, jj, xopt)

def taylor_method(Is, dphis, alpha, TR, mask=None, chunksize=10,
                  unwrap_fun=None, disp=False):
    '''Parameter mapping for multiple phase-cycled bSSFP.

    Parameters
    ==========
    Is : array_like
        Array of phase-cycled images, (dphi, x, y).
    dphis : array_like
        Phase-cycles (in radians).
    alpha : array_like
        Flip angle map (in rad).
    TR : float
        Repetition time (in sec).
    mask : array_like, optional
        Locations to compute map estimates.
    chunksize : int, optional
        Chunk size to use for parallelized loop.
    unwrap_fun : callable
        Function to do 2d phase unwrapping.  If None, will use
        skimage.restoration.unwrap_phase().
    disp : bool, optional
        Show debugging plots.

    Returns
    =======
    t1map : array_like
        T1 map estimation (in sec)
    t2map : array_like
        T2 map estimation (in sec)
    offresmap : array_like
        Off-resonance map estimation (in Hz)
    m0map : array_like
        Proton density map estimation

    Raises
    ======
    AssertionError
        If number of phase-cycles is not divisible by 4.

    Notes
    =====
    mask=None computes maps for all points.  Note that `Is` must be given as a
    list.
    '''

    # If mask is None, that means we'll do all the points
    if mask is None:
        mask = np.ones(Is[0].shape).astype(bool)

    # If unwrap is None, then use default:
    if unwrap_fun is None:
        from skimage.restoration import unwrap_phase
        unwrap_fun = lambda x: unwrap_phase(x)

    # Calculate the banding-removed image using the algorithm in the elliptical
    # model paper.

    # My addition: average the GS recon over all sets of 4 we have.  This will
    # have to do while I work on a generalization of the GS recon method to
    # handle >=4 phase-cycles at a time.
    assert np.mod(len(Is), 4) == 0, 'We need sets of 4 for GS recon!'
    num_sets = int(len(Is)/4)
    Ms = np.zeros((num_sets,) + Is[0].shape, dtype='complex')
    for ii in range(num_sets):
        Ms[ii, ...] = gs_recon(Is[ii::num_sets, ...])
    M = np.mean(Ms, axis=0)

    # Display elliptical model image.
    if disp:
        plt.imshow(np.abs(M))
        plt.title('Eliptical Model - Banding Removed')
        plt.show()

        # These plots look fishy -- they changed when I moved from Merry's
        # SSFPFit function to my ssfp simulation function.  Need to look at
        # MATLAB output to see who's right and/or what's going on.

        # Choose a row in the mask and show 0, 180 phase cycle lines
        idx = np.argwhere(mask)
        idx = idx[np.random.choice(np.arange(idx.shape[0])), :]
        row, _col = idx[0], idx[1]
        col = np.argwhere(mask)[row, :]
        cols = (np.min(col), np.max(col))

        Is0 = Is[::num_sets, ...]
        plt.suptitle('0 PC')
        plt.subplot(2, 2, 1)
        plt.plot(Is0[0, row, cols[0]:cols[1]].real)
        plt.subplot(2, 2, 2)
        plt.plot(Is0[0, row, cols[0]:cols[1]].imag)
        plt.subplot(2, 2, 3)
        plt.plot(np.abs(Is0[0, row, cols[0]:cols[1]]))
        plt.subplot(2, 2, 4)
        plt.plot(np.angle(Is0[0, row, cols[0]:cols[1]]))
        plt.show()

        plt.suptitle('180 PC')
        plt.subplot(2, 2, 1)
        plt.plot(Is[4, row, cols[0]:cols[1]].real)
        plt.subplot(2, 2, 2)
        plt.plot(Is[4, row, cols[0]:cols[1]].imag)
        plt.subplot(2, 2, 3)
        plt.plot(np.abs(Is[4, row, cols[0]:cols[1]]))
        plt.subplot(2, 2, 4)
        plt.plot(np.angle(Is[4, row, cols[0]:cols[1]]))
        plt.show()
        # compare to Lauzon paper figure 1

    ## Elliptical fit done here
    offres_est = np.angle(M)
    m_offres_est = np.ma.array(offres_est, mask=mask & 0)
    offres_est = unwrap_fun(m_offres_est)*mask
    offres_est /= -1*np.pi*TR # -1 is for sign of phi in ssfp sim
    view(offres_est)

    sh = Is.shape[1:]
    t1map = np.zeros(sh)
    t2map = np.zeros(sh)
    offresmap = np.zeros(sh)
    m0map = np.zeros(sh)

    # Since we have to do it for each pixel and all calculations are
    # independent, we can parallelize this sucker!  Use imap_unordered to to
    # update tqdm progress bar more regularly and use less memory over time.
    tot = np.sum(mask.flatten())
    optim = partial(optim_wrapper, Is=Is, TR=TR, dphis=dphis,
                    offres_est=offres_est, alpha=alpha)
    with Pool() as pool:
        res = list(tqdm(pool.imap_unordered(
            optim, np.argwhere(mask), chunksize=int(chunksize)), total=tot,
                        leave=False, desc='Param mapping'))

    # The answers are then unpacked (not garanteed to be in the right order)
    for ii, jj, xopt in res:
        t1map[ii, jj] = xopt[0]
        t2map[ii, jj] = xopt[1]
        offresmap[ii, jj] = xopt[2]
        m0map[ii, jj] = xopt[3]

    return(t1map, t2map, offresmap, m0map)

if __name__ == '__main__':
    pass
