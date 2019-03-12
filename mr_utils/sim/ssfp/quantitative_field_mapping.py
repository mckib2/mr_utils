'''Quantitative field mapping for bSSFP.

Collect quantitative MR maps (T1, T2, flip angle), then, assuming that these
won't change during the duration of the scan, we can use these to take a single
bSSFP scan each time point and solve for the off-resonance.  Thus we get a
field map at time point.
'''

import numpy as np

from mr_utils.utils import find_nearest
from mr_utils.sim.ssfp import ssfp
# from mr_utils import view

def get_df_responses(T1, T2, PD, TR, alpha, phase_cyc, dfs):
    '''Simulate bSSFP response across all possible off-resonances.

    Parameters
    ==========
    T1 : float
        scalar T1 longitudinal recovery value in seconds.
    T2 : float
        scalar T2 transverse decay value in seconds.
    PD : float
        scalar proton density value scaled the same as acquisiton.
    TR : float
        Repetition time in seconds.
    alpha : float
        Flip angle in radians.
    phase_cyc : float
        RF phase cycling in radians.
    dfs : float
        Off-resonance values to simulate over.

    Returns
    =======
    resp : array_like
        Frequency response of SSFP signal across entire spectrum.
    '''

    # Feed ssfp sim an array of parameters to be used with all the df values
    T1s = np.ones(dfs.shape)*T1
    T2s = np.ones(dfs.shape)*T2
    PDs = np.ones(dfs.shape)*PD
    resp = ssfp(T1s, T2s, TR, alpha, dfs, phase_cyc=phase_cyc, M0=PDs)

    # Returns a vector of simulated Mxy with index corresponding to dfs
    return resp

def quantitative_fm_scalar(Mxy, dfs, T1, T2, PD, TR, alpha, phase_cyc):
    '''For scalar T1, T2, PD.

    Parameters
    ==========
    Mxy : float
        Complex transverse signal we measure.
    dfs : array_like
        Off-resonance values to simulate over.
    T1 : float
        scalar T1 longitudinal recovery value in seconds.
    T2 : float
        scalar T2 transverse decay value in seconds.
    PD : float
        scalar proton density value scaled the same as acquisiton.
    TR : float
        Repetition time in seconds.
    alpha : float
        Flip angle in radians.
    phase_cyc : float
        RF phase cycling in radians.

    Returns
    =======
    float
        Off-resonace value that most closely matches Mxy prior.
    '''

    # Simulate over the total range of off-resonance values
    resp = get_df_responses(T1, T2, PD, TR, alpha, phase_cyc, dfs)

    # Find the response that matches Mxy most closely
    idx, _val = find_nearest(resp, Mxy)

    # Return the df's value, because that's really what the caller wanted
    return dfs[idx]

def quantitative_fm(Mxys, dfs, T1s, T2s, PDs, TR, alpha, phase_cyc, mask=None):
    '''Find field map given quantitative maps.

    Parameters
    ==========
    Mxys : array_like
        Complex transverse signal we measure.
    dfs : array_like
        Off-resonance values to simulate over.
    T1s : array_like
        scalar T1 longitudinal recovery value in seconds.
    T2s : array_like
        scalar T2 transverse decay value in seconds.
    PDs : array_like
        scalar proton density value scaled the same as acquisiton.
    TR : float
        Repetition time in seconds.
    alpha : float
        Flip angle in radians.
    phase_cyc : float
        RF phase cycling in radians.
    mask : array_like
        Boolean mask to tell which pixels we should compute df for.

    Returns
    =======
    fm : array_like
        Field map.
    '''

    resps = {}
    orig_size = np.asarray(T1s).shape

    if mask is None:
        mask = np.ones(Mxys.shape)

    Mxys = np.asarray(Mxys).flatten()
    T1s = np.asarray(T1s).flatten()
    T2s = np.asarray(T2s).flatten()
    PDs = np.asarray(PDs).flatten()
    mask = np.asarray(mask).flatten()

    fm = np.zeros(Mxys.size)
    for ii in range(Mxys.size):

        if mask[ii]:
            # Cache results for later in case we come across the same T1,T2,PD
            if (PDs[ii], T1s[ii], T2s[ii]) not in resps:
                resps[(PDs[ii], T1s[ii], T2s[ii])] = get_df_responses(
                    T1s[ii], T2s[ii], PDs[ii], TR, alpha, phase_cyc, dfs)

            # Find the appropriate off-resonance value for this T1,T2,PD,Mxy
            idx, _val = find_nearest(
                resps[(PDs[ii], T1s[ii], T2s[ii])], Mxys[ii])
            fm[ii] = dfs[idx]
        else:
            fm[ii] = 0

    return fm.reshape(orig_size)
