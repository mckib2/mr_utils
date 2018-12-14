import numpy as np
from mr_utils.utils import find_nearest
from mr_utils.sim.ssfp import ssfp

def get_df_responses(T1,T2,PD,TR,alpha,phase_cyc,ddf):
    '''Simulate bSSFP response across all possible off-resonances.

    T1 -- scalar T1 longitudinal recovery value in seconds.
    T2 -- scalar T2 transverse decay value in seconds.
    PD -- scalar proton density value scaled the same as acquisiton.
    TR -- Repetition time in seconds.
    alpha -- Flip angle in radians.
    phase_cyc -- RF phase cycling in radians.
    ddf -- Increment size for off-resonance values: np.arange(-1/TR,1/TR,ddf)
    '''

    # Do for all possible df
    dfs = np.arange(-1/TR,1/TR,ddf)

    # Feed ssfp sim an array of parameters to be used with all the df values
    T1s = np.ones(dfs.shape)*T1
    T2s = np.ones(dfs.shape)*T2
    PDs = np.ones(dfs.shape)*PD
    resp = ssfp(T1s,T2s,TR,alpha,dfs,phase_cyc=phase_cyc,M0=PDs)

    # Returns a vector of simulated Mxy with index corresponding to dfs
    return(resp,dfs)

def quantitative_fm(Mxy,ddf,T1,T2,PD,TR,alpha,phase_cyc):

    # Simulate over the total range of off-resonance values
    resp,dfs = get_df_responses(T1,T2,PD,TR,alpha,phase_cyc,ddf)

    # Find the response that matches Mxy most closely
    idx,val = find_nearest(resp,Mxy)

    # Return the df's value, because that's really what the caller wanted
    return(dfs[idx])
