'''Show effects on ellipse of lin and nonlin coil combine.'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from sigpy.mri import birdcage_maps

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon #, compute_Iw
from mr_utils.test_data.phantom import cylinder_2d
from mr_utils.coils.coil_combine import gcc, walsh

if __name__ == '__main__':


    # Generate bSSFP data
    N = 64
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    nepcs = 200
    epcs = np.linspace(0, 2*np.pi, nepcs, endpoint=False)
    assert not np.mod(nepcs, 4)
    ncoils = 2 # only 2 so we don't get too cluttered
    mps = birdcage_maps((ncoils, N, N))
    TR = 3e-3
    alpha = np.deg2rad(30)
    df = _, df = np.meshgrid(
        np.linspace(-1/TR, 1/TR, N),
        np.linspace(-1/TR, 1/TR, N))
    radius = .9
    PD, T1s, T2s = cylinder_2d(dims=(N, N), radius=radius)

    # Simulate the acquisition
    I = np.zeros((ncoils, npcs, N, N), dtype='complex')
    E = np.zeros((ncoils, nepcs, N, N), dtype='complex')
    for cc in range(ncoils):
        rf = np.angle(mps[cc, ...])
        I[cc, ...] = np.abs(mps[cc, ...])*ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=rf)
        E[cc, ...] = np.abs(mps[cc, ...])*ssfp(
            T1s, T2s, TR, alpha, df, phase_cyc=epcs, M0=PD, phi_rf=rf)
    Iref = ssfp(
        T1s, T2s, TR, alpha, df, phase_cyc=pcs, M0=PD, phi_rf=0)

    # Pick one pixel to look at the ellipses
    x, y = int(N/4), int(3*N/4)

    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)

    # Before coil combine
    nx, ny = 1, 3
    alpha = .6
    plt.subplot(nx, ny, 1)
    for cc in range(ncoils):
        I0 = I[cc, :, x, y]
        E0 = E[cc, :, x, y]
        plt.plot(E0.real, E0.imag, ':k', alpha=alpha)
        plt.plot(I0.real, I0.imag, 'xk')
    plt.title('Coil Ellipses')
    plt.axis('square')
    plt.ylabel('Imag')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    # Now do GCC
    Igcc = np.zeros((npcs, N, N), dtype='complex')
    Egcc = np.zeros((nepcs, N, N), dtype='complex')
    for ii in range(npcs):
        Igcc[ii, ...] = gcc(I[:, ii, ...], vcoils=1, coil_axis=0)
    for ii in trange(nepcs, leave=False):
        Egcc[ii, ...] = gcc(E[:, ii, ...], vcoils=1, coil_axis=0)

    Igcc0 = Igcc[:, x, y]
    Egcc0 = Egcc[:, x, y]
    plt.subplot(nx, ny, 2)
    plt.plot(Egcc0.real, Egcc0.imag, ':k', alpha=alpha)
    plt.plot(Igcc0.real, Igcc0.imag, 'ok')

    # Number the points and connect them
    for ii in range(npcs):
        plt.text(
            Igcc0[ii].real + .05, Igcc0[ii].imag, '%d°' % (ii*90))
    plt.plot(Igcc0[0::2].real, Igcc0[0::2].imag, '-k')
    plt.plot(Igcc0[1::2].real, Igcc0[1::2].imag, '-k')

    plt.title('Ellipse from GCC')
    plt.axis('square')
    plt.xlabel('Real')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    # Now try Walsh - do for all ellipse, unwrap, and then pick out
    # the correct phase-cycles
    Ewalsh = np.zeros((nepcs, N, N), dtype='complex')
    for ii in trange(nepcs, leave=False):
        Ewalsh[ii, ...] = np.sum(
            walsh(E[:, ii, ...], coil_axis=0).conj()*E[:, ii, ...],
            axis=0)

    plt.subplot(nx, ny, 3)
    Ewalsh0 = Ewalsh[:, x, y]

    # Unwrap : we know we're going around an ellipse
    prev = Ewalsh0[0] # force the first one to flip
    tol = 1 # adjust until ellipse is unwrapped
    for ii in range(nepcs):
        val = np.abs(Ewalsh0[ii] - prev)
        print(val) # look to see where tol should be set
        if val > tol:
            Ewalsh0[ii] *= np.exp(-1j*np.pi)
        prev = Ewalsh0[ii]
    skip = int(nepcs/4)
    Iwalsh0 = Ewalsh0[::skip]

    plt.plot(Ewalsh0.real, Ewalsh0.imag, ':k', alpha=alpha)
    plt.plot(Iwalsh0.real, Iwalsh0.imag, 'xk')

    # Show phase-cycles and cross lines
    for ii in range(npcs):
        plt.text(
            Iwalsh0[ii].real + .05, Iwalsh0[ii].imag, '%d°' % (ii*90))
    plt.plot(Iwalsh0[0::2].real, Iwalsh0[0::2].imag, '-k')
    plt.plot(Iwalsh0[1::2].real, Iwalsh0[1::2].imag, '-k')

    # # Get the true weights
    # Id = gs_recon(Iref, pc_axis=0, second_pass=False)
    # _, w0 = compute_Iw(
    #     Iref[0, ...], Iref[2, ...], Id, ret_weight=True)
    # _, w1 = compute_Iw(
    #     Iref[1, ...], Iref[3, ...], Id, ret_weight=True)
    #
    # Iw02 = Iwalsh[0, ...]*w0 + Iwalsh[2, ...]*(1 - w0)
    # Iw13 = Iwalsh[1, ...]*w1 + Iwalsh[3, ...]*(1 - w1)
    # Iwalsh_lGS = (Iw02 + Iw13)/2
    # print(Iwalsh_lGS.shape)
    # Iwalsh_lGS0 = Iwalsh_lGS[x, y]
    # plt.plot(Iwalsh_lGS0.real, Iwalsh_lGS0.imag, 'o')

    # Plot the cross point from Walsh
    Mwalsh = gs_recon(Iwalsh0, pc_axis=0)
    plt.plot(Mwalsh.real, Mwalsh.imag, 'ok')

    # # Plot the true cross point
    # M = gs_recon(Iref[:, x, y], pc_axis=0)
    # plt.plot(M.real, M.imag, 'x', label='$I_d$')
    #
    # # plt.plot(np.abs(M), 0, 'o')
    # # plt.plot(np.abs(Mwalsh), 0, 'x')

    plt.title('Ellipse from SMF')
    plt.axis('square')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.show()
