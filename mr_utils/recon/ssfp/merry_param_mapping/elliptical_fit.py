'''Calculates residuals for least_squares fit.'''

import numpy as np

from mr_utils.sim.ssfp import ssfp

def ellipticalfit(Ireal, TR, dphis, offres, M0, alpha, T1, T2):
    '''ELLIPTICALFIT

    Parameters
    ==========
    Ireal : array_like
        Hermtian transposed phase-cycle values for single pixel.
    TR : float
        Repetition time.
    M0 :
        Estmated proton density from the band reduction algorithm.
    phasecycles :
        Phase-cycles (in rad).
    offres :
        Off-resonance estimation (in Hz).

    Returns
    =======
    J : array_like
        Real part of difference concatenated with imaginary part of difference
    '''

    T1 *= 100
    T2 *= 10
    offres *= 100 # in Hz
    num = dphis.size

    Mxans = np.zeros(num)
    Myans = np.zeros(num)
    for ii, dphi in np.ndenumerate(dphis):
        I = ssfp(
            T1*1e-3, T2*1e-3, TR*1e-3, alpha, offres, phase_cyc=dphi, M0=M0)

        # oposite signs because of the hermitian transpose
        Mxans[ii] = I.real - Ireal[ii].real
        Myans[ii] = I.imag + Ireal[ii].imag

    return np.hstack((Mxans, Myans))
