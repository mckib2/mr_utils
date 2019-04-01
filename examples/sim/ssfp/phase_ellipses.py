'''Show how ellipses change between sweeping df and phase_cyc.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    # Experiment params
    TR = 10e-3
    alpha = np.deg2rad(30)
    lpcs = 16
    pcs = np.linspace(-2*np.pi, 2*np.pi, lpcs, endpoint=False)

    # Tissue params
    T1 = 1.2
    T2 = .035
    M0 = 1
    df = 0
    dfs = np.linspace(-1/TR, 1/TR, lpcs, endpoint=False) + df

    # Do the thing
    I = ssfp(T1, T2, TR, alpha, dfs, 0, M0, phi_rf=0)
    I0 = ssfp(T1, T2, TR, alpha, df, pcs, M0, phi_rf=0)

    # Do phase-cycle correction
    Imag = np.abs(I0)
    Iphase = np.angle(I0) - pcs/2
    I0 = Imag*np.exp(1j*Iphase)

    # Look at ellipses in complex plane
    plt.plot(I.real, I.imag, '.-')
    plt.plot(I0.real, I0.imag, '.--')
    plt.axis('square')
    plt.show()
