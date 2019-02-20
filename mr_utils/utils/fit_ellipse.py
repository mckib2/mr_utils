'''Ellipse fitting functions.'''

import numpy as np

def check_fit(C, I):
    '''General quadratic polynomial function.

    C -- coefficients.
    I -- Complex voxels.

    We want this to equal 0 for a good ellipse fit.   This polynomial is called
    the algebraic distance of the point (x, y) to the given conic.

    See:
        Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
        simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
        free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.

        Halır, Radim, and Jan Flusser. "Numerically stable direct least squares
        fitting of ellipses." Proc. 6th International Conference in Central
        Europe on Computer Graphics and Visualization. WSCG. Vol. 98. 1998.
    '''
    x = I.real
    y = I.imag
    return C[0]*x**2 + C[1]*x*y + C[2]*y**2 + C[3]*x + C[4]*y + C[5]

def fit_ellipse(I):
    '''Python port of improved ellipse fitting algorithm.

    I -- Complex voxels from 6 phase-cycled bSSFP images.

    From the paper's conclusion:
        "Due to its systematic bias, the proposed fitting algorithm cannot be
        used directly in applications where excellent accuracy of the fitting
        is required. But even in that applications our method can be useful as
        a fast and robust estimator of a good initial solution of the fitting
        problem..."

    See figure 2 from:
        Halır, Radim, and Jan Flusser. "Numerically stable direct least squares
        fitting of ellipses." Proc. 6th International Conference in Central
        Europe on Computer Graphics and Visualization. WSCG. Vol. 98. 1998.
    '''

    # We should just have a bunch of phase-cycles of the same voxel, so make
    # it into a column vector since shape doesn't matter
    I = I.flatten()

    # Make sure we have at least 6 phase-cycles (6 unknowns...)
    assert I.size >= 6, 'We need at least 6 phase-cycles!'

    # Behold, the complex plane
    x = I.real
    y = I.imag

    # Here's the heavy lifting
    D1 = np.stack((x**2, x*y, y**2)).T # quadratic part of the design matrix
    D2 = np.stack((x, y, np.ones(x.size))).T # linear part of the design matrix
    S1 = np.dot(D1.T, D1) # quadratic part of the scatter matrix
    S2 = np.dot(D1.T, D2) # combined part of the scatter matrix
    S3 = np.dot(D2.T, D2) # linear part of the scatter matrix
    T = -1*np.linalg.inv(S3).dot(S2.T) # for getting a2 from a1
    M = S1 + S2.dot(T) # reduced scatter matrix
    M = np.array([M[2, :]/2, -1*M[1, :], M[0, :]/2]) # premultiply by inv(C1)
    _eval, evec = np.linalg.eig(M) # solve eigensystem
    cond = 4*evec[0, :]*evec[2, :] - evec[1, :]**2 # evaluate a’Ca
    a1 = evec[:, cond > 0] # eigenvector for min. pos. eigenvalue
    a = np.vstack([a1, T.dot(a1)]).squeeze() # ellipse coefficients
    return a
