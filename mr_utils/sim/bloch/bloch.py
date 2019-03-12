'''Numerical bloch simulations using finite difference method.'''

import numpy as np
from tqdm import trange

def rotation(alpha, beta, gamma):
    '''Create 3D rotation matrix from alpha,beta,gamma.

    Parameters
    ==========
    alpha : float
        Rotation angle about x in rad.
    beta : float
        Rotation angle about y in rad.
    gamma : float
        Rotation angle about z in rad.

    Returns
    =======
    rot : array_like
        Rotation matrix.
    '''

    ca = np.cos(alpha)
    cb = np.cos(beta)
    cg = np.cos(gamma)

    sa = np.sin(alpha)
    sb = np.sin(beta)
    sg = np.sin(gamma)

    rot = np.array([
        [ca*cb*cg - sa*sg, -ca*cb*sg - sa*cg, ca*sb],
        [sa*cb*cg + ca*sg, -sa*cb*sg + ca*cg, sa*sb],
        [-sb*cg, sb*sg, cb]
    ])

    return rot

def sim_loop(T1, T2, M0, Nt, h, alpha, beta, gamma, Bx=0, By=0, Bz=3):
    '''Loop implementation to verify matrix implementation.

    T1 : array_like
        longitudinal relaxation constant.
    T2 : array_like
        transverse relaxation constant.
    M0 : array_like
        value at thermal equilibrium.
    Nt : int
        number of time points for finite difference solution.
    h : float
        step size for finite difference solutions.
    alpha : float
        RF pulse tip angle about x.
    beta : float
        RF pulse tip angle about y.
    gamma : float
        RF pulse tip angle about z.
    Bx : float, optional
        x component of magnetic field.
    By : float, optional
        y component of magnetic field.
    Bz : float, optional
        z component of magnetic field.

    Returns
    =======
    spins : array_like
        Simulated spin vectors.
    '''

    # Initalize spins at thermal equilibrium at first time point
    spins = np.zeros((Nt, 3,) + M0.shape)
    spins[0, 2, ...] = M0

    # Aux variables to construct A matrix
    wx = Bx*np.ones(T1.shape)
    wy = By*np.ones(T1.shape)
    wz = Bz*np.ones(T1.shape)
    R1 = -1/T1
    R2 = -1/T2

    # Apply initial RF tip at each voxel
    R = rotation(alpha, beta, gamma)
    spins[0, ...] = np.tensordot(R, spins[0, ...], axes=1)

    # Do finite-difference simulation, using for loops over each voxel
    for tt in trange(1, Nt, leave=False, desc='Bloch sim'):
        for xx in range(T1.shape[0]):
            for yy in range(T1.shape[1]):
                for zz in range(T1.shape[2]):
                    A = np.array([
                        [R2[xx, yy, zz], wz[xx, yy, zz], -wy[xx, yy, zz]],
                        [-wz[xx, yy, zz], R2[xx, yy, zz], wx[xx, yy, zz]],
                        [wy[xx, yy, zz], -wx[xx, yy, zz], R1[xx, yy, zz]]
                    ])
                    spins[tt, :, xx, yy, zz] = A.dot(
                        spins[tt-1, :, xx, yy, zz])*h + \
                        spins[tt-1, :, xx, yy, zz] + \
                        np.array([0, 0, M0[xx, yy, zz]/T1[xx, yy, zz]])*h

    # # Show results for first voxel
    # plt.plot(np.sqrt(np.sum(spins[:,0:2,0,0,0]**2,axis=1)))
    # plt.plot(spins[:,2,0,0,0])
    # plt.show()
    return spins

