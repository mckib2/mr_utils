'''Rotation matrices.'''

import numpy as np

def rot(theta):
    '''2D rotation matrix through angle theta (rad).

    Parameters
    ==========
    theta : float
        Angle in rad to rotate.

    Returns
    =======
    R : array_like
        Rotation matrix.
    '''

    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    return R
