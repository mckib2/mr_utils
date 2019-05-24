'''Try to look at the error of of w.'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_nrmse
from tqdm import trange

from ismrmrdtools.simulation import (
    generate_birdcage_sensitivities as gbs)

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon, compute_Iw
from mr_utils.coils.coil_combine import walsh_gs
from mr_utils import view

if __name__ == '__main__':

    N = 64
    TR = 3e-3
    alpha = np.deg2rad(30)
    M0 = 1
    pcs = np.linspace(0, 2*np.pi, 4, endpoint=False)
    iters = 5
    num_coils_todo = [2, 4] #[2, 3, 4, 5, 6, 7, 8]

    err = np.zeros((len(num_coils_todo), iters))
    nrmse = err.copy()
    stderr = err.copy()
    for ii, num_coils in enumerate(num_coils_todo):

        # Make coil sensitivities
        mps = gbs(N, number_of_coils=num_coils)

        for it in trange(iters, leave=False, desc='c%d' % num_coils):

            # Generate new random image
            T2 = np.random.random((N, N))
            T1 = np.max(T2.flatten()) + np.random.random((N, N))
            df = 2/TR*np.random.random((N, N)) - 1/TR
            I = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0)
            Id = gs_recon(I, pc_axis=0, second_pass=False)

            # Find the "true" weights
            _Iw0, w0 = compute_Iw(
                I[0, ...], I[2, ...], Id, ret_weight=True)
            _Iw1, w1 = compute_Iw(
                I[1, ...], I[3, ...], Id, ret_weight=True)
            w = np.stack((w0, w1))

            # Apply coil sensitivities
            Is = np.tile(mps[:, None, ...], (1, 4, 1, 1))*np.tile(
                I[None, ...], (num_coils, 1, 1, 1))

            # Try getting weights from Walsh
            Icomb = walsh_gs(Is, coil_axis=0, pc_axis=0)
            Id = gs_recon(Icomb, pc_axis=0, second_pass=False)
            _Iw0, w0_walsh = compute_Iw(
                Icomb[0, ...], Icomb[2, ...], Id, ret_weight=True)
            _Iw1, w1_walsh = compute_Iw(
                Icomb[1, ...], Icomb[3, ...], Id, ret_weight=True)
            w_walsh = np.stack((w0_walsh, w1_walsh))

            val = (w.real - w_walsh.real).flatten()/2
            nrmse[ii, it] = compare_nrmse(w.real, w_walsh.real)
            err[ii, it] = np.mean(val)
            stderr[ii, it] = np.std(val)

    plt.errorbar(
        num_coils_todo,
        np.mean(nrmse, axis=-1),
        yerr=np.std(nrmse, axis=-1))
    plt.show()

    plt.errorbar(
        num_coils_todo,
        np.mean(err, axis=-1),
        yerr=np.mean(stderr, axis=-1))
    plt.show()
