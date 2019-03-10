'''Use the geometric solution to the elliptical signal model for field map.'''

import numpy as np

from mr_utils.recon.ssfp import gs_recon

def gs_field_map(I0, I1, I2, I3, TR, gs_recon_opts=None):
    '''Use the elliptical signal model to estimate the field map.

    I0,I1 -- First phase-cycle pair, separated by 180 degrees.
    I1,I3 -- Second phase-cycle pair, separated by 180 degrees.
    TR -- Repetition time of acquisitons in ms.
    gs_recon_opts -- Options to pass to gs_recon.

    Returns wrapped field map in hertz.

    Implements field map estimation given in:
        Taylor, Meredith, et al. "MRI Field Mapping using bSSFP Elliptical
        Signal model." Proceedings of the ISMRM Annual Conference (2017).
    '''

    if gs_recon_opts is None:
        gs_recon_opts = {}

    # TE = 2*TR
    gs_sol = gs_recon(I0, I1, I2, I3, **gs_recon_opts)
    # gsfm = np.angle(gs_sol)/(2*np.pi*TE)
    gsfm = 1*np.angle(gs_sol)/(np.pi*TR)

    return gsfm
