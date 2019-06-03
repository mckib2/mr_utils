'''GCC comparison figure for simulation.'''

import numpy as np
import matplotlib.pyplot as plt
from sigpy.mri import birdcage_maps

from mr_utils.sim.ssfp import ssfp
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.recon.ssfp import gs_recon
from mr_utils.coils.coil_combine import gcc

if __name__ == '__main__':

    noise_std = 0
    N = 256
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
    # from mr_utils import view
    # view(I, montage_axis=0, movie_axis=1)

    if noise_std > 0:
        n_r = np.random.normal(0, noise_std/2, I.shape)
        n_i = np.random.normal(0, noise_std/2, I.shape)
        n = n_r + 1j*n_i
        I += n

    # Do coil by coil lGS and then GCC
    lGS = np.zeros((ncoils, N, N), dtype='complex')
    for cc in range(ncoils):
        lGS[cc, ...] = gs_recon(I[cc, ...], pc_axis=0)
    lGSgcc = gcc(lGS, coil_axis=0)

    # Now do GCC across coils and do lGS
    I_gcc = np.zeros((npcs, N, N), dtype='complex')
    for ii in range(npcs):
        I_gcc[ii, ...] = gcc(I[:, ii, ...], coil_axis=0)
    I_gcc_lGS = gs_recon(I_gcc, pc_axis=0)
    # from mr_utils import view
    # view(np.stack((lGSgcc, I_gcc_lGS)))

    # Now do GCC across coils, substitute phase, and do lGS
    phase = np.zeros((npcs, N, N))
    for pc in range(npcs):
        for idx in np.ndindex((N, N)):
            ii, jj = idx[:]
            midx = np.argmax(np.abs(I[:, pc, ii, jj]))
            phase[pc, ii, jj] = np.angle(I[midx, pc, ii, jj])
    phase = np.unwrap(phase, axis=0)

    I_gcc_sub = np.abs(I_gcc)*np.exp(1j*phase)
    I_gcc_sub_lGS = gs_recon(I_gcc_sub, pc_axis=0)


    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)


    # Now show the recon results
    args = {
        'vmin': 0,
        'vmax': 1,
        'cmap': 'gray'
    }
    nx, ny = 2, 3

    # First row
    plt.subplot(nx, ny, 1)
    plt.imshow(np.abs(lGSgcc), **args)
    plt.title('Coil-by-coil lGS + GCC')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.subplot(nx, ny, 2)
    plt.imshow(np.abs(I_gcc_lGS), **args)
    plt.title('Coil-GCC + lGS')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.subplot(nx, ny, 3)
    plt.imshow(np.abs(I_gcc_sub_lGS), **args)
    plt.title('Coil-GCC + phase sub + lGS')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    # Second row
    plt.subplot(nx, ny, 5)
    plt.imshow(np.abs(np.abs(lGSgcc) - np.abs(I_gcc_lGS)), **args)
    plt.ylabel('Residual Error')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.subplot(nx, ny, 6)
    plt.imshow(
        np.abs(np.abs(lGSgcc) - np.abs(I_gcc_sub_lGS)), **args)
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.show()