def sim(T1, T2, M0, Nt, h, alpha, beta, gamma, Bx=0, By=0, Bz=3):
    # pylint: disable=C0301
    '''Finite difference solution to Bloch equations.

    T1 : array_like
        longitudinal relaxation constant.
    T2 : array_like
        transverse relaxation constant.
    M0 : array_like
        value at thermal equilibrium.
    Nt : int
        number of time points for finite difference solution.
    h : float
        step size for finite difference solutions.
    alpha : float
        RF pulse tip angle about x.
    beta : float
        RF pulse tip angle about y.
    gamma : float
        RF pulse tip angle about z.
    Bx : float, optional
        x component of magnetic field.
    By : float, optional
        y component of magnetic field.
    Bz : float, optional
        z component of magnetic field.

    Returns
    =======
    spins : array_like
        Simulated spin vectors.

    Notes
    =====
    T1, T2, M0 can be arrays (must be same size) to simulate phantoms.

    See [1]_ for matrix form of Bloch equations.

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Bloch_equations#Matrix_form_of_Bloch_equations
    '''
    # pylint: enable=C0301

    # Initalize spins at thermal equilibrium at first time point
    spins = np.zeros((Nt, 3,) + M0.shape)
    spins[0, 2, ...] = M0

    # Aux variables to construct A matrix
    wx = Bx*np.ones(T1.shape)
    wy = By*np.ones(T1.shape)
    wz = Bz*np.ones(T1.shape)
    R1 = -1/T1
    R2 = -1/T2
    zfac = h*M0/T1

    # Apply initial RF tip at each voxel
    R = rotation(alpha, beta, gamma)
    spins[0, ...] = np.tensordot(R, spins[0, ...], axes=1)

    # Calculate constant A
    A = np.array([
        [R2, wz, -wy],
        [-wz, R2, wx],
        [wy, -wx, R1]
    ])

    # Do finite-difference simulation
    for tt in trange(1, Nt, leave=False, desc='Bloch sim'):
        spins[tt, ...] = np.einsum('ijxyz,jxyz->ixyz', A, spins[tt-1, ...])*h \
                                   + spins[tt-1, ...]
        spins[tt, 2, ...] += zfac

    return spins

def gre(T1, T2, M0, Nt, h, alpha, beta, gamma, TR, TE, Bx=0, By=0, Bz=3):
    '''Finite difference Bloch simulation of spoiled GRE pulse sequence.

    T1 : array_like
        longitudinal relaxation constant.
    T2 : array_like
        transverse relaxation constant.
    M0 : array_like
        value at thermal equilibrium.
    Nt : int
        number of time points for finite difference solution.
    h : float
        step size for finite difference solutions.
    alpha : float
        RF pulse tip angle about x.
    beta : float
        RF pulse tip angle about y.
    gamma : float
        RF pulse tip angle about z.
    TR : float
        repetition time.
    TE : float
        echo time.
    Bx : float, optional
        x component of magnetic field.
    By : float, optional
        y component of magnetic field.
    Bz : float, optional
        z component of magnetic field.

    Returns
    =======
    spins : array_like
        Simulated spin vectors.

    Notes
    =====
    T1, T2, M0 can be arrays (must be same size) to simulate phantoms.
    '''

    # Initalize
    spins = np.zeros((3,) + M0.shape)
    spins[2, ...] = M0

    # Initial tip
    R = rotation(alpha, beta, gamma)
    spins = np.tensordot(R, spins, axes=1)

    # Aux variables
    wx = Bx*np.ones(T1.shape)
    wy = By*np.ones(T1.shape)
    wz = Bz*np.ones(T1.shape)
    R1 = -1/T1
    R2 = -1/T2
    zfac = h*M0/T1

    # Bloch equation matrix, A
    A = np.array([
        [R2, wz, -wy],
        [-wz, R2, wx],
        [wy, -wx, R1]
    ])

    # Split into TRs
    num_TRs = int(Nt*h/TR)
    # print('num_TRs: %g' % num_TRs)

    # Split TRs into TEs
    num_before_TE = int(TE/TR*num_TRs)
    # print('num_before_TE: %g' % num_before_TE)

    num_iters_per_TR = np.around(Nt/num_TRs).astype(int)
    # print('Nt/num_TRs: %g' % num_iters_per_TR)

    # Do all TRs but the last one
    for _tr in trange(num_TRs-1, leave=False, desc='GRE Bloch Sim'):

        # Relaxation
        for _tt in range(num_iters_per_TR):
            spins += np.einsum('ijxyz,jxyz->ixyz', A, spins)*h
            spins[2, ...] += zfac

        # Spoil
        spins[0:2, ...] = 0

        # Next tip
        spins = np.tensordot(R, spins, axes=1)

    # Now readout at TE during last TR
    for _tt in range(num_before_TE):
        # Relaxation
        spins += np.einsum('ijxyz,jxyz->ixyz', A, spins)*h
        spins[2, ...] += zfac


    return spins

if __name__ == '__main__':
    pass
