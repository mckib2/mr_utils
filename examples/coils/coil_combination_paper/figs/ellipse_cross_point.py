'''Show that the direct solution is the cross point.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import gs_recon

if __name__ == '__main__':

    T1 = 1.2
    T2 = .035
    M0 = 1
    TR = 3e-3
    df = 1/(3*TR)
    rf = 0
    alpha = np.deg2rad(10)
    npcs = 4
    pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
    epcs = np.linspace(0, 2*np.pi, 200)
    E = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=epcs, M0=M0, phi_rf=rf)
    I = ssfp(
        T1, T2, TR, alpha, df, phase_cyc=pcs, M0=M0, phi_rf=rf)
    M = gs_recon(I)

    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)

    # Make ellipse outline
    plt.plot(E.real, E.imag, ':k', label='Ellipse')

    # Add and label acquired phase-cycles
    plt.plot(I.real, I.imag, 'xk', label='Phase cycle')
    for ii in range(npcs):
        plt.text(I[ii].real*1.05, I[ii].imag, '%d°' % (ii*90))

    # Get cross lines
    plt.plot(I[0::2].real, I[0::2].imag, 'k-')
    plt.plot(I[1::2].real, I[1::2].imag, 'k-')

    # Add the cross-point
    plt.plot(M.real, M.imag, 'ok', label='$I_d$')
    # plt.text(M.real, M.imag, 'I_d')

    plt.title('Geometric Solution')
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')
    plt.legend()
    plt.axis('square')
    plt.show()
