'''Simulate performance under a variety of noise conditions.'''

import numpy as np
import matplotlib.pyplot as plt
from sigpy.mri import birdcage_maps
from skimage.measure import compare_mse, compare_ssim
from tqdm import tqdm

from mr_utils.sim.ssfp import ssfp
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import sos
from mr_utils.coils.coil_combine import gcc, walsh
from mr_utils.coils.coil_combine import rigid_composite_ellipse

if __name__ == '__main__':

    SNRs = np.linspace(1, 70, 10)
    # N = 256
    N = 64
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    ncoils = 5
    mps = birdcage_maps((ncoils, N, N))
    TR = 3e-3
    alpha = np.deg2rad(30)
    _, df = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N),
        np.linspace(-1/TR, 1/TR, N))
    radius = .9
    PD, T1s, T2s = cylinder_2d(dims=(N, N), radius=radius)

    # Simulate the acquisition
    I = np.zeros((ncoils, npcs, N, N), dtype='complex')
    for cc in range(ncoils):
        rf = np.angle(mps[cc, ...])
        I[cc, ...] = np.abs(mps[cc, ...])*ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=rf)
    Itrue = I.copy()
    # from mr_utils import view
    # view(I, montage_axis=0, movie_axis=1)

    # Make mask for pretty figs
    mask = sos(Itrue, axes=(0, 1)) > .5

    # Loop through coil combination methods
    ccs = [
        lambda x0: sos(x0, axes=0),
        lambda x0: gcc(x0, vcoils=1, coil_axis=0),
        lambda x0: np.sum(
            walsh(x0, coil_axis=0).conj()*x0, axis=0)
    ]
    cc_labels = [
        'SOS',
        'GCC',
        'SMF'
    ]
    # Get ready to measure MSE
    mse = np.zeros((len(ccs), 3, SNRs.size))
    ssim = np.zeros((len(ccs), 3, SNRs.size))
    for ccidx, cc in tqdm(
            enumerate(ccs), leave=False, total=len(ccs)):
        for SNRidx, SNR  in tqdm(
                enumerate(SNRs), leave=False, total=SNRs.size):
            if SNRs is not None:

                mu_r = np.mean(I.real[I.real > 0].flatten())
                mu_i = np.mean(I.imag[I.imag > 0].flatten())
                noise_std_r = mu_r/SNR
                noise_std_i = mu_i/SNR

                n_r = np.random.normal(0, noise_std_r, I.shape)
                n_i = np.random.normal(0, noise_std_i, I.shape)
                n = n_r + 1j*n_i
                I = Itrue + n
            else:
                I = Itrue.copy()

            # Do coil by coil lGS
            lGS = np.zeros((ncoils, N, N), dtype='complex')
            for jj in range(ncoils):
                lGS[jj, ...] = gs_recon(I[jj, ...], pc_axis=0)

            # Get phase substitution using simple method
            phase = np.zeros((npcs, N, N))
            for pc in range(npcs):
                for idx in np.ndindex((N, N)):
                    ii, jj = idx[:]
                    midx = np.argmax(np.abs(I[:, pc, ii, jj]))
                    phase[pc, ii, jj] = np.angle(I[midx, pc, ii, jj])
            phase = np.unwrap(phase, axis=0) # ellipse unwrapping

            # Get phase substitution using full method
            phase_full = rigid_composite_ellipse(
                I, coil_axis=0, pc_axis=1)
            phase_full = np.unwrap(phase_full, axis=0)

            # Get gold standard by coil combing the coil-by-coil lGS
            # lGSsos = sos(lGS, axes=0)
            lGScc = cc(lGS)

            # Now do coil combine and then lGS
            I_cc = np.zeros((npcs, N, N), dtype='complex')
            for ii in range(npcs):
                I_cc[ii, ...] = cc(I[:, ii, ...])
            I_cc_lGS = gs_recon(I_cc, pc_axis=0)

            # Now do coil combine, substitute phase, and do lGS
            I_cc_sub = np.abs(I_cc)*np.exp(1j*phase)
            I_cc_sub_lGS = gs_recon(I_cc_sub, pc_axis=0)
            # from mr_utils import view
            # view(np.stack((lGScc, I_cc_lGS, I_cc_sub_lGS)))

            # Now do coil combine, substitute full phase, and do lGS
            I_cc_sub_full = np.abs(I_cc)*np.exp(1j*phase_full)
            I_cc_sub_full_lGS = gs_recon(I_cc_sub_full, pc_axis=0)

            # Measure MSE
            mse[ccidx, 0, SNRidx] = compare_mse(
                np.abs(lGScc), np.abs(I_cc_lGS))
            mse[ccidx, 1, SNRidx] = compare_mse(
                np.abs(lGScc), np.abs(I_cc_sub_lGS))
            mse[ccidx, 2, SNRidx] = compare_mse(
                np.abs(lGScc), np.abs(I_cc_sub_full_lGS))

            # Measure similarity index
            ssim[ccidx, 0, SNRidx] = compare_ssim(
                np.abs(lGScc), np.abs(I_cc_lGS))
            ssim[ccidx, 1, SNRidx] = compare_ssim(
                np.abs(lGScc), np.abs(I_cc_sub_lGS))
            ssim[ccidx, 2, SNRidx] = compare_ssim(
                np.abs(lGScc), np.abs(I_cc_sub_full_lGS))

    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)

    # Plot MSE for no phase sub
    for ii in range(len(ccs)):
        plt.semilogy(
            SNRs,
            mse[ii, 0, :],
            '-', label='%s: no sub' % cc_labels[ii])

    # Plot MSE for phase sub
    for ii in range(len(ccs)):
        plt.semilogy(
            SNRs,
            mse[ii, 1, :],
            '--', label='%s: sub' % cc_labels[ii])

    # Plot MSE for full phase sub
    for ii in range(len(ccs)):
        plt.semilogy(
            SNRs,
            mse[ii, 2, :],
            ':', label='%s: full' % cc_labels[ii])

    plt.legend()
    plt.title('log(MSE) vs SNR')
    plt.xlabel('SNR')
    plt.ylabel('log(MSE)')
    plt.show()

    # Plot SSIM for no phase sub
    for ii in range(len(ccs)):
        plt.plot(
            SNRs,
            ssim[ii, 0, :],
            '-', label='%s: no sub' % cc_labels[ii])

    # Plot SSIM for phase sub
    for ii in range(len(ccs)):
        plt.plot(
            SNRs,
            ssim[ii, 1, :],
            '--', label='%s: sub' % cc_labels[ii])

    # Plot SSIM for full phase sub
    for ii in range(len(ccs)):
        plt.plot(
            SNRs,
            ssim[ii, 2, :],
            ':', label='%s: full' % cc_labels[ii])

    plt.legend()
    plt.title('SSIM vs SNR')
    plt.xlabel('SNR')
    plt.ylabel('SSIM')
    plt.show()
