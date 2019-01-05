import numpy as np

def binary_smiley(N):
    '''Binary smiley face numerical phantom.

    N -- Height and width in pixels.
    '''

    smiley = np.zeros((N,N))

    # make circle for head
    radius = 0.75
    x,h = np.linspace(-1,1,N,retstep=True)
    X,Y = np.meshgrid(x,x)
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

    return(smiley)
