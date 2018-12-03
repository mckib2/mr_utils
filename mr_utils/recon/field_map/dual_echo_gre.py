import numpy as np

def dual_echo_gre(m1,m2,TE1,TE2):
    '''Compute wrapped field map from two GRE images at different TEs.

    m1 -- GRE image taken with TE = TE1.
    m2 -- GRE image taken with TE = TE2.
    TE1 -- echo time corresponding to m1.
    TE2 -- echo time corresponding to m2.

    Returns field map in herz.
    '''

    fm = np.angle(np.conj(m1)*m2)/np.abs(TE1 - TE2)
    return(fm)
