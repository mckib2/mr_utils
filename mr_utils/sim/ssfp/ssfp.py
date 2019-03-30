'''SSFP constrast simulation functions.'''

import numpy as np
# import matplotlib.pyplot as plt

def ssfp_old(T1, T2, TR, alpha, field_map, phase_cyc=0, M0=1):
    '''Legacy SSFP sim code.  Try using current SSFP function.'''

    theta = get_theta(TR, field_map, phase_cyc)
    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    ct = np.cos(theta)
    st = np.sin(theta)

    # If field_map and T1 or T2 are matrices, then we need to do
    # matrix operations.
    if (np.array([T1, T2]).size > 2) and (
            np.array(field_map).size > 1):

        den = (1 - E1*ca)[:, None]*(1 - np.outer(E2, ct)) \
            - (E2*(E1 - ca))[:, None]*(E2[:, None] - ct)
        Mx = M0*((1 - E1)*sa)[:, None]*(1 - np.outer(E2, ct))/den
        My = -M0*np.outer((1 - E1)*E2*sa, st)/den
        Mxy = Mx + 1j*My
    else:
        den = (1 - E1*ca)*(1 - E2*ct) - E2*(E1 - ca)*(E2 - ct)
        Mx = M0*(1 - E1)*sa*(1 - E2*ct)/den
        My = -M0*(1 - E1)*E2*sa*st/den
        Mxy = Mx + 1j*My

        Mxy *= get_bssfp_phase(T2, TR, field_map)
    return Mxy

def ssfp(T1, T2, TR, alpha, field_map, phase_cyc=0, M0=1, delta_cs=0,
         phi_rf=0, phi_edd=0, phi_drift=0):
    r'''SSFP transverse signal at time TE after excitation.

    Parameters
    ----------
    T1 : float or array_like
        longitudinal exponential decay time constant (in seconds).
    T2 : float or array_like
        transverse exponential decay time constant (in seconds).
    TR : float
        repetition time (in seconds).
    alpha : float or array_like
        flip angle (in rad).
    field_map : float or array_like
        B0 field map (in Hz).
    phase_cyc : float or array_like, optional
        Linear phase-cycle increment (in rad).
    M0 : float or array_like, optional
        proton density.
    delta_cs : float, optional
        chemical shift of species w.r.t. the water peak (in Hz).
    phi_rf : float, optional
        RF phase offset, related to the combin. of Tx/Rx phases (in
        rad).
    phi_edd : float, optional
        phase errors due to eddy current effects (in rad).
    phi_drift : float, optional
        phase errors due to B0 drift (in rad).

    Returns
    -------
    Mxy : numpy.array
        Transverse complex magnetization.

    Notes
    -----
    `T1`, `T2`, `alpha`, `field_map`, and `M0` can all be either a
    scalar or an MxN array.  `phase_cyc` can be a scalar or length L
    vector.

    Implementation of equations [1--2] in [1]_.  These equations are
    based on the Ernst-Anderson derivation [4]_ where off-resonance
    is assumed to be subtracted as opposed to added (as in the
    Freeman-Hill derivation [5]_).  Hoff actually gets Mx and My
    flipped in the paper, so we fix that here.  We also assume that
    the field map will be provided given the Freeman-Hill convention.

    Also see equations [2.7] and [2.10a--b] from [4]_ and equations
    [3] and [6--12] from [5]_.

    References
    ----------
    .. [1] Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact
           removal for bSSFP imaging with an elliptical signal
           model." Magnetic resonance in medicine 71.3 (2014):
           927-933.

    .. [4] Ernst, Richard R., and Weston A. Anderson. "Application of
           Fourier transform spectroscopy to magnetic resonance."
           Review of Scientific Instruments 37.1 (1966): 93-102.

    .. [5] Freeman R, Hill H. Phase and intensity anomalies in
           fourier transform NMR. J Magn Reson 1971;4:366–383.
    '''

    # We are assuming Freeman-Hill convention for off-resonance map,
    # so we need to negate to make use with this Ernst-Anderson-
    # based implementation from Hoff
    field_map = -1*field_map

    # Make sure we're working with arrays
    T1 = np.atleast_2d(T1)
    T2 = np.atleast_2d(T2)
    alpha = np.atleast_2d(alpha)
    field_map = np.atleast_2d(field_map)
    phase_cyc = np.atleast_2d(phase_cyc)

    # If we have more than one phase-cycle, then add that dimension
    if phase_cyc.size > 1:
        reps = (phase_cyc.size, 1, 1)
        phase_cyc = np.tile(
            phase_cyc, T1.shape[:] + (1,)).transpose((2, 0, 1))
        T1 = np.tile(T1, reps)
        T2 = np.tile(T2, reps)
        alpha = np.tile(alpha, reps)
        field_map = np.tile(field_map, reps)

    # All this nonsense so we don't divide by 0
    E1 = np.zeros(T1.shape)
    E1[T1 > 0] = np.exp(-TR/T1[T1 > 0])
    E2 = np.zeros(T2.shape)
    E2[T2 > 0] = np.exp(-TR/T2[T2 > 0])

    # Precompute theta and some cos, sin
    theta = get_theta(TR, field_map, phase_cyc, delta_cs)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    ct = np.cos(theta)
    st = np.sin(theta)

    # Get to business
    den = (1 - E1*ca)*(1 - E2*ct) - (E2*(E1 - ca))*(E2 - ct)
    Mx = -M0*((1 - E1)*E2*sa*st)/den
    My = M0*((1 - E1)*sa)*(1 - E2*ct)/den
    Mxy = Mx + 1j*My
    Mxy *= get_bssfp_phase(
        T2, TR, field_map, delta_cs, phi_rf, phi_edd, phi_drift)

    return Mxy.squeeze()

