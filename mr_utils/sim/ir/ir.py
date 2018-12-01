import numpy as np

def ir90(T1,TI,M0=1):
    '''Inversion recovery simulation with 90 deg flig angle.

    T1 -- longitudinal exponential decay time constant.
    TI -- inversion time.
    M0 -- proton density.
    '''
    S = M0*(1 - 2*np.exp(-TI/T1) + np.exp(-TR/T1))
    return(S)
