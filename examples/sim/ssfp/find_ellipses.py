'''Given 4 points, find all possible ellipses.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import (
    fit_ellipse_halir, plot_conic, rotate_points)

if __name__ == '__main__':

    T1 = .8
    T2 = 0.035
    M0 = .8
    alpha = np.deg2rad(7)
    TR = 3e-3
    df = 1/(5*TR)
    phi_rf = 0 #np.pi/8

    npcs = 6
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    enpcs = 100
    epcs = np.linspace(0, 2*np.pi, enpcs, endpoint=False)
    assert np.mod(enpcs, 4) == 0

    I = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=phi_rf)
    Ie = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=epcs, M0=M0, phi_rf=phi_rf)
    M = gs_recon(Ie[::int(enpcs/4)], pc_axis=0, second_pass=False)

    mx, my = np.mean(I.real), np.mean(I.imag)
    x, y = I.real, I.imag
    xe, ye = Ie.real, Ie.imag

    # I think that the centroid is not the same as the center of the
    # ellipse, so we subtract the mean to get it zero centered,
    # it's not really zero centered.

    # Seem to work well when alpha ~ 20?

    xf, yf = rotate_points(
        *plot_conic(fit_ellipse_halir(x - mx, y - my)), np.pi/2)
    plt.plot(xf + mx, yf + my)
    plt.plot(x, y, '.')
    plt.plot(xe, ye, ':')
    plt.plot(M.real, M.imag, '*')
    plt.axis('square')
    plt.show()
