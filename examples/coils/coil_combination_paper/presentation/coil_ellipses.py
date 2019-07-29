'''Show how coil ellipses are generated.'''

import numpy as np
from phantominator import shepp_logan
from sigpy.mri import birdcage_maps
import matplotlib.pyplot as plt

from mr_utils import view
from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    N = 128
    ph = shepp_logan(N)
    # view(ph)

    # Simulate phae-cycled acquitions
    npcs = 100
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    T1 = ph*2
    T2 = ph
    M0 = ph
    TR = 3e-3
    alpha = np.deg2rad(30)
    _, df = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N),
        np.linspace(-1/TR, 1/TR, N))
    I = ssfp(T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=0)
    print(I.shape)

    # view(I)

    # ctr = int(N/2)
    # plt.plot(I[:, ctr, ctr].real, I[:, ctr, ctr].imag)
    # plt.axis('square')
    # plt.xlabel('Real')
    # plt.ylabel('Imaginary')
    # plt.show()


    # Make maps
    nc = 8
    mps = birdcage_maps((nc, N, N))
    print(mps.shape)
    ph = ph[None, ...]*mps

    xx, yy = int(N/3), int(N/4)
    Im = np.zeros((nc, npcs, N, N), dtype=I.dtype)
    for ii in range(nc):
        rf = np.angle(mps[ii, ...])
        Im[ii, ...] = np.abs(mps[ii, ...])*ssfp(
            T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=rf)

    #     plt.plot(Im[ii, :, xx, yy].real, Im[ii, :, xx, yy].imag)
    # plt.axis('square')
    # plt.xlabel('Real')
    # plt.ylabel('Imaginary')
    # plt.show()

    # view(Im, montage_axis=1, movie_axis=0)

    # view(Im[:, 0, ...], fft=True, log=True)
