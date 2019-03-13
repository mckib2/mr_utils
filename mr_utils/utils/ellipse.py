'''General functions for working with ellipses.'''

import logging

import numpy as np
from scipy.optimize import leastsq

def get_semiaxes(c):
    '''Solve for semi-axes of the cartesian form of the ellipse equation.

    Parameters
    ==========
    c : array_like
        Coefficients of general quadratic polynomial function for conic funs.

    Returns
    =======
    float
        Semi-major axis
    float
        Semi-minor axis

    Notes
    =====
    https://en.wikipedia.org/wiki/Ellipse
    '''
    A, B, C, D, E, F = c[:]
    B2 = B**2
    den = B2 - 4*A*C
    num = 2*(A*E**2 + C*D**2 - B*D*E + den*F)
    num *= (A + C + np.array([1, -1])*np.sqrt((A - C)**2 + B2))
    AB = -1*np.sqrt(num)/den

    # # Return semi-major axis first
    # if AB[0] > AB[1]:
        # print(AB)
        # return(AB[1], AB[0])
    return(AB[0], AB[1])

def get_center(c):
    '''Compute center of ellipse from implicit function coefficients.

    Parameters
    ==========
    c : array_like
        Coefficients of general quadratic polynomial function for conic funs.

    Returns
    =======
    xc : float
        x coordinate of center.
    yc : float
        y coordinate of center.
    '''
    A, B, C, D, E, _F = c[:]
    den = B**2 - 4*A*C
    xc = (2*C*D - B*E)/den
    yc = (2*A*E - B*D)/den
    return(xc, yc)

def rotate_points(x, y, phi, p=(0, 0)):
    '''Rotate points x, y through angle phi w.r.t. point p.

    Parameters
    ==========
    x : array_like
        x coordinates of points to be rotated.
    y : array_like
        y coordinates of points to be rotated.
    phi : float
        Angle in radians to rotate points.
    p : tuple, optional
        Point to rotate around.

    Returns
    =======
    xr : array_like
        x coordinates of rotated points.
    yr : array_like
        y coordinates of rotated points.
    '''
    x = x.flatten()
    y = y.flatten()
    xr = (x - p[0])*np.cos(phi) - (y - p[0])*np.sin(phi) + p[0]
    yr = (y - p[1])*np.cos(phi) + (x - p[1])*np.sin(phi) + p[1]
    return(xr, yr)

