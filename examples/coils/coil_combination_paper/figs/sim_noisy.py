'''Simulate performance under a variety of noise conditions.'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from sigpy.mri import birdcage_maps
from skimage.measure import compare_nrmse, compare_ssim
from tqdm import tqdm

from mr_utils.sim.ssfp import ssfp
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import sos
from mr_utils.coils.coil_combine import gcc, walsh
from mr_utils.coils.coil_combine import (
    rigid_composite_ellipse, simple_composite_ellipse)

if __name__ == '__main__':

    SNRs = np.linspace(1, 70, 10)
    # fig_SNR = [SNRs[3], SNRs[-1]] # SNR to use for comparison figure
    fig_SNR = [SNRs[6]]
    # SNRs = np.atleast_1d(SNRs[6])
    N = 256
    # N = 32
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

    from mr_utils import view
    view(I, montage_axis=1, movie_axis=0)

    # Make a reference image by doing lGS without any coils
    Iref = ssfp(
        T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=0)
    Iref = gs_recon(Iref, pc_axis=0)

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

    # Array to hold image comparsion figure data:
    # (coil-comb, [ref, coil-by-coil, naive, full, simple]=5, images)
    comp = np.zeros((len(fig_SNR), len(ccs), 5, N, N))

    # Do the thing!
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
            phase = simple_composite_ellipse(
                I, coil_axis=0, pc_axis=1)
            phase = np.unwrap(phase, axis=0) # ellipse unwrapping

            # plt.rc('font', family='Times New Roman', size=18)
            # plt.subplot(1, 2, 1)
            # plt.imshow(sos(I[:, 0, ...], axes=0), cmap='gray')
            # plt.tick_params(
            #     top='off', bottom='off', left='off', right='off',
            #     labelleft='off', labelbottom='off')
            #
            # plt.subplot(1, 2, 2)
            # plt.imshow(phase[0, ...]*mask)
            # plt.colorbar()
            # plt.tick_params(
            #     top='off', bottom='off', left='off', right='off',
            #     labelleft='off', labelbottom='off')
            #
            # plt.show()
            # assert False

            # Get phase substitution using full method
            phase_full = rigid_composite_ellipse(
                I, coil_axis=0, pc_axis=1)
            phase_full = np.unwrap(phase_full, axis=0)
            # from skimage.restoration import unwrap_phase
            # phase_full = unwrap_phase(phase_full*mask)

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

            # Stuff the array for the comparison figure
            if SNR in fig_SNR:
                figidx = np.argwhere(fig_SNR == SNR).squeeze()
                if ccidx == 0:
                    # reference
                    comp[figidx, ccidx, 0, ...] = np.abs(Iref)

                # coil-by-coil
                comp[figidx, ccidx, 1, ...] = np.abs(lGScc)

                 # naive
                comp[figidx, ccidx, 2, ...] = np.abs(I_cc_lGS)

                # full
                comp[figidx, ccidx, 3, ...] = np.abs(
                    I_cc_sub_full_lGS)

                # simple
                comp[figidx, ccidx, 4, ...] = np.abs(I_cc_sub_lGS)

            # Measure MSE
            mse[ccidx, 0, SNRidx] = compare_nrmse(
                np.abs(Iref), np.abs(I_cc_lGS))
            mse[ccidx, 1, SNRidx] = compare_nrmse(
                np.abs(Iref), np.abs(I_cc_sub_lGS))
            mse[ccidx, 2, SNRidx] = compare_nrmse(
                np.abs(Iref), np.abs(I_cc_sub_full_lGS))

            # Measure similarity index
            ssim[ccidx, 0, SNRidx] = compare_ssim(
                np.abs(Iref), np.abs(I_cc_lGS))
            ssim[ccidx, 1, SNRidx] = compare_ssim(
                np.abs(Iref), np.abs(I_cc_sub_lGS))
            ssim[ccidx, 2, SNRidx] = compare_ssim(
                np.abs(Iref), np.abs(I_cc_sub_full_lGS))

    # Set up LaTeX
    # plt.rc('text', usetex=True)
    # plt.rc('font', family='serif', size=16)
    plt.rc('font', family='Times New Roman', size=18)

    # Comparison figures
    nx, ny = len(ccs), 5
    args = {'vmin': 0, 'vmax': 1}
    # args = {}
    for kk in range(len(fig_SNR)):
        titles = [
            'Reference',
            'Coil-by-coil',
            'Naive',
            'Full',
            'Simple']
        idx = 1
        for ii in range(nx):
            for jj in range(ny):
                if not (ii == 0 and jj == 0): # skip ref

                    if not np.allclose(
                            comp[kk, ii, jj, ...], np.zeros((N, N))):
                        plt.subplot(nx, ny, idx)


                        # plt.imshow(
                        #     comp[kk, ii, jj, ...], cmap='gray', **args)
                        #
                        # # Add MSE to each figure
                        # plt.xlabel('MSE: %e' % compare_nrmse(
                        #     comp[kk, 0, 0, ...],
                        #     comp[kk, ii, jj, ...]), fontsize=10)

                        val = np.abs(
                            (comp[kk, 0, 0, ...] - comp[kk, ii, jj, ...])/comp[kk, 0, 0, ...])*mask
                        val = np.nan_to_num(val)
                        mse_val = compare_nrmse(
                            comp[kk, 0, 0, ...],
                            comp[kk, ii, jj, ...])

                        fac = np.max(np.abs(val).astype(float).flatten())
                        if fac > 0:
                            val /= fac
                            msg = 'MSE: %.2e (x%.1f)' % (mse_val, 1/fac)
                        else:
                            msg = ''
                        plt.imshow(val, cmap='gray', **args)

                        ann = plt.annotate(
                            msg, xy=(1, 0), xycoords='axes fraction',
                            fontsize=12, xytext=(-5, 5),
                            textcoords='offset points', color='white',
                            ha='right', va='bottom')
                        ann.set_path_effects([
                            path_effects.Stroke(linewidth=2,
                            foreground='black'),
                            path_effects.Normal()])

                        # Add headers
                        if ii == 0:
                            plt.title(titles[jj])
                        if jj == 1:
                            plt.ylabel(cc_labels[ii])

                        # Remove extras
                        plt.tick_params(
                            top='off', bottom='off', left='off',
                            right='off', labelleft='off',
                            labelbottom='off')
                idx += 1
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()

    # Plot MSE for no phase sub
    for ii in range(len(ccs)):
        plt.semilogy(
            SNRs,
            mse[ii, 0, :],
            '-', linewidth=2,
             label='%s: Naive' % cc_labels[ii])

    # Plot MSE for phase sub
    for ii in range(len(ccs)):
        plt.semilogy(
            SNRs,
            mse[ii, 1, :],
            '--', linewidth=2,
            label='%s: Simple' % cc_labels[ii])

    # Plot MSE for full phase sub
    for ii in range(len(ccs)):
        plt.semilogy(
            SNRs,
            mse[ii, 2, :],
            ':', linewidth=2,
            label='%s: Full' % cc_labels[ii])

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
            '-', linewidth=2, label='%s: Naive' % cc_labels[ii])

    # Plot SSIM for phase sub
    for ii in range(len(ccs)):
        plt.plot(
            SNRs,
            ssim[ii, 1, :],
            '--', linewidth=2, label='%s: Simple' % cc_labels[ii])

    # Plot SSIM for full phase sub
    for ii in range(len(ccs)):
        plt.plot(
            SNRs,
            ssim[ii, 2, :],
            ':', linewidth=2, label='%s: Full' % cc_labels[ii])

    plt.legend()
    plt.title('SSIM vs SNR')
    plt.xlabel('SNR')
    plt.ylabel('SSIM')
    plt.show()
