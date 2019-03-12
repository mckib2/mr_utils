'''Inversion recovery pulse sequence simulation.'''

import numpy as np

def ir90(T1, TR, TI, M0=1):
    '''Inversion recovery simulation with 90 deg flig angle.

    Parameters
    ==========
    T1 : array_like
        longitudinal exponential decay time constant.
    TR : float
        repetition time.
    TI : float
        inversion time.
    M0 : array_like, optional
        proton density.

    Returns
    =======
    S : array_like
        Simulated magnitude image.
    '''
    S = M0*(1 - 2*np.exp(-TI/T1) + np.exp(-TR/T1))
    return S
