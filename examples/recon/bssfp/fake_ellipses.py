'''Synthesize ellipses of two possible rotations given 4 points.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET, gs_recon
from mr_utils.utils import fit_ellipse_halir, plot_conic, rotate_points

if __name__ == '__main__':

    T1 = .8
    T2 = 0.035
    M0 = .8
    alpha = np.deg2rad(30)
    TR = 10e-3
    df = 1/(2*TR)
    phi_rf = 0 #np.pi/8

    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    enpcs = 100
    epcs = np.linspace(0, 2*np.pi, enpcs, endpoint=False)

    I = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=phi_rf)
    Ie = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=epcs, M0=M0, phi_rf=phi_rf)

    # plt.plot(Ie.real, Ie.imag)
    # plt.plot(I.real, I.imag, '.')
    # plt.axis('square')
    # plt.show()

    # Somehow I need to figure out how to find a point along along
    # both possible semi-major axes

    # # Choose points from the fitted ellipse
    # C = fit_ellipse_halir(I.real, I.imag)
    # print(C)
    # xe, ye = plot_conic(C, 6)
    # plt.plot(xe, ye)
    # plt.plot(I.real, I.imag)
    # plt.show()
    #
    #
    # I0 = xe + 1j*ye
    # Meff, T1_est, T2_est, df_est = PLANET(
    #     I0, alpha, TR, T1_guess=.8, compute_df=True, disp=True)
    #
    # print(T1, T2, df)
    # print(T1_est, T2_est, df_est)
