'''Try to get coil maps from phase-cycles.'''

import numpy as np
import matplotlib.pyplot as plt

from sigpy.mri import birdcage_maps

from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.coils.coil_combine import walsh
from mr_utils import view

if __name__ == '__main__':

    TR = 3e-3
    alpha = np.deg2rad(30)
    N = 64
    radius = .9
    npcs = 4
    assert np.mod(npcs, 4) == 0
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    df, _ = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N), np.linspace(-1/TR, 1/TR, N))

    # Get some coil sensitivities
    num_coils = 5
    mps = birdcage_maps((num_coils, N, N))

    # Get npcs PCs of a cylinder
    PDs, T1s, T2s = cylinder_2d(dims=(N, N), radius=radius)
    I = ssfp(T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PDs, phi_rf=0)
    Is = np.zeros((num_coils, npcs, N, N), dtype='complex')
    for ii in range(num_coils):
        Is[ii, ...] = ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PDs,
            phi_rf=np.angle(mps[ii, ...]))
        Is[ii, ...] *= np.abs(mps[ii, ...])

    # Now find the rotation back to reference for each ellipse sample
    # ref = 0
    # for ii in range(npcs):
    #     for idx in np.ndindex((N, N)):
    #         xx, yy = idx[:]
    #         px = Is[:, ii, xx, yy]
    #         for cc in range(num_coils):
    #             change = px[cc]/px[ref]
    #             phase = np.angle(change)
    #             # Is[cc, ii, xx, yy] *= np.exp(-1j*phase)
    #             Is[cc, ii, xx, yy] *= 1/change

    px = (int(N/3), int(N/3))
    for cc in range(num_coils):
        I0 = Is[cc, :, px[0], px[1]]
        plt.plot(I0.real, I0.imag)
    plt.show()

    # Now do constructive gs recon
    I_lGS = np.zeros((num_coils, N, N), dtype='complex')
    for cc in range(num_coils):
        I_lGS[ii, ...] = gs_recon(Is[ii, ...], pc_axis=0)
    view(np.mean(I_lGS, axis=0))

    # # Now get gs reconstruction for each coil
    # I_lGS = np.zeros((num_coils, N, N), dtype='complex')
    # for ii in range(num_coils):
    #     if npcs > 4:
    #         step = int(npcs/4)
    #         I_lGS[ii, ...] = gs_recon(Is[ii, ::step, ...], pc_axis=0)
    #     else:
    #         I_lGS[ii, ...] = gs_recon(Is[ii, ...], pc_axis=0)

    # # For each pixel, find the rotation and scaling to get back to
    # # the reference coil
    # csm_est = np.zeros((num_coils, N, N), dtype='complex')
    # ref = 1 # reference
    # for ii in range(num_coils):
    #     csm_est[ii, ...] = I_lGS[ii, ...]/ref # I_lGS[ref, ...]
    #
    # cc = np.sum(np.conj(csm_est)*I_lGS, axis=0)
    # view(np.stack((np.abs(cc), np.angle(cc))))

    # # Get correct scaling
    # cc = np.sum(np.conj(csm_est)*I_lGS, axis=0)
    # scale_fac = cc*csm_est[0, ...]/I_lGS[0, ...]
    # # view(scale_fac)
    # csm_est /= np.abs(scale_fac)
    # csm_est *= np.exp(-1j*np.angle(scale_fac))
    # cc = np.sum(np.conj(csm_est)*I_lGS, axis=0)
    #
    # view(np.concatenate((mps, csm_est), axis=0), montage_axis=0)
    # view(np.stack((cc*csm_est[0, ...], I_lGS[0, ...])))
    # assert np.allclose(cc*csm_est[0, ...], I_lGS[0, ...])
    # view(cc)

    # csm_walsh = walsh(I_lGS, coil_axis=0)
    # cc_walsh = np.sum(np.conj(csm_walsh)*I_lGS, axis=0)
    # view(cc_walsh)
