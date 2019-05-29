'''Show ellipses of coil images.'''

import numpy as np
import matplotlib.pyplot as plt

# from ismrmrdtools.simulation import (
#    generate_birdcage_sensitivities as gbs)
from sigpy.mri import birdcage_maps

from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon, compute_Iw
from mr_utils.coils.coil_combine import walsh
from mr_utils import view

if __name__ == '__main__':

    TR = 3e-3
    alpha = np.deg2rad(30)
    N = 64
    radius = .9
    npcs = 100
    assert np.mod(npcs, 4) == 0
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    noise_std = 0.01
    weighted_avg = False
    df, _ = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N), np.linspace(-1/TR, 1/TR, N))
    # view(df)

    # Get some coil sensitivities
    num_coils = 5
    # mps = gbs(N, number_of_coils=num_coils)
    mps = birdcage_maps((num_coils, N, N))
    mps *= np.exp(1j*np.random.random(mps.shape))
    # view(mps)

    # Get npcs PCs of a cylinder
    PDs, T1s, T2s = cylinder_2d(dims=(N, N), radius=radius)
    I = ssfp(T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PDs, phi_rf=0)
    Is = np.zeros((num_coils, npcs, N, N), dtype='complex')
    for ii in range(num_coils):
        Is[ii, ...] = ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PDs,
            phi_rf=np.angle(mps[ii, ...]))
        Is[ii, ...] *= np.abs(mps[ii, ...])

    # Choose a pixel to look at
    px = (int(N/3), int(N/2))
    for ii in range(num_coils):
        Is0 = Is[ii, :, px[0], px[1]]

        # # Correct for coil phase and magnitude
        # Is0 = Is0*np.exp(1j*np.angle(mps[ii, px[0], px[1]]))
        # Is0 = Is0/np.abs(mps[ii, px[0], px[1]])

        # Show coil ellipse
        plt.plot(Is0.real, Is0.imag, '.-', label=str(ii))

    # Show the result of walsh after lGS
    # assert npcs == 4
    I_lGS = np.zeros((num_coils, N, N), dtype='complex')
    for ii in range(num_coils):
        if npcs > 4:
            step = int(npcs/4)
            I_lGS[ii, ...] = gs_recon(Is[ii, ::step, ...], pc_axis=0)
        else:
            I_lGS[ii, ...] = gs_recon(Is[ii, ...], pc_axis=0)
        plt.plot(
            I_lGS[ii, px[0], px[1]].real,
            I_lGS[ii, px[0], px[1]].imag, '+')
    csm = walsh(I_lGS, noise_ims=None, coil_axis=0)
    I_walsh = np.sum(np.conj(csm)*I_lGS, axis=0)
    I_walsh0 = I_walsh[px[0], px[1]]
    plt.plot(I_walsh0.real, I_walsh0.imag, 'o')
    # w0 = np.zeros((N, N, num_coils), dtype='complex')
    # w1 = w0.copy()
    # for ii in range(num_coils):
    #     Id = gs_recon(Is[ii, ...], pc_axis=0, second_pass=False)
    #     _Iw0, w0[..., ii] = compute_Iw(
    #         Is[ii, 0, ...], Is[ii, 2, ...], Id, ret_weight=True)
    #     _Iw1, w1[..., ii] = compute_Iw(
    #         Is[ii, 1, ...], Is[ii, 3, ...], Id, ret_weight=True)
    # w0 = np.mean(w0, axis=-1)
    # w1 = np.mean(w1, axis=-1)
    # I_lGS = np.zeros((num_coils, N, N), dtype='complex')
    # n = np.zeros(I_lGS.shape)
    # for ii in range(num_coils):
    #     Iw02 = Is[ii, 0, ...]*w0 + Is[ii, 2, ...]*(1 - w0)
    #     Iw13 = Is[ii, 1, ...]*w1 + Is[ii, 3, ...]*(1 - w1)
    #     I_lGS[ii, ...] = (Iw02 + Iw13)/2
    # csm = walsh(I_lGS, noise_ims=n, coil_axis=0)
    # I_walsh = np.sum(np.conj(csm)*I_lGS, axis=0)
    # I_walsh0 = I_walsh[px[0], px[1]]
    # plt.plot(I_walsh0.real, I_walsh0.imag, '+')

    # Show the true ellipse
    Is0_true = I[:, px[0], px[1]]
    plt.plot(Is0_true.real, Is0_true.imag, '--', label='True')
    if npcs > 4:
        step = int(npcs/4)
        M = gs_recon(Is0_true[::step, ...], pc_axis=0)
    else:
        M = gs_recon(Is0_true, pc_axis=0)
    plt.plot(M.real, M.imag, '*')
    plt.axis('square')
    plt.legend()
    plt.show()
