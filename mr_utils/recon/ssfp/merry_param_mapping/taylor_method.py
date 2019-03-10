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
    '''Wrapper for parallelization.'''
    ii, jj = idx[0], idx[1]
    I = np.array([I0[ii, jj] for I0 in Is])
    xopt, _fopt = optimize(
        I.conj().T, TR, dphis, offres_est[ii, jj]/100, 1.2, alpha[ii, jj],
        1000/100, 100/10)
    return(ii, jj, xopt)

def taylor_method(Is, dphis, alpha, TR, mask=None, chunksize=10, disp=False):
    '''Parameter mapping for multiple phase-cycled bSSFP.

    Is -- List of phase-cycled images.
    dphis -- Phase-cycles (in radians).
    alpha -- Flip angle map (in Hz).
    TR -- Repetition time (milliseconds).
    mask -- Locations to compute map estimates.
    chunksize -- Chunk size to use for parallelized loop.
    disp -- Show debugging plots.

    mask=None computes maps for all points.  Note that `Is` must be given as a
    list.
    '''

    # If mask is None, that means we'll do all the points
    if mask is None:
        mask = np.ones(Is[0].shape).astype(bool)

    # Calculate the banding-removed image using the algorithm in the elliptical
    # model paper.

    # My addition: average the GS recon over all sets of 4 we have.  This will
    # have to do while I work on a generalization of the GS recon method to
    # handle >=4 phase-cycles at a time.
    assert isinstance(Is, list), 'Phase-cycles must be provided in a list!'
    assert np.mod(len(Is), 4) == 0, 'We need sets of 4 for GS recon!'
    num_sets = int(len(Is)/4)
    Ms = np.zeros((num_sets,) + Is[0].shape, dtype='complex')
    for ii in range(num_sets):
        Is0 = Is[ii::num_sets]
        Ms[ii, ...] = gs_recon(Is0[0], Is0[1], Is0[2], Is0[3])
    M = np.mean(Ms, axis=0)

    # Display elliptical model image.
    if disp:
        plt.figure()
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

        Is0 = Is[::num_sets]
        plt.figure()
        plt.suptitle('0 PC')
        plt.subplot(2, 2, 1)
        plt.plot(Is0[0].real[row, cols[0]:cols[1]])
        plt.subplot(2, 2, 2)
        plt.plot(Is0[0].imag[row, cols[0]:cols[1]])
        plt.subplot(2, 2, 3)
        plt.plot(np.abs(Is0[0][row, cols[0]:cols[1]]))
        plt.subplot(2, 2, 4)
        plt.plot(np.angle(Is0[0][row, cols[0]:cols[1]]))
        plt.show()

        plt.figure()
        plt.suptitle('180 PC')
        plt.subplot(2, 2, 1)
        plt.plot(Is[4].real[row, cols[0]:cols[1]])
        plt.subplot(2, 2, 2)
        plt.plot(Is[4].imag[row, cols[0]:cols[1]])
        plt.subplot(2, 2, 3)
        plt.plot(np.abs(Is[4][row, cols[0]:cols[1]]))
        plt.subplot(2, 2, 4)
        plt.plot(np.angle(Is[4][row, cols[0]:cols[1]]))
        plt.show()
        # compare to Lauzon paper figure 1

    ## Elliptical fit done here
    offres_est = np.angle(M)
    offres_est = np.unwrap(offres_est, axis=1)
    offres_est[~mask] = 0 #pylint: disable=E1130
    view(offres_est)
    offres_est /= np.pi*TR*1e-3

    t1map = np.zeros(Is[0].shape)
    t2map = np.zeros(Is[0].shape)
    offresmap = np.zeros(Is[0].shape)
    m0map = np.zeros(Is[0].shape)

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
        t1map[ii, jj] = xopt[0]*100
        t2map[ii, jj] = xopt[1]*10
        offresmap[ii, jj] = xopt[2]*100
        m0map[ii, jj] = xopt[3]

    return(t1map, t2map, offresmap, m0map)

if __name__ == '__main__':
    pass