def rotate_coefficients(c, phi):
    '''Rotate coefficients of implicit equations through angle phi.

    Parameters
    ==========
    c : array_like
        Coefficients of general quadratic polynomial function for conic funs.
    phi : float
        Angle in radians to rotate ellipse.

    Returns
    =======
    array_like
        Coefficients of rotated ellipse.

    Notes
    =====
    http://www.mathamazement.com/Lessons/Pre-Calculus/09_Conic-Sections-and-Analytic-Geometry/rotation-of-axes.html
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

def do_planet_rotation(I):
    '''Rotate complex points to fit vertical ellipse centered at (xc, 0).

    Parameters
    ==========
    I : array_like
        Complex points from SSFP experiment.

    Returns
    =======
    xr : array_like
        x coordinates of rotated points.
    yr : array_like
        y coordinates of rotated points.
    cr : array_like
        Coefficients of rotated ellipse.
    phi : float
        Rotation angle in radians of effective rotation to get ellipse vertical
        and in the x > 0 half plane.
    '''

    # Represent complex number in 2d plane
    x = I.real.flatten()
    y = I.imag.flatten()

    # Fit ellipse and find initial guess at what rotation will make it
    # vertical with center at (xc, 0).  The arctan term rotates the ellipse
    # to be horizontal, then we need to decide whether to add +/- 90 degrees
    # to get it vertical.  We want xc to be positive, so we must choose the
    # rotation to get it vertical.
    c = fit_ellipse_halir(x, y)
    phi = -.5*np.arctan2(c[1], (c[0] - c[2])) + np.pi/2
    xr, yr = rotate_points(x, y, phi)

    # If xc is negative, then we chose the wrong rotation! Do -90 deg
    cr = fit_ellipse_halir(xr, yr)
    if get_center(cr)[0] < 0:
        # print('X IS NEGATIVE!')
        phi = -.5*np.arctan2(c[1], (c[0] - c[2])) - np.pi/2
        xr, yr = rotate_points(x, y, phi)

    # Fit the rotated ellipse and bring yc to 0
    cr = fit_ellipse_halir(xr, yr)
    yr -= get_center(cr)[1]
    cr = fit_ellipse_halir(xr, yr)
    # print(get_center(cr))

    # With noisy measurements, sometimes the fit is incorrect in the above
    # steps and the ellipse ends up horizontal.  We can realize this by finding
    # the major and minor semiaxes of the ellipse.  The first axis returned
    # should be the smaller if we were correct, if not, do above steps again
    # with an extra factor of +/- 90 deg to get the ellipse standing up
    # vertically.
    ax = get_semiaxes(c)
    if ax[0] > ax[1]:
        # print('FLIPPITY FLOPPITY!')
        xr, yr = rotate_points(x, y, phi + np.pi/2)
        cr = fit_ellipse_halir(xr, yr)
        if get_center(cr)[0] < 0:
            # print('X IS STILL NEGATIVE!')
            phi -= np.pi/2
            xr, yr = rotate_points(x, y, phi)
        else:
            phi += np.pi/2

        cr = fit_ellipse_halir(xr, yr)
        yr -= get_center(cr)[1]
        cr = fit_ellipse_halir(xr, yr)
        # print(get_center(cr))

    return(xr, yr, cr, phi)

def check_fit(C, x, y):
    '''General quadratic polynomial function.

    Parameters
    ==========
    C : array_like
        coefficients.
    x : array_like
        x coordinates assumed to be on ellipse.
    y : array_like
        y coordinates assumed to be on ellipse.

    Returns
    =======
    float
        Measure of how well the ellipse fits the points (x, y).

    Notes
    =====
    We want this to equal 0 for a good ellipse fit.   This polynomial is called
    the algebraic distance of the point (x, y) to the given conic.

    This equation is referenced in [1]_ and [2]_.

    References
    ==========
    .. [1] Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
           simultaneous T1 and T2 mapping using phase‐cycled balanced
           steady‐state free precession." Magnetic resonance in medicine 79.2
           (2018): 711-722.

    .. [2] Halır, Radim, and Jan Flusser. "Numerically stable direct least
           squares fitting of ellipses." Proc. 6th International Conference in
           Central Europe on Computer Graphics and Visualization. WSCG. Vol.
           98. 1998.
    '''
    x = x.flatten()
    y = y.flatten()
    return C[0]*x**2 + C[1]*x*y + C[2]*y**2 + C[3]*x + C[4]*y + C[5]

def fit_ellipse_halir(x, y):
    '''Python port of improved ellipse fitting algorithm by Halir and Flusser.

    Parameters
    ==========
    x : array_like
        y coordinates assumed to be on ellipse.
    y : array_like
        y coordinates assumed to be on ellipse.

    Returns
    =======
    array_like
        Ellipse coefficients.

    Notes
    =====
    Note that there should be at least 6 pairs of (x,y).

    From the paper's conclusion:

        "Due to its systematic bias, the proposed fitting algorithm cannot be
        used directly in applications where excellent accuracy of the fitting
        is required. But even in that applications our method can be useful as
        a fast and robust estimator of a good initial solution of the fitting
        problem..."

    See figure 2 from [2]_.
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

    Parameters
    ==========
    x : array_like
        y coordinates assumed to be on ellipse.
    y : array_like
        y coordinates assumed to be on ellipse.

    Returns
    =======
    array_like
        Ellipse coefficients.

    Notes
    =====
    See Figure 1 from [2]_.

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

    Parameters
    ==========
    x : array_like
        y coordinates assumed to be on ellipse.
    y : array_like
        y coordinates assumed to be on ellipse.
    polar : bool, optional
        Whether or not coordinates are provided as polar or Cartesian.

    Returns
    =======
    a : float
        Semi-major axis
    e : float
        Eccentricity

    Notes
    =====
    Note that if polar=True, then x will be assumed to be radius and y will be
    assumed to be theta.

    See:
    https://scipython.com/book/chapter-8-scipy/examples/non-linear-fitting-to-an-ellipse/
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
