'''PLANET: an ellipse fitting approach for simultaneous T1 and T2 mapping...

...Using Phase-Cycled Balanced Steady-State Free Precession.
'''

import numpy as np

from mr_utils.utils import get_semiaxes, do_planet_rotation, get_center

def PLANET(I, alpha, TR, T1_guess, fit_ellipse=None, pcs=None,
           compute_df=False, disp=False):
    '''Simultaneous T1, T2 mapping using phase‐cycled bSSFP.

    Parameters
    ==========
    I : array_like
        Complex voxels from phase-cycled bSSFP images.
    alpha : float
        Flip angle (in rad).
    TR : float
        Repetition time (in sec).
    T1_guess : float
        Estimate of expected T1 value (in sec).
    fit_ellipse : callable, optional
        Function used to fit data points to ellipse.
    pcs : array_like, optional
        Phase-cycles that generate phase-cycle images of I (required if
        computing df).
    compute_df : bool, optional
        Whether or not estimate local off-resonance, df.
    disp : bool, optional
        Show plots.

    Returns
    =======
    Meff : array_like
        Effective magnetization amplitude
    T1 : array_like
        Estimate of T1 values
    T2 : array_like
        Estimate of T2 values
    df : array_like, optional
        Estimate of off-resonance values.

    Raises
    ======
    NotImplementedError
        If compute_df=True
    AssertionError
        If fit_ellipse returns something that is not an ellipse
    AssertionError
        If the rotation fails and xc < 0 or yc =/= 0.
    AssertionError
        If a, b, or Meff are outside of interval (0, 1).
    ValueError
        If ellipse callapses to a line.
    ValueError
        If the sign of b cannot be determined.

    Notes
    =====
    Requires at least 6 phase cycles to fit the ellipse.  The ellipse fitting
    method they use (and which is implemented here) may not be the best
    method, but it is quick.  Could add more options for fitting in the future.

    fit_ellipse(x, y) should take two arguments and return a vector containing
    the coefficients of the implicit ellipse equation.  If fit_ellipse=None
    then the mr_utils.utils.fit_ellipse_halir() function will be used.

    pcs should be a list of phase-cycles in radians.  If pcs=None, it will be
    determined as I.size equally spaced phasce-cycles on the interval [0, 2pi).

    Implements algorithm described in [1]_.

    References
    ==========
    .. [1] Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
           simultaneous T1 and T2 mapping using phase‐cycled balanced
           steady‐state free precession." Magnetic resonance in medicine 79.2
           (2018): 711-722.
    '''

    # Make sure we have an ellipse fitting function
    if fit_ellipse is None:
        from mr_utils.utils import fit_ellipse_halir
        fit_ellipse = fit_ellipse_halir

    # Make sure we know what phase-cycles we have if we're computing df
    if compute_df:
        if pcs is None:
            pcs = np.linspace(0, 2*np.pi, I.size, endpoint=False)
        else:
            # Make sure we get phase-cycles as a numpy array
            pcs = np.array(pcs)
        assert pcs.size == I.size, ('Number of phase-cycles must match entries'
                                    ' of I!')

    ## Step 1. Direct linear least squares ellipse fitting to phase-cycled
    ## bSSFP data.
    C = fit_ellipse(I.real, I.imag)

    # Look at it in standard form
    C1, C2, C3, _C4, _C5, _C6 = C[:]
    assert C2**2 - 4*C1*C3 < 0, 'Not an ellipse!'

    ## Step 2. Rotation of the ellipse to initial vertical conic form.
    xr, yr, Cr, _phi = do_planet_rotation(I)
    I0 = xr + 1j*yr
    xc, yc = get_center(Cr)

    # Look at it to make sure we've rotated correctly
    if disp:
        import matplotlib.pyplot as plt
        Idraw = np.concatenate((I, [I[0]]))
        I0draw = np.concatenate((I0, [I0[0]]))
        plt.plot(Idraw.real, Idraw.imag, label='Sampled')
        plt.plot(I0draw.real, I0draw.imag, label='Rotated')
        plt.legend()
        plt.axis('square')
        plt.show()

    # Sanity check: make sure we got what we wanted:
    assert np.allclose(yc, 0), 'Ellipse rotation failed! yc = %g' % yc
    assert xc > 0, 'xc needs to be in the right half-plane! xc = %g' % xc
    # C1r, C2r, C3r, C4r, C5r, C6r = Cr[:]


    ## Step 3. Analytical solution for parameters Meff, T1, T2.
    # Get the semi axes, AA and BB
    A, B = get_semiaxes(Cr)
    # Ellipse must be vertical -- so make the axes look like it
    if A > B:
        A, B = B, A
    A2 = A**2
    B2 = B**2

    # Decide sign of first term of b
    E1 = np.exp(-TR/T1_guess)
    aE1 = np.arccos(E1)
    if alpha > aE1:
        val = -1
    elif alpha < aE1:
        val = 1
    elif alpha == aE1:
        raise ValueError('Ellipse is a line! x = Meff')
    else:
        raise ValueError('Houston, we should never have raised this error...')

    # See Appendix
    # xc = np.abs(xc) # THIS IS NOT IN THE APPENDIX but by def in eq [9]
    xc2 = xc**2
    xcA = xc*A
    b = (val*xcA + np.sqrt(xcA**2 - (xc2 + B2)*(A2 - B2)))/(xc2 + B2)
    b2 = b**2
    a = B/(xc*np.sqrt(1 - b2) + b*B)
    ab = a*b
    Meff = xc*(1 - b2)/(1 - ab)

    # Sanity checks:
    assert 0 < b < 1, '0 < b < 1 has been violated! b = %g' % b
    assert 0 < a < 1, '0 < a < 1 has been violated! a = %g' % a
    assert 0 < Meff < 1, '0 < Meff < 1 has been violated! Meff = %g' % Meff

    # Now we can find the things we were really after
    ca = np.cos(alpha)
    T1 = -1*TR/(np.log((a*(1 + ca - ab*ca) - b)/(a*(1 + ca - ab) - b*ca)))
    T2 = -1*TR/np.log(a)

    ## Step 4. Estimation of the local off-resonance df.
    if compute_df:
        # The beta way:
        # costheta = np.zeros(dphis.size)
        # for nn in range(dphis.size):
        #     x, y = I0[nn].real, I0[nn].imag
        #     tanbeta = y/(x - xc)
        #     t = np.arctan(A/B*tanbeta)
        #     costheta[nn] = (np.cos(t) - b)/(b*np.cos(t) - 1)

        # The atan2 way:
        costheta = np.zeros(pcs.size)
        for nn in range(pcs.size):
            x, y = I0[nn].real, I0[nn].imag
            t = np.arctan2(y, x - xc)

            if a > b:
                costheta[nn] = (np.cos(t) - b)/(b*np.cos(t) - 1)
            else:
                # Sherbakova doesn't talk about this case in the paper!
                costheta[nn] = (np.cos(t) + b)/(b*np.cos(t) + 1)

        # Get least squares estimate for K1, K2
        X = np.array([np.cos(pcs), np.sin(pcs)]).T
        K = np.linalg.multi_dot((np.linalg.pinv(X.T.dot(X)), X.T, costheta))
        K1, K2 = K[:]

        # And finally...
        theta0 = np.arctan2(K2, K1)
        df = -1*theta0/(2*np.pi*TR) # spurious negative sign, currently a bug
        return(Meff, T1, T2, df)

    # else...
    return(Meff, T1, T2)

if __name__ == '__main__':
    pass
