'''PLANET: an ellipse fitting approach for simultaneous T1 and T2 mapping...

...Using Phase-Cycled Balanced Steady-State Free Precession.
'''

import numpy as np

from mr_utils.utils import fit_ellipse


def PLANET(I, alpha, TR, T1s=None):
    '''Simultaneous T1, T2 mapping using phase‐cycled bSSFP.

    I -- Complex voxels from phase-cycled bSSFP images.
    alpha -- Flip angle (in rad).
    TR -- Repetition time (in sec).
    T1s -- Range of T1s.

    Requires at least 6 phase cycles to fit the ellipse.  The ellipse fitting
    method they use (and which is implemented here) may not be the best
    method, but it is quick.  Could add more options for fitting in the future.

    Implements algorithm described in:
        Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
        simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
        free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.
    '''

    ## Step 1. Direct linear least squares ellipse fitting to phase-cycled
    ## bSSFP data.
    c = fit_ellipse(I)

    # Look at it in standard form
    A, B, C, D, E, F = c[:]
    assert B**2 - 4*A*C < 0, 'Not an ellipse!'

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
    # phi = .5*np.arctan2(c[1], c[0] - c[2]) # Shcherbakova, need to add pi/2

    # Shcherbakova's solution for phi didn't satisfy me, so I looked at
    # https://en.wikipedia.org/wiki/Ellipse to find the following expression.
    # Making phi seems necessary to get the ellipse vertically oriented.
    phi = -1*np.arctan2(C - A - np.sqrt((A - C)**2 + B**2), B)
    Ir = I*np.exp(1j*phi)
    plt.plot(Ir.real, Ir.imag, '*')

    # Find new coefficients: http://www.mathamazement.com/
    # Lessons/Pre-Calculus/09_Conic-Sections-and-Analytic-Geometry/
    # rotation-of-axes.html
    Ar = (A + C)/2 + (A - C)/2*np.cos(2*phi) - B/2*np.sin(2*phi)
    Br = (A - C)*np.sin(2*phi) + B*np.cos(2*phi)
    Cr = (A + C)/2 + (C - A)/2*np.cos(2*phi) + B/2*np.sin(2*phi)
    Dr = D*np.cos(phi) - E*np.sin(phi)
    Er = D*np.sin(phi) + E*np.cos(phi)
    Fr = F
    eqn = Ar*X**2 + Br*X*Y + Cr*Y**2 + Dr*X + Er*Y + Fr
    plt.contour(X, Y, eqn, [Z])
    plt.show()

    # Step 3. Analytical solution for parameters Meff, T1, T2.

    # E1 = np.exp(-TR/T1s)
    # aE1 = np.arccos(E1)
    # if alpha > aE1:
    #     val = -1
    # else:
    #     val = 1
    #
    # b = (val*xc*A + np.sqrt(
    #     (xc*A)**2 - (xc**2 + B**2)*(A**2 - B**2)))/(xc**2 + B**2)
    # a = B/(xc*np.sqrt(1 - b**2) + b*B)
    # Meff = xc*(1 - b**2)/(1 - a*b)

if __name__ == '__main__':

    from mr_utils.sim.ssfp import ssfp

    num_pc = 8
    I = np.zeros(num_pc, dtype='complex')
    pcs = [2*np.pi*n/num_pc for n in range(num_pc)]
    TR = 10e-3
    alpha = np.deg2rad(30)
    df = 1/(2.5*TR)
    for ii, pc in enumerate(pcs):
        I[ii] = ssfp(.3, .085, TR, alpha, df, pc)

    PLANET(I, alpha, TR)
