import numpy as np

def se90(T1,T2,TR,TE,M0=1):
    '''Spin echo simulation assuming 90 deg flip angle
    '''

    S = M0*(1 - np.exp(-TR/T1))*np.exp(-TE/T2)
    return(S)
