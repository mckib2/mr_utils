'''Do simple planet implementation to make sure we know what to do.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from mr_utils.sim.ssfp import ssfp
from mr_utils.utils import (fit_ellipse_halir, rotate_coefficients,
                            get_center, get_semiaxes)

if __name__ == '__main__':

    # Generate a voxel with several phase-cycles
    num_pcs = 100
    dphis = np.linspace(0, 2*np.pi, num_pcs, endpoint=False)
    T1, T2 = .675, .075
    TR = 10e-3
    alpha = np.deg2rad(20)
    df = 9
    M0 = 1
    phi_rf = np.deg2rad(5)
    I = ssfp(T1, T2, TR, alpha, df, dphis, M0, phi_rf=phi_rf)

    # plt.plot(I.real, I.imag)
    # plt.axis('square')
    # plt.show()

    # Step 1: Fit ellipse
    C = fit_ellipse_halir(I.real, I.imag)

    # Rotate to vertical conic form
    phi = 1/2*np.arctan(C[1]/(C[0] - C[2])) #+ np.pi/2 # unwrap: +pi/2
    C0 = rotate_coefficients(C, -phi)
    I0 = I*np.exp(-1j*phi)

    plt.plot(I.real, I.imag)
    plt.plot(I0.real, I0.imag)
    plt.axis('square')
    plt.show()

    xc, yc = get_center(C0)
    assert xc > 0
    assert np.allclose(yc, 0)


    # Step 3: Solve for M, T1, T2
    A, B = get_semiaxes(C0)

    # Compute b and redundancy check for a
    if alpha <= np.arccos(np.exp(-TR/T1)):
        b = (xc*A + np.sqrt(
            (xc*A)**2 - (xc**2 + B**2)*(A**2 - B**2)))/(xc**2 + B**2)
        a_check = (xc*b - A)/(xc - A*b)
    else:
        b = (-xc*A + np.sqrt(
            (xc*A)**2 - (xc**2 + B**2)*(A**2 - B**2)))/(xc**2 + B**2)
        a_check = (A + xc*b)/(xc + A*b)
    assert 0 < b < 1
    assert 0 < a_check < 1

    # a has same formula either way
    a = B/(xc*np.sqrt(1 - b**2) + b*B)
    assert 0 < a < 1

    # Redundancy check
    assert np.allclose(a, a_check)

    Mest = xc*(1 - b**2)/(1 - a*b)
    T1est = -TR/(np.log((a*(1 + np.cos(alpha) - a*b*np.cos(alpha)) - b)/(
        a*(1 + np.cos(alpha) - a*b) - b*np.cos(alpha))))
    T2est = -TR/np.log(a)

    print(T1, T1est)
    print(T2, T2est)
    print(M0, Mest)

    # Step 4. Off-resonance estimation.
    costheta = np.zeros(dphis.size)
    for nn in range(dphis.size):
        x, y = I0[nn].real, I0[nn].imag
        tanbeta = y/(x - xc)
        t = np.arctan(A/B*tanbeta)
        costheta[nn] = (np.cos(t) - b)/(b*np.cos(t) - 1)

    obj = lambda x: np.linalg.norm(
        costheta - x[0]*np.cos(dphis) - x[1]*np.sin(dphis))**2
    res = minimize(obj, np.ones(2))
    K1, K2 = res['x'][:]
    print(K1, K2)
    theta0 = np.arctan(K2/K1)
    dfest = theta0/(2*np.pi*TR)

    print('1/TR: %g' % (1/TR))
    print(df, dfest)
