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

def fd_gen_complex_step(f,x0,h=0,v=np.finfo(float).eps):
    '''Compute generalized forward difference complex step derivative of f.

    f -- Function to compute derivative of at x0.
    x0 -- Point to compute derivative of f on.
    h -- Real part of forward perturbation.
    v -- Imaginary part of forward perturbation.

    Implements Equation 4 from:
        Abreu, Rafael, et al. "On the accuracy of the
        Complex-Step-Finite-Difference method." Journal of Computational and
        Applied Mathematics 340 (2018): 390-403.
    '''

    g = np.zeros(x0.shape)
    for ii in range(x0.size):
        xp = np.zeros(x0.shape,dtype='complex')
        xp[ii] = h + 1j*v
        g[ii] = np.imag(f(x0 + xp))/v
    return(g)

def cd_gen_complex_step(f,x0,h=None,v=None):
    '''Compute generalized central difference complex step derivative of f.

    f -- Function to compute derivative of at x0.
    x0 -- Point to compute derivative of f on.
    h -- Real part of forward and backward derivatives.
    v -- Imaginary part of forward and backwards derivatives.

    If you choose h,v such that 3*h**2 =/= v**2, there will be an additional
    error term proportional to 3rd order derivative (not implemented).  So
        it's in your best interest to choose h,v so this error is minimized.

    Implements Equation 5 from:
        Abreu, Rafael, et al. "On the accuracy of the
        Complex-Step-Finite-Difference method." Journal of Computational and
        Applied Mathematics 340 (2018): 390-403.
    '''

    # Choose 3h**2 -v**2 = 0 to get fourth-order error term
    if h is None and v is None:
        v = np.sqrt(np.finfo(float).eps)
        h = np.sqrt(v**2/3)
        assert 3*h**2 == v**2

    # Precompute constants
    xpf0 = h + 1j*v
    xpb0 = -h + 1j*v
    den = 2*v

    g = np.zeros(x0.shape)
    for ii in range(x0.size):
        xpf = np.zeros(x0.shape,dtype='complex')
        xpb = xpf.copy()
        xpf[ii] = xpf0
        xpb[ii] = xpb0

        g[ii] = (np.imag(f(x0 + xpf)) + np.imag(f(x0 + xpb)))/den
    return(g)

def complex_step_6th_order(f,x0,h=None,v=None):

    # Choose u,v to get 6th order error: 5*h**2 - 7*v**2 = 0
    if h is None and v is None:
        v = np.sqrt(np.finfo(float).eps)
        h = np.sqrt(7/5*v**2)
        assert 5*h**2 - 7*v**2 == 0

    # Precompute constants
    xp0 = 1j*v
    xpf0 = h + 1j*v
    xpb0 = -h + 1j*v
    c0 = (3*h**2 - v**2)/(3*h**2*v)
    c1 = v/(6*h**2)

    g = np.zeros(x0.shape)
    for ii in range(x0.size):
        xp = np.zeros(x0.shape,dtype='complex')
        xpf = xp.copy()
        xpb = xp.copy()
        xp[ii] = xp0
        xpf[ii] = xpf0
        xpb[ii] = xpb0

        g[ii] = c0*np.imag(f(x0 + xp)) + c1*(np.imag(f(x0 + xpf)) + np.imag(f(x0 + xpb)))
    return(g)

if __name__ == '__main__':
    pass
