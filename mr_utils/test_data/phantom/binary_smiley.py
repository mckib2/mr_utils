'''Simple numerical phantom shaped like a smiley face.  Value either 1 or 0.'''

import numpy as np

def binary_smiley(N, radius=.75):
    '''Binary smiley face numerical phantom.

    Parameters
    ==========
    N : int
        Height and width in pixels.
    radius : float, optional
        Radius of circle used for head.

    Returns
    =======
    smiley : array_like
        Binary image of a smiley face.
    '''

    smiley = np.zeros((N, N))

    # make circle for head
    x, _h = np.linspace(-1, 1, N, retstep=True)
    X, Y = np.meshgrid(x, x)
    idx = np.sqrt(X**2 + Y**2) < radius
    smiley[idx] = 1

    # Make some eyes
    idx = X > radius*1/4
    idx &= X < radius*1/4 + .05
    idx |= X < -radius*1/4
    idx &= X > -radius*1/4 - .05
    idx &= Y > -radius*1/2
    idx &= Y < -radius*1/5
    smiley[idx] = 0

    # Make a mouth
    idx = X > -1/2*radius
    idx &= X < 1/2*radius
    idx &= Y > 1/2*radius
    idx &= Y < 1/2*radius + .05
    smiley[idx] = 0

    return smiley
