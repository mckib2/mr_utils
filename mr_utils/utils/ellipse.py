'''General functions for working with ellipses.'''

import logging

import numpy as np
from scipy.optimize import leastsq

def get_semiaxes(c):
    '''Solve for semi-axes of the cartesian form of the ellipse equation.

    c -- Coefficients of general quadratic polynomial function for conic funs.

    See:
        https://en.wikipedia.org/wiki/Ellipse
    '''
    A, B, C, D, E, F = c[:]
    B2 = B**2
    den = B2 - 4*A*C
    num = 2*(A*E**2 + C*D**2 - B*D*E + den*F)
    num *= (A + C + np.array([1, -1])*np.sqrt((A - C)**2 + B2))
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

def check_fit(C, x, y):
    '''General quadratic polynomial function.

    C -- coefficients.
    x, y -- Coordinates assumed to be on ellipse.

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
    x = x.flatten()
    y = y.flatten()
    return C[0]*x**2 + C[1]*x*y + C[2]*y**2 + C[3]*x + C[4]*y + C[5]

def fit_ellipse_halir(x, y):
    '''Python port of improved ellipse fitting algorithm by Halir and Flusser.

    x, y -- Coordinates assumed to be on ellipse.

    Note that there should be at least 6 pairs of (x,y).

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

    # We should just have a bunch of points, so we can shape it into a column
    # vector since shape doesn't matter
    x = x.flatten()
    y = y.flatten()

    # Make sure we have at least 6 points (6 unknowns...)
    if x.size < 6 and y.size < 6:
        logging.warning('We need at least 6 sample points for a good fit!')

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

def fit_ellipse_fitzgibon(x, y):
    '''Python port of direct ellipse fitting algorithm by Fitzgibon et. al.

    x, y -- Coordinates assumed to be on ellipse.

    See Figure 1 from:
        Halır, Radim, and Jan Flusser. "Numerically stable direct least squares
        fitting of ellipses." Proc. 6th International Conference in Central
        Europe on Computer Graphics and Visualization. WSCG. Vol. 98. 1998.

    Also see previous python port:
        http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
    '''

    # Like a pancake...
    x = x.flatten()
    y = y.flatten()

    # Make sure we have at least 6 points (6 unknowns...)
    if x.size < 6 and y.size < 6:
        logging.warning('We need at least 6 sample points for a good fit!')

    # Do the thing
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    D = np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x))) # Design matrix
    S = np.dot(D.T, D) # Scatter matrix
    C = np.zeros([6, 6]) # Constraint matrix
    C[(0, 2), (0, 2)] = 2
    C[1, 1] = -1
    E, V = np.linalg.eig(np.dot(np.linalg.inv(S), C)) # solve eigensystem
    n = np.argmax(np.abs(E)) # find positive eigenvalue
    a = V[:, n].squeeze() # corresponding eigenvector
    return a

def fit_ellipse_nonlin(x, y, polar=False):
    '''Fit ellipse only depending on semi-major axis and eccentricity.

    x, y -- Coordinates assumed to be on ellipse.
    polar -- Whether or not coordinates are provided as polar or Cartesian.

    Note that if polar=True, then x will be assumed to be radius and y will be
    assumed to be theta.

    See:
        https://scipython.com/book/chapter-8-scipy/examples/
        non-linear-fitting-to-an-ellipse/
    '''

    # Convert cartesian coordinates to polar
    if not polar:
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
    else:
        r = x
        theta = y

    def f(theta, p):
        '''Ellipse function.'''
        a, e = p
        return a * (1 - e**2)/(1 - e*np.cos(theta))

    def residuals(p, r, theta):
        '''Return the observed - calculated residuals using f(theta, p).'''
        return r - f(theta, p)

    def jac(p, _r, theta):
        '''Calculate and return the Jacobian of residuals.'''
        a, e = p
        ct = np.cos(theta)
        ect = e*ct
        e2 = e**2
        da = (1 - e2)/(1 - ect)
        de = (-2*a*e*(1 - ect) + a*(1 - e2)*ct)/(1 - ect)**2
        return(-da, -de)

    p0 = (1, 0.5)
    plsq = leastsq(residuals, p0, Dfun=jac, args=(r, theta), col_deriv=True)
    # print(plsq[0])

    # import matplotlib.pyplot as plt
    # plt.polar(theta, r, 'x')
    # theta_grid = np.linspace(0, 2*np.pi, 200)
    # plt.polar(theta_grid, f(theta_grid, plsq[0]), lw=2)
    # plt.show()

    # Return a, e
    return plsq[0]
