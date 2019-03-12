'''Spin echo simulation.'''

import numpy as np

def se90(T1, T2, TR, TE, M0=1):
    '''Spin echo simulation assuming 90 deg flip angle

    Parameters
    ==========
    T1 : array_like
        longitudinal relaxation time.
    T2 : array_like
        transverse relaxation time.
    TR : float
        repetition time.
    TE : float
        echo time
    M0 : array_like, optional
        Proton density.

    Returns
    =======
    S : array_like
        Simulated magnitude spin echo image.
    '''

    S = M0*(1 - np.exp(-TR/T1))*np.exp(-TE/T2)
    return S
