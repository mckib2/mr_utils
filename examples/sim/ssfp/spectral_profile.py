'''Example demonstrating how to generate an SSFP spectral profile.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    # SSFP experiment params
    TR = 5e-3
    alpha = np.deg2rad(10)

    # Choose a single phase-cycle to simulate
    lpcs = 4
    pc = np.linspace(0, 2*np.pi, lpcs, endpoint=False)[2]

    # Experiment conditions and tissue params
    T1 = .750
    T2 = .035
    M0 = 1
    df = np.linspace(-1/TR, 1/TR, 200) # over all off-resonance vals
    # df = [-1, 0, 1]
    phi_rf = np.deg2rad(-70) # this changes phase values!

    # Do the thing once with no phi_rf, once with to see difference
    I = ssfp(T1, T2, TR, alpha, df, pc, M0, phi_rf=0)
    Iphi_rf = ssfp(T1, T2, TR, alpha, df, pc, M0, phi_rf=phi_rf)

    # Look at the spectral profile
    fig, ax1 = plt.subplots()
    ax1.plot(df, np.abs(I))
    ax1.plot(df, np.abs(Iphi_rf), '--')
    ax1.set_ylabel('Magnitude')
    ax1.set_xlabel('Off-resonance (Hz)')

    ax2 = ax1.twinx()
    ax2.plot(
        df, np.rad2deg(np.angle(I)), 'r--', label='Phase, phi_rf=0')
    ax2.plot(
        df, np.rad2deg(np.angle(Iphi_rf)), 'g--',
        label='Phase, phi_rf=%d deg' % np.rad2deg(phi_rf))
    ax2.set_ylabel('Phase (deg)')
    ax2.set_xlabel('Off-resonance (Hz)')
    ax2.legend()

    plt.show()
