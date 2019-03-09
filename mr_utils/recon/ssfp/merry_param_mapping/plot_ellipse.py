'''Plot an ellipse based on MR parameters.'''

import numpy as np

from mr_utils.sim.ssfp import ssfp

def plotEllipse(T1, T2, TR, alpha, offres, M0, dphi):
    '''
    dphi=1 means use fixed linspace for dphi set, else, use the list of dphis
    provided.
    '''

    if dphi == 1:
        x = []
        y = []
        dphis = np.arange(0, 2*np.pi, .01)
        x = np.zeros(dphis.size)
        y = np.zeros(dphis.size)
        for ii, theta in enumerate(dphis):
            Mxy = ssfp(T1, T2, TR, alpha, offres, phase_cyc=theta, M0=M0)
            x[ii] = Mxy.real
            y[ii] = Mxy.imag
    else:
        x = np.zeros(dphi.size)
        y = np.zeros(dphi.size)
        for ii in range(dphi.size):
            Mxy = ssfp(T1, T2, TR, alpha, offres, phase_cyc=dphi[ii], M0=M0)
            x[ii] = Mxy.real
            y[ii] = Mxy.imag
    return(x, y)
