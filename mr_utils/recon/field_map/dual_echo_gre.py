'''Compute field map from dual echo GRE acquisitions.'''

import numpy as np

def dual_echo_gre(m1, m2, TE1, TE2):
    '''Compute wrapped field map from two GRE images at different TEs.

    Parameters
    ==========
    m1 : array_like
        GRE image taken with TE = TE1.
    m2 : array_like
        GRE image taken with TE = TE2.
    TE1 : float
        echo time corresponding to m1.
    TE2 : float
        echo time corresponding to m2.

    Returns
    =======
    fm : array_like
        Field map in herz
    '''

    fm = np.angle(np.conj(m1)*m2)/(np.abs(TE1 - TE2)*2*np.pi)
    return fm
