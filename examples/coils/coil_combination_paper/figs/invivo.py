'''Show results using 4 channel brain image.'''

from os.path import isfile

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_nrmse

# Use this walsh as mine breaks for the really noisy data...
from ismrmrdtools.coils import calculate_csm_walsh as walsh

from mr_utils.test_data import load_test_data
from mr_utils.recon.ssfp import gs_recon
from mr_utils.coils.coil_combine import gcc
from mr_utils.coils.coil_combine import (
    rigid_composite_ellipse, simple_composite_ellipse)
from mr_utils.utils import sos

if __name__ == '__main__':

    path = 'mr_utils/test_data/examples/coils/'
    data = load_test_data(path, ['ssfp_brain_masters.npy'])[0]
    # data = data[..., ::4] # only the PCs we need
    # data = np.moveaxis(data, (-2, -1), (0, 1))
    # shave = int(data.shape[2]/4)
    # data = data[..., shave:-shave, :]
    data *= 3e5
    # ncoils, npcs, M, N = data.shape[:]
    # # print(data.shape)
    # from mr_utils import view
    # view(data, fft=True)
    # assert False

    # # Do some fancy dancing to average all similar phase cycles
    # sh = data.shape[:]
    # adj = np.mod(sh[-1], 4)
    # data = np.reshape(data[..., :-adj], (*sh[:-1], 4, -1))
    # data = np.sum(data, axis=-1)
    # data = np.moveaxis(data, (-1, -2), (0, 1)) # put axes in place

    # We are in k-space, put into image space
    # ax =(-2, -1)
    ax = (0, 1)
    data = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        data, axes=ax), axes=ax), axes=ax)

    # sl = int(data.shape[2]/4)
    # data = data[..., sl:-sl, :]
    # # npcs, ncoils, sx, sy = I.shape[:]
    # data = np.moveaxis(data, 0, 1)

    sl = int(data.shape[0]/4)
    data = data[sl:-sl, :, ...]
    data = np.moveaxis(data, (-1, -2), (0, 1))
    data = np.rot90(data, axes=(-2, -1))
    ncoils, npcs, M, N = data.shape[:]


    # Make a mask for pretty pics
    mask = sos(data, axes=(0, 1))
    mask = mask > np.mean(mask.flatten())
    # from mr_utils import view
    # view(mask)

    phase = simple_composite_ellipse(data, coil_axis=0, pc_axis=1)
    print(phase.shape)
    # from mr_utils import view
    # view(phase)

    # Set up LaTeX
    # plt.rc('text', usetex=True)
    # plt.rc('font', family='serif', size=16)
    plt.rc('font', family='Times New Roman', size=16)

    # Show phase of simple phase substitution
    plt.imshow(phase[1, ...]*mask)
    # plt.xlabel('Phase substitution for 90° phase-cycle.')
    plt.colorbar()
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')
    plt.show()

    # Now get full phase
    filename = path + 'phase_full_invivo.npy'
    if not isfile(filename):
        phase_full = rigid_composite_ellipse(
            data, coil_axis=0, pc_axis=1)
        np.save(filename, phase_full)
    else:
        phase_full = np.load(filename)

    # Unwrap the phase around the coils
    phase = np.unwrap(phase, axis=0)
    phase_full = np.unwrap(phase_full, axis=0)
    # from mr_utils import view
    # view(phase_full)

    # Do each recon...
    ccs = [
        lambda x0: sos(x0, axes=0),
        lambda x0: gcc(x0, vcoils=1, coil_axis=0),
        # lambda x0: np.sum(
        #     walsh(x0, coil_axis=0).conj()*x0, axis=0)
        lambda x0: np.sum(walsh(x0)[0].conj()*x0, axis=0)
    ]
    cc_labels = [
        'SOS',
        'GCC',
        'SMF'
    ]
    # Array to hold image comparsion figure data:
    # (coil-comb, [coil-by-coil, naive, full, simple]=4, images)
    res = np.zeros((len(ccs), 4, M, N), dtype='complex')
    for ccidx, cc in enumerate(ccs):

        # Do coil by coil lGS
        lGS = np.zeros((ncoils, M, N), dtype='complex')
        for jj in range(ncoils):
            lGS[jj, ...] = gs_recon(data[jj, ...], pc_axis=0)

        # Get gold standard by coil combing the coil-by-coil lGS
        lGScc = cc(lGS)

        # Now do coil combine and then lGS
        I_cc = np.zeros((npcs, M, N), dtype='complex')
        for ii in range(npcs):
            I_cc[ii, ...] = cc(data[:, ii, ...])
        I_cc_lGS = gs_recon(I_cc, pc_axis=0)

        # Now do coil combine, substitute phase, and do lGS
        I_cc_sub = np.abs(I_cc)*np.exp(1j*phase)
        I_cc_sub_lGS = gs_recon(I_cc_sub, pc_axis=0)
        # from mr_utils import view
        # view(np.stack((lGScc, I_cc_lGS, I_cc_sub_lGS)))

        # Now do coil combine, substitute full phase, and do lGS
        I_cc_sub_full = np.abs(I_cc)*np.exp(1j*phase_full)
        I_cc_sub_full_lGS = gs_recon(I_cc_sub_full, pc_axis=0)

        # coil-by-coil
        res[ccidx, 0, ...] = np.abs(lGScc)

         # naive
        res[ccidx, 1, ...] = np.abs(I_cc_lGS)

        # full
        res[ccidx, 2, ...] = np.abs(
            I_cc_sub_full_lGS)

        # simple
        res[ccidx, 3, ...] = np.abs(I_cc_sub_lGS)
    res = np.nan_to_num(res)

    # Comparison figures
    nx, ny = len(ccs), 4
    args = {
        'vmin': 0,
        'vmax': 1.2
    }
    # args = {}
    titles = [
        'Coil-by-coil',
        'Naive',
        'Full',
        'Simple']
    idx = 1
    mse_plots = False
    for ii in range(nx):
        for jj in range(ny):
            plt.subplot(nx, ny, idx)

            if not mse_plots:
                plt.imshow(
                    np.abs(res[ii, jj, ...]), cmap='gray', **args)
            else:
                val = np.abs(
                    (res[ii, 0, ...] - res[ii, jj, ...])/res[ii, 0, ...])*np.abs(mask)
                mse_val = compare_nrmse(
                    res[ii, 0, ...],
                    res[ii, jj, ...])

                fac = np.max(np.abs(val).astype(float).flatten())
                print(fac)
                if fac > 0:
                    val /= fac
                    msg = 'MSE: %.2e (x%.1f)' % (mse_val, 1/fac)
                else:
                    msg = ''
                #     plt.imshow(
                #         np.abs(1/np.log(np.abs(
                #             res[ii, 0, ...] - res[ii, jj, ...])))/1e2,
                #         cmap='gray', **args)
                # else:
                #     msg = 'MSE: %.2e' % mse_val
                plt.imshow(val, cmap='gray', **args)
                # plt.text(0, 0, 'MSE: %e' % compare_mse(
                #     res[ii, 0, ...],
                #     res[ii, jj, ...]), fontsize=10)
                plt.annotate(
                    msg, xy=(1, 0), xycoords='axes fraction',
                    fontsize=12, xytext=(-5, 5),
                    textcoords='offset points', color='white',
                    ha='right', va='bottom')

            # # Add MSE to each figure
            # plt.xlabel('MSE: %e' % compare_mse(
            #     res[ii, 0, ...],
            #     res[ii, jj, ...]), fontsize=10)

            # Add headers
            if ii == 0:
                plt.title(titles[jj])
            if jj == 0:
                plt.ylabel(cc_labels[ii])

            # Remove extras
            plt.tick_params(
                top='off', bottom='off', left='off',
                right='off', labelleft='off',
                labelbottom='off')
            # plt.axis('equal')
            idx += 1
    # plt.axes().set_aspect('equal')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
