'''Calculates residuals for least_squares fit.'''

import numpy as np

from mr_utils.recon.ssfp.merry_param_mapping.ssfp_fit import SSFPfit

def ellipticalfit(Ireal, TE, TR, dphi, offres, M0, alpha, T1, T2):
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
    num = dphi.size

    Mxans = np.zeros(num)
    Myans = np.zeros(num)
    for k in range(num):
        # [Mx0(k,n), My0(k,n), a0(k,n), b0(k,n), M_0(k,n)] = SSFPfit(T1(k,n),
        # T2(k,n), TR, TE, alpha(k,n), 0, offres(k,n),M0(k,n));
        Mx, My, _, _, _ = SSFPfit(T1, T2, TR, TE, alpha, dphi[k], offres, M0)
        I = Mx + 1j*My

        # oposite signs because of the hermitian transpose
        # print(I.shape, print(Ireal.shape))
        Mxans[k] = np.real(I) - np.real(Ireal[k])
        Myans[k] = np.imag(I) + np.imag(Ireal[k])

    # J=(norm([Mxans Myans])); %for fmincon
    J = np.hstack((Mxans, Myans)) # for lsqnonlin

    return J
