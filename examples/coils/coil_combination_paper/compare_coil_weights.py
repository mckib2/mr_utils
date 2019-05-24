'''Compare weights found from different coils.

We expect them to be the same, let's see if that's actually the case.
They are close!  Exactly what we expected!  They are not as close as
I thought they'd be, but it makes sense considering that the coil
sensitivities distort the images a little bit.

This is a little strange, since all the pixels are statistically
unrelated, so patch size is (1, 1).  Might be more instructive to
do this with a real image.
'''

import numpy as np

from ismrmrdtools.simulation import (
    generate_birdcage_sensitivities as gbs)

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon, compute_Iw

if __name__ == '__main__':

    N = 64
    TR = 3e-3
    alpha = np.deg2rad(30)
    M0 = 1
    pcs = np.linspace(0, 2*np.pi, 4, endpoint=False)
    T2 = np.random.random((N, N))
    T1 = np.max(T2.flatten()) + np.random.random((N, N))
    df = 2/TR*np.random.random((N, N)) - 1/TR
    I = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0)
    Id = gs_recon(I, pc_axis=0, second_pass=False)

    # Find the "true" weights
    _Iw0, w0 = compute_Iw(
        I[0, ...], I[2, ...], Id, ret_weight=True, patch_size=(1, 1))
    _Iw1, w1 = compute_Iw(
        I[1, ...], I[3, ...], Id, ret_weight=True, patch_size=(1, 1))
    w = np.stack((w0, w1))

    # Make coil sensitivities
    num_coils = 5
    mps = gbs(N, number_of_coils=num_coils)
    Is = np.tile(mps[:, None, ...], (1, 4, 1, 1))*np.tile(
        I[None, ...], (num_coils, 1, 1, 1))

    # Find weights using each coil set
    weights = np.zeros((num_coils,) + w.shape[:])
    for ii in range(num_coils):

        I0 = Is[ii, ...]
        Id = gs_recon(I0, pc_axis=0, second_pass=False)
        _Iw0, w0 = compute_Iw(
            I0[0, ...], I0[2, ...], Id, ret_weight=True,
            patch_size=(1, 1))
        _Iw1, w1 = compute_Iw(
            I0[1, ...], I0[3, ...], Id, ret_weight=True,
            patch_size=(1, 1))
        w_coil = np.stack((w0, w1))
        weights[ii, ...] = w_coil

        print(np.mean((w.real - w_coil.real).flatten()))

    weights = np.mean(weights, axis=0)
    print(np.mean((w.real - weights.real).flatten()))
