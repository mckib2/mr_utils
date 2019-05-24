'''For regional differential energy minimization use brighest coil.

Notes
-----
So the idea is that doing regional differential energy minimization
(RDEM) takes a long time if you want to do it on each coil one by one.
Notice that the lGS only depends on weights, so if we can come up
with good weights, no one's the wiser.  Try finding the brighest
patch in the set of coils and using that one to find the weights.

That actually seems quite involved, and probably not something that
would work anyway, because we still have banding, and we'd be getting
intensity variation from that and the coil sensitivities.
'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

from ismrmrdtools.coils import calculate_csm_inati_iter as inati
from ismrmrdtools.simulation import (
    generate_birdcage_sensitivities as gbs)

from mr_utils.test_data.phantom import bssfp_2d_cylinder
from mr_utils.recon.ssfp import gs_recon, compute_Iw
from mr_utils.coils.coil_combine import walsh_gs, walsh
from mr_utils import view #pylint: disable=W0611

if __name__ == '__main__':

    TR = 3e-3
    alpha = np.deg2rad(30)
    N = 64
    radius = .9
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    noise_std = 0.1

    # Get npcs PCs of a cylinder
    I = bssfp_2d_cylinder(
        TR=TR, alpha=alpha, dims=(N, N), radius=radius, phase_cyc=pcs)
    # print(I.shape)
    # view(I)

    # Get some coil sensitivities
    num_coils = 4
    mps = gbs(N, number_of_coils=num_coils)
    Is = np.tile(mps[..., None], (1, 1, 1, npcs))*np.tile(
        I[None, ...], (num_coils, 1, 1, 1))
    # Shape: (coil, x, y, pcs)
    if noise_std > 0:
        n_r = np.random.normal(0, noise_std/2, Is.shape)
        n_i = np.random.normal(0, noise_std/2, Is.shape)
        n = n_r + 1j*n_i
        Is += n
    else:
        n = np.zeros(Is.shape)

    # Get truth data
    # Id = gs_recon(I, pc_axis=-1, second_pass=False)
    # Iw0, w0 = compute_Iw(I[..., 0], I[..., 2], Id, ret_weight=True)
    # Iw1, w1 = compute_Iw(I[..., 1], I[..., 3], Id, ret_weight=True)
    # I_lGS = (Iw0 + Iw1)/2
    # view(I_lGS)

    # Actually, for the truth data, let's see if we can do better by
    # averaging the weights for each coil, since they should be the
    # same
    w0 = np.zeros((N, N, num_coils), dtype='complex')
    w1 = w0.copy()
    for ii in range(num_coils):
        Id = gs_recon(Is[ii, ...], pc_axis=-1, second_pass=False)
        _Iw0, w0[..., ii] = compute_Iw(
            Is[ii, ..., 0], Is[ii, ..., 2], Id, ret_weight=True)
        _Iw1, w1[..., ii] = compute_Iw(
            Is[ii, ..., 1], Is[ii, ..., 3], Id, ret_weight=True)
    w0 = np.mean(w0, axis=-1)
    w1 = np.mean(w1, axis=-1)
    I_lGS = np.zeros((num_coils, N, N), dtype='complex')
    ns = I_lGS.copy()
    for ii in range(num_coils):
        Iw02 = Is[ii, ..., 0]*w0 + Is[ii, ..., 2]*(1 - w0)
        Iw13 = Is[ii, ..., 1]*w1 + Is[ii, ..., 3]*(1 - w1)
        n0 = n[ii, ..., 0]*w0 + n[ii, ..., 2]*(1 - w0)
        n1 = n[ii, ..., 1]*w1 + n[ii, ..., 3]*(1 - w1)
        I_lGS[ii, ...] = (Iw02 + Iw13)/2
        ns[ii, ...] = (n0 + n1)/2
    csm = walsh(I_lGS, noise_ims=ns, coil_axis=0)
    I_lGS = np.sum(np.conj(csm)*I_lGS, axis=0)
    I_lGS[np.isnan(I_lGS)] = 0
    # view(I_lGS)

    # Now replicate, but use individual weights for each coil set
    I_lGS0 = np.zeros((num_coils, N, N), dtype='complex')
    ns = I_lGS0.copy()
    for ii in range(num_coils):
        I_lGS0[ii, ...] = gs_recon(Is[ii, ...], pc_axis=-1)
        ns[ii, ...] = gs_recon(n[ii, ...], pc_axis=-1)
    csm = walsh(I_lGS0, noise_ims=ns, coil_axis=0)
    I_lGS0 = np.sum(np.conj(csm)*I_lGS0, axis=0)
    ctr = int(N/2)
    view(np.abs(I_lGS0) - np.abs(I_lGS))
    shave = 10
    plt.plot(np.abs(I_lGS0[shave:-shave, ctr]))
    plt.plot(np.abs(I_lGS[shave:-shave, ctr]), '--')
    plt.show()
    # Pooled weights works marginally better!

    # Try using walsh
    csm = walsh_gs(Is, coil_axis=0, pc_axis=-1)
    I_walsh = np.sum(
        np.conj(np.tile(csm[..., None], (1, 1, 1, npcs)))*Is, axis=0)
    # view(I_walsh)

    # Use true weights
    Iw02 = I_walsh[..., 0]*w0 + I_walsh[..., 2]*(1 - w0)
    Iw13 = I_walsh[..., 1]*w1 + I_walsh[..., 3]*(1 - w1)
    I_lGS_walsh = (Iw02 + Iw13)/2
    # view(I_lGS_walsh)
    print(compare_mse(np.abs(I_lGS), np.abs(I_lGS_walsh)))

    # Get weights from Id
    I_lGS_walsh = gs_recon(I_walsh, pc_axis=-1, second_pass=True)
    # view(I_lGS_walsh)
    print(compare_mse(np.abs(I_lGS), np.abs(I_lGS_walsh)))


    # # Now try using bad coil combine method
    # I_inati_pcs = np.zeros(Is.shape[1:], dtype='complex')
    # for ii in range(npcs):
    #     I_inati_pcs[..., ii] = inati(Is[..., ii], smoothing=0)[1]
    # I_inati = gs_recon(I_inati_pcs, pc_axis=-1)
    # # view(I_inati)
    #
    # # Now combine using true weights:
    # Iw02 = I_inati_pcs[..., 0]*w0 + I_inati_pcs[..., 2]*(1 - w0)
    # Iw13 = I_inati_pcs[..., 1]*w1 + I_inati_pcs[..., 3]*(1 - w1)
    # I_inati_lGS = (Iw02 + Iw13)/2
    # view(I_inati_lGS)
    # # Already a lot better, but not perfect...

    # # Now try using brighest coil
    # # Id = np.max(np.max(np.abs(Is), axis=-1), axis=0)
    # # Id = np.mean(I_inati_pcs, axis=-1)
    # Iw0, w0 = compute_Iw(
    #     I_inati_pcs[..., 0], I_inati_pcs[..., 2], Id, ret_weight=True)
    # Iw1, w1 = compute_Iw(
    #     I_inati_pcs[..., 1], I_inati_pcs[..., 3], Id, ret_weight=True)
    # I_lGS = (Iw0 + Iw1)/2
    # view(I_lGS)
