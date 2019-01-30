import numpy as np

def rot(theta):
    '''2D rotation matrix through angle theta (rad).'''

    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    return R