def elliptical_params(T1, T2, TR, alpha, M0=1):
    '''Return ellipse parameters M, a, b.

    Parameters
    ----------
    T1 : array_like
        longitudinal exponential decay time constant (in sec).
    T2 : array_like
        transverse exponential decay time constant (in sec).
    TR : float
        repetition time (in sec).
    alpha : float
        flip angle (in rad).
    M0 : array_like, optional
        Proton density.

    Returns
    -------
    M : array_like
        Cross point.
    a : array_like
        Theta-independent ellipse parameter.
    b : array_like
        Theta-independent ellipse parameter.

    Notes
    -----
    Outputs are the parameters of ellipse an ellipse, (M, a, b).
    These parameters do not depend on theta.

    Implementation of equations [3-5] in [1]_.
    '''

    # Make sure we're working with arrays
    T1 = np.array(T1)
    T2 = np.array(T2)

    # All this nonsense so we don't divide by 0
    E1 = np.zeros(T1.shape)
    E1[T1 > 0] = np.exp(-TR/T1[T1 > 0])
    E2 = np.zeros(T2.shape)
    E2[T2 > 0] = np.exp(-TR/T2[T2 > 0])

    ca = np.cos(alpha)
    sa = np.sin(alpha)
    den = 1 - E1*ca - (E2**2)*(E1 - ca)
    M = M0*(1 - E1)*sa/den
    a = E2
    b = E2*(1 - E1)*(1 + ca)/den
    return(M, a, b)

def ssfp_from_ellipse(M, a, b, TR, field_map, phase_cyc=0):
    '''Simulate banding given elliptical signal params and field map.

    Parameters
    ----------
    M : array_like
        Cross point.
    a : array_like
        Theta-independent ellipse parameter.
    b : array_like
        Theta-independent ellipse parameter.
    TR : float
        Repetition time (in sec).
    field_map : array_like
        Off-resonance map (in Hz).
    phase_cyc : float
        Phase-cycling increment (in rad).

    Returns
    -------
    I : array_like
        SSFP simulation result.
    '''

    theta = get_theta(TR, field_map, phase_cyc)
    I = M*(1 - a*np.exp(1j*theta))/(1 - b*np.cos(theta))
    I *= get_bssfp_phase(0, TR, field_map) # what is T2?
    return I

def  get_geo_center(M, a, b):
    '''Get geometric center of ellipse.

    Parameters
    ----------
    M : array_like
        Cross point.
    a : array_like
        Theta-independent ellipse parameter.
    b : array_like
        Theta-independent ellipse parameter.

    Returns
    -------
    xc : array_like
        x coordinates of geometric center of ellipse.
    yc : array_like
        y coordinates of geometric center of ellipse.
    '''

    xc = M*(1 - a*b)/(1 - b**2)
    yc = 0
    return(xc, yc)

def get_cart_elliptical_params(M, a, b):
    '''Get parameters needed for cartesian representation of ellipse.

    Parameters
    ----------
    M : array_like
        Cross point.
    a : array_like
        Theta-independent ellipse parameter.
    b : array_like
        Theta-independent ellipse parameter.

    Returns
    -------
    xc : array_like
        x coordinates of geometric center of ellipse.
    yc : array_like
        y coordinates of geometric center of ellipse.
    A : array_like
        Semi-major axis.
    B : array_like
        Semi-minor axis.
    '''

    A = M*np.abs(a - b)/(1 - b**2)
    B = M*a/np.sqrt(1 - b**2)
    xc, yc = get_geo_center(M, a, b)

    return(xc, yc, A, B)

