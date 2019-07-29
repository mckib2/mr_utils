'''Demonstrate inverse affine transformation as sensitivities.
'''

import numpy as np
import matplotlib.pyplot as plt
from sigpy.mri import birdcage_maps

from mr_utils.sim.ssfp import ssfp
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.coils.coil_combine import rigid_composite_ellipse

if __name__ == '__main__':

    # Start out with an easy example: two coils
    SNR = 50
    N = 64
    alpha = np.deg2rad(10)
    TR = 3e-3
    _, df = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N),
        np.linspace(-1/TR, 1/TR, N))
    radius = .9
    PD, T1s, T2s = cylinder_2d(dims=(N, N), radius=radius)
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    ncoils = 5
    mps = birdcage_maps((ncoils, N, N))

    # Simulate acquisition
    I = np.zeros((ncoils, npcs, N, N), dtype='complex')
    for cc in range(ncoils):
        rf = np.angle(mps[cc])
        I[cc, ...] = np.abs(mps[cc])*ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=rf)
    Itrue = I.copy()

    # Add noise if needed
    if SNR is not None:
        noise_std_r = np.mean(np.abs(I.real))/SNR
        noise_std_i = np.mean(np.abs(I.imag))/SNR
        n_r = np.random.normal(0, noise_std_r, I.shape)
        n_i = np.random.normal(0, noise_std_i, I.shape)
        I += n_r + 1j*n_i

    composite_ellipse = rigid_composite_ellipse(
        I, coil_axis=0, pc_axis=1, ret_ellipse=True)

    # Let's take a looksie
    xx, yy = int(N/3), int(N/3)
    plt.plot(
        composite_ellipse[:, xx, yy].real,
        composite_ellipse[:, xx, yy].imag, '--')
    plt.axis('square')
    plt.show()
