'''Try figuring out coil sensitivities.'''

import numpy as np
import matplotlib.pyplot as plt
from sigpy.mri import birdcage_maps
from scipy.optimize import minimize
from scipy.cluster.vq import whiten

from mr_utils.sim.ssfp import ssfp
from mr_utils.test_data.phantom import cylinder_2d, binary_smiley
from mr_utils.recon.ssfp import gs_recon
from mr_utils.utils import sos
from mr_utils import view # pylint: disable=W0611

def get_coils(dims):
    '''Make coil sensitivities.'''
    return birdcage_maps(dims)

def get_df(dims, TR):
    '''Make off-res.'''
    _, df = np.meshgrid(
        np.linspace(-1/TR, 1/TR, dims[0]),
        np.linspace(-1/TR, 1/TR, dims[1]))
    return df

def PolyArea(x, y):
    '''Shoelace formula'''
    return 0.5*np.abs(
        np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

if __name__ == '__main__':

    noise_std = 0
    N = 64
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    ncoils = 5
    mps = get_coils(dims=(ncoils, N, N))
    TR = 3e-3
    alpha = np.deg2rad(30)
    df = get_df((N, N), TR)
    radius = .9
    PD, T1s, T2s = cylinder_2d(dims=(N, N), radius=radius)
    # PD = binary_smiley(N, radius=radius)*20

    # Simulate the acquisition
    I = np.zeros((ncoils, npcs, N, N), dtype='complex')
    for cc in range(ncoils):
        rf = np.angle(mps[cc, ...])
        I[cc, ...] = np.abs(mps[cc, ...])*ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=rf)
    # view(I, montage_axis=0, movie_axis=1)

    if noise_std > 0:
        n_r = np.random.normal(0, noise_std/2, I.shape)
        n_i = np.random.normal(0, noise_std/2, I.shape)
        n = n_r + 1j*n_i
        I += n

    # We can find the phase-cycle sensitivities easily using the
    # lGS recon on each coil.  The coil sensitivities are divided out
    # but we should be wary of the SNR at each pixel
    P = np.zeros((ncoils, npcs, N, N), dtype='complex')
    lGS = np.zeros((ncoils, N, N), dtype='complex')
    for cc in range(ncoils):
        lGS[cc, ...] = gs_recon(I[cc, ...], pc_axis=0)
        P[cc, ...] = I[cc, ...]/lGS[cc, ...]
    # view(np.angle(P.reshape((-1, N, N))), montage_axis=0)
    P = np.mean(P, axis=0)
    # view(P)

    # Use P to find magnitude of coil sensitivities by assuming that
    # the area of polygon defined by P is similar to the area of C.
    C = np.zeros((ncoils, N, N), dtype='complex')
    for cc in range(ncoils):
        for idx in np.ndindex((N, N)):
            ii, jj = idx[:]

            # Find magnitude
            est_area = PolyArea(
                P[:, ii, jj].real, P[:, ii, jj].imag)
            I00 = I[cc, :, ii, jj]
            xx, yy = I00.real, I00.imag
            C[cc, ii, jj] = 1/np.sqrt(est_area/PolyArea(xx, yy))

            # Find rotation
            rots = np.angle(lGS[cc, ii, jj]) - np.angle(I00)
            kk = np.argmax(np.abs(rots))
            rot = rots[kk]
            C[cc, ii, jj] *= np.exp(1j*rot)

            # # Take a peek
            # if np.max(np.abs(I00)) > .5:
            #     plt.plot(P[:, ii, jj].real, P[:, ii, jj].imag)
            #     scaled = I00/np.conj(C[cc, ii, jj])
            #     plt.plot(scaled.real, scaled.imag, '--')
            #     plt.show()

    # view(np.stack((C, lGS)).reshape((-1, N, N)), montage_axis=0)
    mask = PD > 0
    # Csos = sos(C*mask, axes=0)
    lGSsos = sos(lGS*mask, axes=0)
    # view(np.stack((Csos, lGSsos)))

    # view(C - lGS)
    # view(np.angle(C))
    # view(np.stack((
    #     np.abs(mps), C)).reshape((-1, N, N)), montage_axis=0)
    # view(np.abs(mps) - np.abs(C))
    # view(mps/C)

    I0 = I/(np.tile(
        P[None, ...], (ncoils, 1, 1, 1))*np.tile(
            C[:, None, ...].conj(), (1, npcs, 1, 1)))
    # I0[np.isnan(I0)] = 0
    I0 = np.mean(I0, axis=1)
    I0 = sos(I0, axes=0)*mask

    view(np.stack((I0, lGSsos)))
