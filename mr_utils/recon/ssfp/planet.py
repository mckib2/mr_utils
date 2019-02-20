'''PLANET: an ellipse fitting approach for simultaneous T1 and T2 mapping...

...Using Phase-Cycled Balanced Steady-State Free Precession.
'''

import numpy as np

from mr_utils.utils import fit_ellipse, rotate_coefficients, get_center
from mr_utils.utils import get_semiaxes

def PLANET(I, alpha, TR, T1s=None, pcs=None, compute_df=False, disp=False):
    '''Simultaneous T1, T2 mapping using phase‐cycled bSSFP.

    I -- Complex voxels from phase-cycled bSSFP images.
    alpha -- Flip angle (in rad).
    TR -- Repetition time (in sec).
    pcs -- List of phase-cycles in I (required if computing df).
    T1s -- Range of T1s.
    compute_df -- Whether or not estimate local off-resonance, df.
    disp -- Show plots.

    Requires at least 6 phase cycles to fit the ellipse.  The ellipse fitting
    method they use (and which is implemented here) may not be the best
    method, but it is quick.  Could add more options for fitting in the future.

    pcs should be a list of phase-cycles in radians.  If pcs=None, it will be
    determined as I.size equally spaced phasce-cycles on the interval [0, 2pi).

    Implements algorithm described in:
        Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
        simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
        free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.
    '''

    # Make sure we know what phase-cycles we have if we're computing df
    if compute_df:
        from scipy.optimize import curve_fit
        if pcs is None:
            pcs = [2*np.pi*nn/I.size for nn in range(I.size)]
        assert len(pcs) == I.size, 'Phase-cycle list must match entries of I!'

        # For now, let's just die
        raise NotImplementedError('compute_df not working yet...')

    # Make sure we have a reasonable range of T1s to work with if the user
    # doesn't provide any
    if T1s is None:
        T1s = np.linspace(.2, 2, 100)

    ## Step 1. Direct linear least squares ellipse fitting to phase-cycled
    ## bSSFP data.
    c = fit_ellipse(I)

    # Look at it in standard form
    A, B, C, D, E, F = c[:]
    assert B**2 - 4*A*C < 0, 'Not an ellipse!'

    # Show some ellipses (for debugging mostly)
    if disp:
        import matplotlib.pyplot as plt
        x = np.linspace(-0.4, 0.4, 1000)
        y = np.linspace(-0.4, 0.4, 1000)
        X, Y = np.meshgrid(x, y)
        eqn = A*X**2 + B*X*Y + C*Y**2 + D*X + E*Y + F
        Z = 0
        plt.contour(X, Y, eqn, [Z])
        plt.xlim([-0.3, 0.3])
        plt.ylim([-0.3, 0.3])
        plt.grid()
        plt.plot(I.real, I.imag, '.')

    ## Step 2. Rotation of the ellipse to initial vertical conic form.
    phi = -.5*np.arctan2(c[1], c[0] - c[2]) # Shcherbakova with added -1 fac
    cr = rotate_coefficients(c, phi)
    xc, yc = get_center(cr)

    # Manually unwrap
    if not np.allclose(yc, 0):
        phi0 = phi + np.pi/2
        cr = rotate_coefficients(c, phi0)
        xc, yc = get_center(cr)
        if not np.allclose(yc, 0):
            phi0 = phi - np.pi/2
            cr = rotate_coefficients(c, phi0)
            xc, yc = get_center(cr)
        phi = phi0

    # Make sure we got what we wanted:
    assert np.allclose(yc, 0), 'Ellipse rotation failed! yc = %g' % yc
    Ar, Br, Cr, Dr, Er, Fr = cr[:]

    # If we want to look at it (for debugging mostly)
    if disp:
        Ir = I*np.exp(1j*phi)
        plt.plot(Ir.real, Ir.imag, '*')
        eqn = Ar*X**2 + Br*X*Y + Cr*Y**2 + Dr*X + Er*Y + Fr
        plt.contour(X, Y, eqn, [Z])
        plt.show()

    ## Step 3. Analytical solution for parameters Meff, T1, T2.
    # Get the semi axes, AA and BB
    AA, BB = get_semiaxes(cr)
    assert AA < BB, 'Ellipse must be vertical!'
    AA2 = AA**2
    BB2 = BB**2

    # Decide sign of b
    E1 = np.exp(-TR/T1s)
    aE1 = np.arccos(E1)
    if np.all(alpha > aE1):
        val = -1
    elif np.all(alpha < aE1):
        val = 1
    elif np.all(alpha == aE1):
        raise ValueError('Ellipse is a line! x = Meff')
    else:
        raise ValueError('Houston, we should never have raised this error...')

    # See Appendix
    xc = np.abs(xc) # THIS IS NOT IN THE APPENDIX but by def in eq [9]
    xc2 = xc**2
    xcAA = xc*AA
    b = (val*xcAA + np.sqrt(xcAA**2 - (xc2 + BB2)*(AA2 - BB2)))/(xc2 + BB2)
    b2 = b**2
    a = BB/(xc*np.sqrt(1 - b2) + b*BB)
    ab = a*b
    Meff = xc*(1 - b2)/(1 - ab)

    # Now we can find the things we were really after
    assert 0 < b < 1, '0 < b < 1 has been violated! b = %g' % b
    assert 0 < a < 1, '0 < a < 1 has been violated! a = %g' % a
    assert 0 < Meff < 1, '0 < Meff < 1 has been violated! Meff = %g' % Meff
    ca = np.cos(alpha)
    T1 = -1*TR/(np.log((a*(1 + ca - ab*ca) - b)/(a*(1 + ca - ab) - b*ca)))
    T2 = -1*TR/np.log(a)

    ## Step 4. Estimation of the local off-resonance df.
    if compute_df:
        tanbeta = I.imag/(I.real - xc)
        tn = np.arctan2(AA*tanbeta, BB)
        ctn = np.cos(tn)
        ct = (ctn - b)/(b*ctn - 1)

        k, _cov = curve_fit(
            lambda x, k0, k1: k0*np.cos(x) + k1*np.sin(x), pcs, ct)
        theta0 = np.arctan2(k[1], k[0])
        df = theta0/(2*np.pi*TR)
        return(Meff, T1, T2, df)
    # else...
    return(Meff, T1, T2)

if __name__ == '__main__':
    pass
