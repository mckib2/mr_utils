'''Steady-state solution for SSFP.'''

import numpy as np

def freeman_ssfp(T1, T2, TR, alpha, field_map, M0=1, before=False):
    '''Solution to steady-state given by Freeman and Hill.

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
    M0 : float or array_like, optional
        proton density.
    before : bool
        If True, will return the magetization just prior to RF pulse.
        If False, will return Mxy at TE, that is
        Mxy[TE] = Mxy+ exp(-TE/T2) exp(-j theta/2).

    Notes
    -----
    This implementation does not take into account chemical shift,
    phi_rf, eddy currents, or B0 drift.

    Implements equations [6--12] in [1]_.  This is also equation [6]
    from [2]_.

    This is very similar to the derivation given by Ernst-Anderson in
    [3]_ but for the sign convention for off-resonance.  This leads
    to sign difference in Mx compared to the Ernst-Anderson as well
    as a negative phase term exp(-j theta/2) when readout is at TE.

    References
    ----------
    .. [1] Freeman R, Hill H. Phase and intensity anomalies in
           fourier transform NMR. J Magn Reson 1971;4:366–383.

    .. [2] Hinshaw, Waldo S. "Image formation by nuclear magnetic
           resonance: the sensitive‐point method." Journal of Applied
           Physics 47.8 (1976): 3709-3721.

    .. [3] Ernst, Richard R., and Weston A. Anderson. "Application of
           Fourier transform spectroscopy to magnetic resonance."
           Review of Scientific Instruments 37.1 (1966): 93-102.
    '''

    theta = 2*np.pi*field_map*TR

    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TR/T2)

    ca = np.cos(alpha)
    sa = np.sin(alpha)
    ct = np.cos(theta)
    st = np.sin(theta)

    D = (1 - E1*ca)*(1 - E2*ct) - (E1 - ca)*(E2 - ct)*E2
    Mx = M0*(1 - E1)*(E2*sa*st)/D

    # Do we want to look right before or after RF pulse?
    if before:
        My = M0*(1 - E1)*(E2*sa*ct - E2**2*sa)/D
    else:
        My = M0*(1 - E1)*((1 - E2*ct)*sa)/D

    return (Mx + 1j*My)*np.exp(-TR/(2*T2))*np.exp(-1j*theta/2)


if __name__ == '__main__':
    pass
