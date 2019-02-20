'''Ellipse fitting functions.'''

import numpy as np


def get_semiaxes(c):
    '''Solve for semi-axes of the cartesian form of the ellipse equation.

    c -- Coefficients of general quadratic polynomial function for conic funs.

    See:
        https://en.wikipedia.org/wiki/Ellipse
    '''
    A, B, C, D, E, F = c[:]
    num = 2*(A*E**2 + C*D**2 - B*D*E + (B**2 - 4*A*C)*F)
    num *= (A + C + np.array([1, -1])*np.sqrt((A - C)**2 + B**2))
    den = B**2 - 4*A*C
    AB = -1*np.sqrt(num)/den

    # Return semi-major axis first
    if AB[0] > AB[1]:
        return(AB[1], AB[0])
    return(AB[0], AB[1])


def get_center(c):
    '''Compute center of ellipse from implicit function coefficients.

    c -- Coefficients of general quadratic polynomial function for conic funs.
    '''
    A, B, C, D, E, _F = c[:]
    den = B**2 - 4*A*C
    xc = (2*C*D - B*E)/den
    yc = (2*A*E - B*D)/den
    return(xc, yc)

def rotate_coefficients(c, phi):
    '''Rotate coefficients of implicit equations through angle phi.

    c -- Coefficients of general quadratic polynomial function for conic funs.
    phi -- Angle in radians to rotate ellipse.

    See:
        http://www.mathamazement.com/Lessons/Pre-Calculus/
        09_Conic-Sections-and-Analytic-Geometry/rotation-of-axes.html
    '''
    cp, c2p = np.cos(phi), np.cos(2*phi)
    sp, s2p = np.sin(phi), np.sin(2*phi)
    A, B, C, D, E, F = c[:]
    Ar = (A + C + (A - C)*c2p - B*s2p)/2
    Br = (A - C)*s2p + B*c2p
    Cr = (A + C + (C - A)*c2p + B*s2p)/2
    Dr = D*cp - E*sp
    Er = D*sp + E*cp
    return np.array([Ar, Br, Cr, Dr, Er, F])

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
