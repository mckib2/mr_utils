'''Python port of Merry's bSSFP parameter mapping code.

This is an alternative to PLANET.
'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from mr_utils.recon.ssfp import gs_recon
from mr_utils.recon.ssfp.merry_param_mapping.optimize import optimize
from mr_utils import view

def taylor_method(Is, dphis, alpha, TR, mask=None, disp=False):
    '''Parameter mapping for multiple phase-cycled bSSFP.

    Is -- List of phase-cycled images.
    dphis -- Phase-cycles (in radians).
    alpha -- Flip angle map.
    TR -- Repetition time.
    mask -- Locations to compute map estimates.
    disp -- Show debugging plots.

    mask=None computes maps for all points.
    '''

    if mask is None:
        mask = np.ones(Is[0].shape).astype(bool)

    # Calculate the banding-removed image using the algorithm in the elliptical
    # model paper.

    # Can we average sets if we have them?
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
    offres_est /= -np.pi*TR*1e-3 # I still have to add this negative in here...

    t1map = np.zeros(Is[0].shape)
    t2map = np.zeros(Is[0].shape)
    offresmap = np.zeros(Is[0].shape)
    m0map = np.zeros(Is[0].shape)

    # For each pixel...
    tot = np.sum(mask.flatten())
    for idx in tqdm(
            np.argwhere(mask), total=tot, desc='Param Mapping', leave=False):
        ii, jj = idx[0], idx[1]
        I = np.array([I0[ii, jj] for I0 in Is])
        xopt, _fopt = optimize(
            I.conj().T, TR, dphis, offres_est[ii, jj]/100, 1.2, alpha[ii, jj],
            1000/100, 100/10)
        t1map[ii, jj] = xopt[0]*100
        t2map[ii, jj] = xopt[1]*10
        offresmap[ii, jj] = xopt[2]*100
        m0map[ii, jj] = xopt[3]

    return(t1map, t2map, offresmap, m0map)


if __name__ == '__main__':
    pass
