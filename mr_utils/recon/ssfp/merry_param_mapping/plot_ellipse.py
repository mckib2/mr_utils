'''Plot an ellipse based on MR parameters.'''

import numpy as np

from mr_utils.sim.ssfp import ssfp

def plotEllipse(T1, T2, TR, alpha, offres, M0, dphi):
    '''Compute (x, y) coordinates for ellipse described by MR parameters.

    Parameters
    ==========
    T1 : float
        Longitudinal relaxation constant (in sec).
    T2 : float
        Transverse relaxation constant (in sec).
    TR : float
        Repetition time (in sec).
    alpha : float
        Flip angle (in rad).
    offres : float
        Off-resonance (in Hz).
    M0 : float
        Proton density.
    dphi : float or bool
        Phase-cycle value (in rad). dphi=True means use fixed linspace for dphi
        set, else, use the list of dphis provided.

    Returns
    =======
    x : array_like
        x coordinate values of ellipse.
    y : array_like
        y coordinate values of ellipse.
    '''

    if isinstance(dphi, bool):
        dphis = np.arange(0, 2*np.pi, .01)
        Mxy = ssfp(T1, T2, TR, alpha, offres, phase_cyc=dphis, M0=M0)
    else:
        Mxy = ssfp(T1, T2, TR, alpha, offres, phase_cyc=dphis, M0=M0)

    x = Mxy.real
    y = Mxy.imag
    return(x, y)
