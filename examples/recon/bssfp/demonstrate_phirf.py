'''Example demonstrating effects of RF Tx/Rx phase on ellipse.

Notice that df and phi_rf have similar, but different effects.  Off-resonance
rotates that ellipse without moving the phase-cycle points along the
"race-track" while phi_rf both rotates and moves the phase-cycle points.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    # Sample SSFP experiment params
    T1 = 1.2
    T2 = .045
    TR = 12e-3
    alpha = np.deg2rad(7)
    M0 = 1
    phi_rf = np.pi/5
    num_dphis = 16

    # We want phase-cycles for a pixel with no offresonance, only phi_rf
    # effects and then equivalent phase-cycles for a pixel with comparable
    # off-resonance effects and no phi_rf phase.
    dphis = np.linspace(0, 2*np.pi, num_dphis, endpoint=False)
    Is_phi = ssfp(T1, T2, TR, alpha, 0, dphis, M0, phi_rf=phi_rf)
    Is_df = ssfp(T1, T2, TR, alpha, phi_rf/(np.pi*TR), dphis, M0, phi_rf=0)

    # Show the two ellipses on top of each other to see have phase-cycles have
    # "moved along the racetrack"
    plt.plot(
        np.concatenate((Is_phi.real, np.atleast_1d(Is_phi.real[0]))),
        np.concatenate((Is_phi.imag, np.atleast_1d(Is_phi[0].imag))), '+-',
        label='phi_rf')
    plt.plot(
        np.concatenate((Is_df.real, np.atleast_1d(Is_df.real[0]))),
        np.concatenate((Is_df.imag, np.atleast_1d(Is_df[0].imag))), '+--',
        label='df')
    plt.xlabel('real')
    plt.ylabel('imag')
    plt.legend()
    plt.axis('square')
    plt.show()
