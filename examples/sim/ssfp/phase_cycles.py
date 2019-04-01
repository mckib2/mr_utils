'''Example showing how phase-cycles lie on spectral profile.

Notes
-----
When we sweep over off-resonance (dfs), we can readily see the
characteristic frequency response for bSSFP.  However, when we sweep
across linear phase-cycle, it appears different.  This is due to the
fact that when we measure at TE = TR/2, the resulting magnetization
has rotated by half of its total precession angle.  We can correct
for this by subtracting half of the linear phase-cylcle value from
the phase.

See the discussion directly above 'EXPERIMENTAL METHODS' on page 6 in
[1]_.

References
----------
.. [1] Miller, Karla L. "Asymmetries of the balanced SSFP profile.
       Part I: theory and observation." Magnetic Resonance in
       Medicine: An Official Journal of the International Society for
       Magnetic Resonance in Medicine 63.2 (2010): 385-395.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    # SSFP experiment params
    TR = 12e-3
    alpha = np.deg2rad(10)
    lpcs = 64
    pcs = np.linspace(-2*np.pi, 2*np.pi, lpcs, endpoint=False)

    # Experiment conditions and tissue params
    T1 = .830
    T2 = .080
    M0 = 1
    dfs = np.linspace(-1/TR, 1/TR, lpcs, endpoint=False)

    # Do the thing once with no phi_rf, once with to see difference
    I = ssfp(T1, T2, TR, alpha, 0, pcs, M0, phi_rf=0)
    Idf = ssfp(T1, T2, TR, alpha, dfs, M0, phi_rf=0)

    # Look at the spectral profile
    pcs_deg = np.rad2deg(pcs)
    aI = np.angle(I)
    aIdf = np.unwrap(np.angle(Idf)[::-1])[::-1]

    fig, ax1 = plt.subplots()
    ax1.plot(pcs_deg, np.abs(I))
    ax1.plot(pcs_deg, np.abs(Idf), '--')
    ax1.set_ylabel('Magnitude')
    ax1.set_xlabel('Frequency (deg)')

    ax2 = ax1.twinx()
    ax2.plot(pcs_deg, aI, '--', label='Phase, pcs')
    ax2.plot(
        pcs_deg, aI - pcs/2, '--', label='Phase - phase_cyc/2, pcs')
    ax2.plot(pcs_deg, aIdf, ':', label='Phase, dfs')
    ax2.set_ylabel('Phase (rad)')
    ax2.set_xlabel('Frequency (deg)')
    ax2.legend()

    plt.show()
