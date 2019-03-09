'''Calculates residuals for least_squares fit.'''

import numpy as np

from mr_utils.sim.ssfp import ssfp

def ellipticalfit(Ireal, TR, dphis, offres, M0, alpha, T1, T2):
    '''ELLIPTICALFIT

    Ireal - complex pixel hermtian transposed
    TE - echo time
    TR - repetition time
    M0 - estmated from the band reduction algorithm
    phasecycles- phase cycle angles
    offres- offresonance profile
    output- J: real part of difference, imaginary part of the difference
    g gradients
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
