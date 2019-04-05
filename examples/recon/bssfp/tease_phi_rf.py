'''Tease out phi_rf from multiple acquisition bSSFP experiment.

Right now we're fighting an extra degree of freedom.  Need to find
some constraint so we get that last degree of freedom locked up.
'''

import numpy as np
import matplotlib.pyplot as plt
from ismrmrdtools.simulation import generate_birdcage_sensitivities

from mr_utils import view
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import (do_planet_rotation, get_center,
                            fit_ellipse_halir, get_semiaxes)

if __name__ == '__main__':

    # Set up the experiment
    TR = 10e-3
    alpha = np.deg2rad(20)
    M0 = 1
    lpcs = 8
    pcs = np.linspace(0, 2*np.pi, lpcs, endpoint=False)
    dim = 64
    ncoils = 4

    # Set up the tissue and environment nuissances
    T1 = .750
    T2 = .035
    df = 40 # only positive because pcs are (0, 2 pi)

    # Get coil sensitivities and coil channels for 1 voxel
    xx, yy = int(dim/4), int(dim/3)
    csm = generate_birdcage_sensitivities(
        dim, number_of_coils=ncoils)[:, xx, yy]
    phi_rf = np.angle(csm)
    # phi_rf = np.zeros(csm.shape)
    csm = np.abs(csm)

    # Run the experiment for one voxel, all coils
    I = np.zeros((ncoils, lpcs), dtype='complex')
    I0 = np.zeros(I.shape, dtype='complex')
    phis = np.zeros((ncoils))
    for cc in range(ncoils):
        for nn in range(lpcs):

            # Get center pixel
            I[cc, nn] = csm[cc]*ssfp(
                T1, T2, TR, alpha, df, pcs[nn], M0,
                phi_rf=phi_rf[cc])

        # Do PLANET rotation to get vertical ellipse
        xr, yr, _C0, phis[cc] = do_planet_rotation(I[cc, :])
        I0[cc, :] = xr + 1j*yr

        # plt.plot(I[cc, :].real, I[cc, :].imag)
        # plt.plot(I0[cc, :].real, I0[cc, :].imag)
        # plt.axis('square')
        # plt.show()

    # Get coil sensitivity map estimates
    from ismrmrdtools.coils import calculate_csm_walsh
    recons = np.zeros(ncoils, dtype='complex')
    for cc in range(ncoils):
        view(gs_recon(I[cc, :]))
        # recons[cc] = gs_recon(I[cc, :][:, None, None], pc_axis=-1)
    # csm_est = calculate_csm_walsh(recons[:, None, None])
    # view(csm_est)

    # # Can we find the null?
    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # dfs = np.linspace(-1/TR, 1/TR, lpcs)
    # print(np.rad2deg(phi_rf))
    # print(np.rad2deg(phis))
    # for cc in range(ncoils):
    #     im0 = np.atleast_2d(I[cc, ::2])
    #     im1 = np.atleast_2d(I[cc, 1::2])
    #     recon0 = gs_recon(im0, pc_axis=-1)
    #     recon1 = gs_recon(im1, pc_axis=-1)
    #     recon = (recon0 + recon1)/2
    #
    #     ax1.plot(dfs, np.abs(I[cc, :]), '.-')
    #     # ax1.plot(dfs, np.tile(np.abs(recon), (lpcs, 1)))
    #
    #     ax2.plot(dfs, np.rad2deg(np.angle(I[cc, :])), '.--')
    #     # ax2.plot(np.rad2deg(np.angle(recon)), '+')
    #
    # plt.show()

    # Coefficient matrix
    # We have 1 degree of freedom that I am filling by cheating.
    # The last row has a 1 in the phi_rf[0] spot and I'm feeding it
    # the true value of phi_rf[0] to lock down that degree of freedom
    # while I try to figure out how to actually constrain it.
    A = np.zeros((ncoils+1, ncoils+1))

    # df is always effecting the measurement except for last
    # artificial row
    A[:-1, ncoils] = 1

    # One coil per row
    for cc in range(ncoils):
        A[cc, cc] = 1

    # Constrain the last degree of freedom:
    A[-1, 0] = 1

    # Make sure A looks right:
    print(A)

    # Least squares solution
    val = phi_rf[0]
    y = np.concatenate((phis, [val])) # feed true phi_rf[0]
    x = np.linalg.lstsq(A, y, rcond=None)[0]

    print(np.rad2deg(x[:ncoils]))
    print(np.rad2deg(phi_rf))

    print(x[ncoils]/(np.pi*TR) + 1/(2*TR))
    print(df)

    # With lpcs=4, ncoils=4, have 4 equations, 5 unknowns
    # phi_rf[0] + df = phis[0]
    # phi_rf[1] + df = phis[1]
    # phi_rf[2] + df = phis[2]
    # phi_rf[3] + df = phis[3]


    # # Can we use something from PLANET?
    # C0 = fit_ellipse_halir(I0[0, :].real, I0[0, :].imag)
    # xc, yc = get_center(C0)
    # A, B = get_semiaxes(C0)
    # plt.plot(I0[0, :].real, I0[0, :].imag)
    # plt.plot(I0[0, 0].real, I0[0, 0].imag, '*')
    # t = np.arctan2(I0[0, 0].imag, I0[0, 0].real - xc)
    # plt.plot(xc + A*np.cos(t), B*np.sin(t), '*')
    # plt.axis('square')
    # plt.show()