def make_cart_ellipse(xc, yc, A, B, num_t=100):
    '''Make a cartesian ellipse, return x,y coordinates for plotting.

    Parameters
    ----------
    xc : array_like
        x coordinates of geometric center of ellipse.
    yc : array_like
        y coordinates of geometric center of ellipse.
    A : array_like
        Semi-major axis.
    B : array_like
        Semi-minor axis.

    Returns
    -------
    x : array_like
        Cartesian x coordinates.
    y : array_like
        Cartesian y coordinates.
    '''

    # Use parametric equation
    t = np.linspace(0, 2*np.pi, num_t)
    x = A*np.cos(t) + xc
    y = B*np.sin(t) + yc
    return(x, y)

def get_center_of_mass(M, a, b):
    '''Give center of mass a function of ellipse parameters.

    Parameters
    ----------
    M : array_like
        Cross point.
    a : array_like
        Theta-independent ellipse parameter.
    b : array_like
        Theta-independent ellipse parameter.

    Returns
    -------
    cm : array_like
        Center of mass.
    '''

    cm = M*(1 + ((b - a)/b)*(1/np.sqrt(1 - b**2) - 1))
    return cm

def get_center_of_mass_nmr(T1, T2, TR, alpha, M0=1):
    '''Give center of mass as a function of NMR parameters.

    Parameters
    ----------
    T1 : array_like
        longitudinal exponential decay time constant (in sec).
    T2 : array_like
        transverse exponential decay time constant (in sec).
    TR : float
        Repetition time (in sec).
    alpha : float
        Flip angle (in rad).
    M0 : array_like, optional
        Proton density.

    Returns
    -------
    cm : array_like
        Center of mass.
    '''

    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)
    ca = np.cos(alpha)
    cm = M0*(1 - (E1 - ca)*np.sqrt((E2**2 - 1)/(E2**2*(
        E1 - ca)**2 - (E1*ca - 1)**2)))*np.tan(alpha/2)
    return cm

def spectrum(T1, T2, TR, alpha):
    '''Generate an entire period of the bSSFP signal profile.

    Parameters
    ----------
    T1 : array_like
        longitudinal exponential decay time constant (in sec).
    T2 : array_like
        transverse exponential decay time constant (in sec).
    TR : float
        Repetition time (in sec).
    alpha : float
        Flip angle (in rad).

    Returns
    -------
    sig : array_like
        Full, complex SSFP spectrum.
    '''

    # Get all possible off-resonance frequencies
    df = np.linspace(-1/TR, 1/TR, 100)
    sig = ssfp_old(T1, T2, TR, alpha, df)
    return sig

def get_bssfp_phase(T2, TR, field_map, delta_cs=0, phi_rf=0,
                    phi_edd=0, phi_drift=0):
    '''Additional bSSFP phase factors.

    Parameters
    ----------
    T1 : array_like
    TR : float
        repetition time (in sec).
    field_map : array_like
        off-resonance map (Hz).
    delta_cs : float, optional
        chemical shift of species w.r.t. the water peak (Hz).
    phi_rf : float, optional
        RF phase offset, related to the combin. of Tx/Rx phases (rad).
    phi_edd : float, optional
        phase errors due to eddy current effects (rad).
    phi_drift : float, optional
        phase errors due to B0 drift (rad).

    Returns
    -------
    phase : array_like
        Additional phase term to simulate readout at time TE = TR/2.
        Assumes balanced (TE = TR/2).

    Notes
    -----
    This is exp(-i phi) from end of p. 930 in [1]_.

    We use a positive exponent, exp(i phi), as in Hoff and Taylor
    MATLAB implementations.  This phase factor is also positive in
    equaiton [5] of [3]_.

    In Hoff's paper the equation is not explicitly given for phi, so
    we implement equation [5] that gives more detailed terms, found
    in [2]_.

    References
    ----------
    .. [2] Shcherbakova, Yulia, et al. "PLANET: An ellipse fitting
           approach for simultaneous T1 and T2 mapping using
           phase‐cycled balanced steady‐state free precession."
           Magnetic resonance in medicine 79.2 (2018): 711-722.

    .. [3] Scheffler, Klaus, and Jürgen Hennig. "Is TrueFISP a
           gradient‐echo or a spin‐echo sequence?." Magnetic
           Resonance in Medicine: An Official Journal of the
           International Society for Magnetic Resonance in Medicine
           49.2 (2003): 395-397.
    '''

    TE = TR/2 # assume bSSFP
    phi = 2*np.pi*(
        delta_cs + field_map)*TE + phi_rf + phi_edd + phi_drift
    return np.exp(1j*phi)*np.exp(-TE/T2)

