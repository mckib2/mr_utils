'''Use the geometric solution to the elliptical signal model for field map.'''

import numpy as np

from mr_utils.recon.ssfp import gs_recon

def gs_field_map(I0, I1, I2, I3, TR, gs_recon_opts=None):
    '''Use the elliptical signal model to estimate the field map.

    Parameters
    ----------
    I0 : array_like
        First of the first phase-cycle pair (0 degrees).
    I2 : array_like
        Second of the first phase-cycle pair (180 degrees).
    I1 : array_like
        First of the second phase-cycle pair (90 degrees).
    I3 : array_like
        Second of the second phase-cycle pair (270 degrees).
    TR : float
        Repetition time of acquisitons in ms.
    gs_recon_opts : dict, optional
        Options to pass to gs_recon.

    Returns
    -------
    gsfm : array_like
        Wrapped field map in hertz.

    Notes
    -----
    I0, I2 and I1, I3 must be phase-cycle pairs, meaning I0, I2 are
    separated by 180 degrees and I1, I3 are separated by 180 degrees.
    It does not matter what the actual phase-cycles are.

    Implements field map estimation given in [1]_.

    References
    ----------
    .. [1] Taylor, Meredith, et al. "MRI Field Mapping using bSSFP
           Elliptical Signal model." Proceedings of the ISMRM Annual
           Conference (2017).
    '''

    if gs_recon_opts is None:
        gs_recon_opts = {}

    # TE = 2*TR
    gs_sol = gs_recon(I0, I1, I2, I3, **gs_recon_opts)
    # gsfm = np.angle(gs_sol)/(2*np.pi*TE)
    gsfm = np.angle(gs_sol)/(np.pi*TR)

    return gsfm
