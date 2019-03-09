'''Plot an ellipse based on MR parameters.'''

import numpy as np

from mr_utils.recon.ssfp.merry_param_mapping.ssfp_fit import SSFPfit

def plotEllipse(T1, T2, TR, TE, alpha, offres, M0, dphi):
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
            Mx, My, _a, _b, _M = SSFPfit(
                T1, T2, TR, TE, alpha, theta, offres, M0)
            x[ii] = Mx
            y[ii] = My

    else:
        x = np.zeros(dphi.size)
        y = np.zeros(dphi.size)
        for ii in range(dphi.size):
            Mx, My, _a, _b, _M = SSFPfit(
                T1, T2, TR, TE, alpha, dphi[ii], offres, M0)
            x[ii] = Mx
            y[ii] = My

    return(x, y)