def get_theta(TR, field_map, phase_cyc=0, delta_cs=0):
    '''Get theta, spin phase per repetition time, given off-resonance.

    Parameters
    ----------
    TR : float
        repetition time (in sec).
    field_map : array_like
        Off-resonance map (in Hz).
    phase_cyc : array_like, optional
        Phase-cycling (in rad).
    delta_cs : float, optional, optional
        chemical shift of species w.r.t. the water peak (Hz).

    Returns
    -------
    theta : array_like
        Spin phase per repetition time, given off-resonance.

    Notes
    -----
    Equation for theta=2*pi*df*TR is in Appendix A of [3]_.  The
    additional chemical shift term can be found, e.g., in [2]_.

    References
    ----------
    .. [3] Hargreaves, Brian A., et al. "Characterization and
           reduction of the transient response in steady‐state MR
           imaging." Magnetic Resonance in Medicine: An Official
           Journal of the International Society for Magnetic
           Resonance in Medicine 46.1 (2001): 149-158.
    '''

    return 2*np.pi*(delta_cs + field_map)*TR + phase_cyc

def get_cross_point(I1, I2, I3, I4):
    '''Find intersection of two lines connecting diagonal pairs.

    Parameters
    ----------
    I1 : array_like
        First of the first phase-cycle pair (0 degrees).
    I2 : array_like
        First of the second phase-cycle pair (90 degrees).
    I3 : array_like
        Second of the first phase-cycle pair (180 degrees).
    I4 : array_like
        Second of the second phase-cycle pair (270 degrees).

    Returns
    -------
    x0 : array_like
        x coordinate of cross point.
    y0 : array_like
        y coordinate of cross point.

    Notes
    -----
    (xi,yi) are the real and imaginary parts of complex valued pixels
    in four bSSFP images denoted Ii and acquired with phase cycling
    dtheta = (i-1)*pi/2 with 0 < i < 4.

    This are Equations [11-12] from [1]_.  There is  a typo in the
    paper for equation [12] fixed in this implementation.  The first
    term of the numerator should have (y2 - y4) instead of (x2 - y4)
    as written.
    '''

    x1, y1 = I1.real, I1.imag
    x2, y2 = I2.real, I2.imag
    x3, y3 = I3.real, I3.imag
    x4, y4 = I4.real, I4.imag

    den = (x1 - x3)*(y2 - y4) + (x2 - x4)*(y3 - y1)
    x0 = ((x1*y3 - x3*y1)*(x2 - x4) - (x2*y4 - x4*y2)*(x1 - x3))/den
    y0 = ((x1*y3 - x3*y1)*(y2 - y4) - (x2*y4 - x4*y2)*(y1 - y3))/den
    return(x0, y0)

def get_complex_cross_point(Is):
    '''Find intersection of two lines connecting diagonal pairs.

    Parameters
    ----------
    Is : array_like
        4 phase-cycled images: [I0, I1, I2, I3].

    Returns
    -------
    M : array_like
        Complex cross point.

    Notes
    -----
    We assume that Is has the phase-cycle dimenension along the first
    axis.

    (xi, yi) are the real and imaginary parts of complex valued
    pixels in four bSSFP images denoted Ii and acquired with phase
    cycling dtheta = (i-1)*pi/2 with 0 < i < 4.

    This is Equation [13] from [1]_.
    '''

    x1, y1 = Is[0, ...].real, Is[0, ...].imag
    x2, y2 = Is[1, ...].real, Is[1, ...].imag
    x3, y3 = Is[2, ...].real, Is[2, ...].imag
    x4, y4 = Is[3, ...].real, Is[3, ...].imag

    den = (x1 - x3)*(y2 - y4) + (x2 - x4)*(y3 - y1)
    if (den == 0).any():
        # Make sure we're not dividing by zero
        den += np.finfo(float).eps

    M = ((x1*y3 - x3*y1)*(Is[1, ...] - Is[3, ...]) - (
        x2*y4 - x4*y2)*(Is[0, ...] - Is[2, ...]))/den
    return M

if __name__ == '__main__':
    pass
