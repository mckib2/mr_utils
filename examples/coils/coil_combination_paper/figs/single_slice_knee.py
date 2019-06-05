'''Get results for in vivo knee data, single slice.'''

from os.path import isfile
from time import time

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

# Use this walsh as mine breaks for the really noisy data...
from ismrmrdtools.coils import calculate_csm_walsh as walsh

from mr_utils.test_data import load_test_data
from mr_utils.recon.ssfp import gs_recon
from mr_utils.coils.coil_combine import gcc
from mr_utils.coils.coil_combine import (
    simple_composite_ellipse, rigid_composite_ellipse)
from mr_utils.utils import sos
from mr_utils.definitions import ROOT_DIR

if __name__ == '__main__':

    # Load the single slice test data
    path = 'mr_utils/test_data/examples/coils/'
    t0 = time()
    data = load_test_data(path, ['knee_pcs_slice64.npy'])[0]
    print('Took %d seconds to load data!' % (time() - t0))
    data *= 8e6
    ncoils, npcs, M, N = data.shape[:]
    # from mr_utils import view
    # view(data[:, 0, ...])

    phase = simple_composite_ellipse(data, coil_axis=0, pc_axis=1)
    # print(phase.shape)
    # from mr_utils import view
    # view(phase)

    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)

    # Now get full phase
    filename = 'single_slice_knee_full_phase_sub.npy'
    if not isfile(ROOT_DIR + '/'+ path + filename):
        phase_full = rigid_composite_ellipse(
            data, coil_axis=0, pc_axis=1)
        np.save(ROOT_DIR + '/' + path + filename, phase_full)
    else:
        phase_full = np.load(ROOT_DIR + '/' + path + filename)

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

    # Comparison figures
    nx, ny = len(ccs), 4
    args = {'vmin': 0, 'vmax': 1.4}
    # args = {}
    titles = [
        'Coil-by-coil',
        'Naive',
        'Full',
        'Simple']
    idx = 1
    for ii in range(nx):
        for jj in range(ny):
            plt.subplot(nx, ny, idx)
            plt.imshow(
                np.abs(res[ii, jj, ...]).T, cmap='gray', **args)

            # Add MSE to each figure
            plt.xlabel('MSE: %e' % compare_mse(
                res[ii, 0, ...],
                res[ii, jj, ...]), fontsize=10)

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
            idx += 1
    plt.show()
