'''Try to get points to rotate along ellipse using coil sensitivity.

Notes
-----
Because off-resonance stays the same, coil ellipses only differ by
rotation and scaling one from another, the points still lie at the
same relative location on the ellipses.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp

def plot_ellipse(I, fmt='-'):
    '''Plot closed ellipse in complex plane.'''
    x, y = I.real, I.imag
    plt.plot(
        np.concatenate((x, [x[0]])),
        np.concatenate((y, [y[0]])), fmt)

if __name__ == '__main__':

    T1 = 1.2
    T2 = .03
    TR = 3e-3
    alpha = np.deg2rad(7)
    npcs = 12
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    M0 = 1
    df = 1/(2*TR)

    I0 = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=0)
    rf = .1
    I1 = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=rf)

    plot_ellipse(I0, '.-')
    plot_ellipse(I1*np.exp(1j*rf), '.--')
    plt.axis('square')
    plt.show()
