import numpy as np


def fd_complex_step(f,x0,h=np.finfo(float).eps):
    '''Compute forward difference complex step of function f.
    '''

    g = np.zeros(x0.shape)
    for ii in range(x0.size):
        xp = np.zeros(x0.shape,dtype='complex')
        xp[ii] = 1j*h
        g[ii] = np.imag(f(x0 + xp))/h
    return(g)
