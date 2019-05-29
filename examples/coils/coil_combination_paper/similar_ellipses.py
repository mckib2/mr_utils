'''Estimate ellipse points from similar ellipses.

Notes
-----
This would be used to get better estimates of ellipses for each coil
image, as the contrast would still be by reference coil.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

from mr_utils.sim.ssfp import ssfp

def plot_ellipse(I, fmt='-', label=''):
    '''Plot closed ellipse in complex plane.'''
    x, y = I.real, I.imag
    plt.plot(
        np.concatenate((x, [x[0]])),
        np.concatenate((y, [y[0]])), fmt, label=label)

if __name__ == '__main__':

    T1 = 1.2
    T2 = .03
    TR = 3e-3
    alpha = np.deg2rad(7)
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    M0 = 1
    df = 1/(2*TR)
    ncoils = 5
    noise_std = 0.002

    # Simulate coil ellipses
    I = np.zeros((ncoils, npcs), dtype='complex')
    rfs = np.linspace(0, np.pi, ncoils, endpoint=False)
    mags = np.linspace(.2, 1, ncoils)
    for cc in range(ncoils):
        I[cc, :] = mags[cc]*ssfp(
            T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0,
            phi_rf=rfs[cc])
    #     plot_ellipse(I[cc, :], '.-')
    # plt.axis('square')
    # plt.show()

    # Add some juicy noise
    I_true = I.copy()
    if noise_std > 0:
        n_r = np.random.normal(0, noise_std/2, I.shape)
        n_i = np.random.normal(0, noise_std/2, I.shape)
        n = n_r + 1j*n_i
        I += n

    # Get distances between each vertex of each ellipse
    D = np.zeros((ncoils, npcs, npcs))
    for cc in range(ncoils):
        X = np.concatenate((
            I[cc, :][:, None].real, I[cc, :][:, None].imag), axis=1)
        Y = np.concatenate((
            I[cc, :][:, None].real, I[cc, :][:, None].imag), axis=1)
        D[cc, ...] = cdist(X, Y)

    # Construct composite ellipse for reference coil.  We would need
    # to do this for each coil to get a complete set of coil images.
    ref_coil = -1
    Ic = np.zeros((ncoils, npcs), dtype='complex')
    mag_ests = np.zeros(ncoils)
    for cc in range(ncoils):
        # Get scaling
        res = np.linalg.lstsq(
            D[ref_coil, ...], D[cc, ...], rcond=None)[0]
        mag_ests[cc] = np.trace(res)/4

        # Get rotation
        phase = np.angle(I[ref_coil, :]) - np.angle(I[cc, ...])
        phase = np.unwrap(phase)
        phase = np.mean(phase)

        # Make composite
        Ic[cc, :] = I[cc, :]*np.exp(1j*phase)/mag_ests[cc]
        plot_ellipse(Ic[cc, :], '.-', label=str(cc))

    # Weight composite ellipse by squares of magnitudes
    weights = mag_ests**2
    weights /= np.sum(weights)
    weights = np.tile(weights[:, None], (1, npcs))
    Ic = np.sum(Ic*weights, axis=0)
    plot_ellipse(Ic, '.--', label='Ic')


    plt.axis('square')
    plt.legend()
    plt.show()
