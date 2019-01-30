'''Dictionary lookup of NMR parameters given bSSFP signal.
'''

import numpy as np
# import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp_old

def get_keys(T1s, T2s, alphas):
    '''Generate matrix of params [T1,T2,alpha] to generate a dictionary.

    T1,T2 are chosen to be feasible, i.e., T1 >= T2.
    '''

    T1_mesh, T2_mesh, alpha_mesh = np.meshgrid(T1s, T2s, alphas)
    mask = (T1_mesh >= T2_mesh) # choose the consistent parameters
    T1_mesh = T1_mesh[mask].flatten()
    T2_mesh = T2_mesh[mask].flatten()
    alpha_mesh = alpha_mesh[mask].flatten()

    # Create key lookups
    keys = np.vstack((T1_mesh, T2_mesh, alpha_mesh))
    return keys

def ssfp_dictionary(T1s, T2s, TR, alphas, df):
    '''Generate a dicionary of bSSFP profiles given parameters.

    T1s -- (1D) all T1 decay constant values to simulate.
    T2s -- (1D) all T2 decay constant values to simulate.
    TR -- repetition time for bSSFP simulation.
    alphas -- (1D) all flip angle values to simulate.
    df -- (1D) off-resonance frequencies over which to simulate.

    T1s,T2s,alphas should all be 1D arrays.  All feasible combinations will be
    simulated (i.e., where T1 >= T2).  The dictionary and keys are returned.
    Each dictionary column is the simulation over frequencies df.  The keys are
    a list of tuples: (T1,T2,alpha).
    '''

    # Get keys from supplied params
    keys = get_keys(T1s, T2s, alphas)

    # Use more efficient matrix formulation
    D = ssfp_old(keys[0, :], keys[1, :], TR, keys[2, :], df)
    return(D, keys)

def ssfp_dictionary_for_loop(T1s, T2s, TR, alphas, df):
    '''Verification for ssfp_dictionary generation.'''

    # Get keys from supplied params
    keys = get_keys(T1s, T2s, alphas)

    # Generate dictionary iterating over keys
    N = np.sum(keys.shape[1])
    D = np.zeros((N, df.size), dtype='complex')
    for ii in range(N):
        D[ii, :] = ssfp_old(keys[0, ii], keys[1, ii], TR, keys[2, ii], df)
    return(D, keys)

def find_atom(sig, D, keys):
    '''Find params of dictionary atom closest to observed signal profile.'''

    # Make sig and columns of D comparable


    # Use MSE metric between each column of D and sig
    res = np.sqrt(np.sum(np.abs(D - sig)**2, axis=1))

    # Take the lowest MSE to be the correct atom and get the key
    param_est = keys[:, np.argmin(res)]
    return param_est

if __name__ == '__main__':
    pass
