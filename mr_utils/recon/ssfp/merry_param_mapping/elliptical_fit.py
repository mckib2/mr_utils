'''Calculates residuals for least_squares fit.'''

from ctypes import c_double

# import numpy as np

from mr_utils.sim.ssfp import ssfp

def ellipticalfit(Ireal, TR, dphis, offres, M0, alpha, T1, T2):
    '''ELLIPTICALFIT

    Parameters
    ==========
    Ireal : array_like
        Hermtian transposed phase-cycle values for single pixel.
    TR : float
        Repetition time (in sec).
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

    I = ssfp(T1, T2, TR, alpha, offres, phase_cyc=dphis, M0=M0)
    return (I - Ireal).view(dtype=c_double)


    # for ii, dphi in np.ndenumerate(dphis):
    #     I = ssfp(
    #         T1, T2, TR, alpha, offres, phase_cyc=dphi, M0=M0)
    #
    #     # oposite signs because of the hermitian transpose
    #     Mxans[ii] = I.real - Ireal[ii].real
    #     Myans[ii] = I.imag - Ireal[ii].imag
    #
    # return np.hstack((Mxans, Myans))
