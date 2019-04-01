'''Estimate phi_rf from coil sensitivity maps.'''

import numpy as np
from ismrmrdtools.simulation import generate_birdcage_sensitivities
from ismrmrdtools.coils import calculate_csm_walsh
# from ismrmrdtools.coils calculate_csm_inati_iter
from skimage.filters import threshold_li
from tqdm import tqdm

from mr_utils import view
from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon
from mr_utils.test_data.phantom import cylinder_2d

if __name__ == '__main__':

    # Simulation parameters
    TR = 5e-3
    alpha = np.deg2rad(30)
    N = 256
    ncoils = 4
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    min_df, max_df = -1/TR, 1/TR

    # Tissue parameters
    T1 = 1.200
    T2 = 0.030
    M0 = 1
    PD, T1s, T2s = cylinder_2d(dims=(N, N), radius=.75,
                               params={'T1': T1, 'T2': T2, 'M0': M0})

    # Use a linear off-resonance
    fx = np.linspace(min_df, max_df, N)
    fy = np.zeros(N)
    df, _ = np.meshgrid(fx, fy)

    # Create true coil sensitivity maps
    csm = generate_birdcage_sensitivities(N, number_of_coils=ncoils)
    phi_rf = np.angle(csm)
    csm_mag = np.tile(
        np.abs(csm), (npcs, 1, 1, 1,)).transpose((1, 0, 2, 3))

    # Do the sim over all coils
    I = np.zeros((ncoils, npcs, N, N), dtype='complex')
    for cc in range(ncoils):
        I[cc, ...] = ssfp(
            T1s, T2s, TR, alpha, df, pcs, PD,
            phi_rf=-phi_rf[cc, ...])

        # DON'T DO THIS, STUPID!
        # # phase-cycle correction
        # Imag = np.abs(I[cc, ...])
        # Iphase = np.angle(I[cc, ...]) - np.tile(pcs/2, (N, N, 1)).T
        # I[cc, ...] = Imag*np.exp(1j*Iphase)

    I *= csm_mag
    # view(I.transpose((2, 3, 0, 1)))

    # Estimate the sensitivity maps from coil images
    recons = np.zeros((ncoils, N, N), dtype='complex')
    for cc in range(ncoils):
        recons[cc, ...] = gs_recon(I[cc, ...], pc_axis=0)
    thresh = threshold_li(np.abs(recons))
    mask = np.abs(recons) > thresh
    csm_est, _ = calculate_csm_walsh(recons)

    # This doesn't work as well, still alright, but we knew this about
    # inati
    # csm_est, _ = calculate_csm_inati_iter(recons)

    # # Do the other way: estimate coil sensitivities from phase-cycle
    # csms = np.zeros((npcs, ncoils, N, N))
    # for ii in range(npcs):
    #     csms[ii, ...], _ = calculate_csm_walsh(I[:, ii, ...])
    # csm_est = np.mean(csms, axis=0)

    # # Look at residual phase
    # view(np.rad2deg((np.angle(csm)*mask - (
    #     np.angle(csm_est) - np.pi/2)*mask)))

    df_est = np.zeros((N, N))
    M = np.zeros((ncoils, N, N), dtype='complex')
    for cc in range(ncoils):
        M[cc, ...] = gs_recon(I[cc, ...])

    # Solve for off-resonance at each voxel
    w0 = np.zeros((N, N))
    for idx in tqdm(np.ndindex((N, N)), total=N**2, leave=False):
        ii, jj = idx[:]
        tmp = np.angle(M[:, ii, jj]) - np.angle(csm_est[:, ii, jj])
        # tmp = np.unwrap(tmp)
        w0[ii, jj] = np.mean(tmp)

    # Convert to Hz
    df_est = (w0/(np.pi*TR)).reshape(df.shape)

    view(np.stack((df, -df_est)))
    view(df + df_est)# + 1/(2*TR))
