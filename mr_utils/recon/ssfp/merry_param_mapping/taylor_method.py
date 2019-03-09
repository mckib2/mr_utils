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
        # MATLAB output to see who's right and/or what's going on.  Probably
        # related to the fact that ssfp() is adding a bSSFP phase that's 180
        # degrees wrong, see offresonance map estimation below for discussion.
        # plt.figure()
        # plt.title('0 PC')
        # plt.subplot(2, 2, 1)
        # plt.plot(Is[0].real[30, 29:228])
        # plt.subplot(2, 2, 2)
        # plt.plot(Is[0].imag[30, 29:228])
        # plt.subplot(2, 2, 3)
        # plt.plot(np.abs(Is[0][30, 29:228]))
        # plt.subplot(2, 2, 4)
        # plt.plot(np.angle(Is[0][30, 29:228]))
        # plt.show()
        #
        # plt.figure()
        # plt.title('180 PC')
        # plt.subplot(2, 2, 1)
        # plt.plot(Is[4].real[30, 29:228])
        # plt.subplot(2, 2, 2)
        # plt.plot(Is[4].imag[30, 29:228])
        # plt.subplot(2, 2, 3)
        # plt.plot(np.abs(Is[4][30, 29:228]))
        # plt.subplot(2, 2, 4)
        # plt.plot(np.angle(Is[4][30, 29:228]))
        # plt.show()
        # # compare to Lauzon paper figure 1

    ## Elliptical fit done here
    offres_est = np.angle(M)
    offres_est = np.unwrap(offres_est, axis=1)
    offres_est[~mask] = 0 #pylint: disable=E1130
    view(offres_est)
    offres_est /= -np.pi*TR*1e-3

    # TODO:
    # Notice the negative factor in the above offresonance estimate.  This is
    # because the bSSFP phase factor being added by ssfp() is 180 degrees off
    # from where it should be.  Until this gets fixed, we need this negative
    # sign.

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
