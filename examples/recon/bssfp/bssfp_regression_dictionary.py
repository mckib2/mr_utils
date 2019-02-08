'''Given two phase cycles, look up T1, T2, theta, M0.'''

import numpy as np
from tqdm import tqdm

from mr_utils.sim.ssfp import ssfp

if __name__ == '__main__':

    # Acquisiton parameters
    TR = 6e-3
    alpha = np.deg2rad(10)

    # Make a dictionary
    dfs = np.linspace(-1/TR, 1/TR, 101)
    T1s = np.linspace(.8, .04, 51)
    T2s = np.linspace(1., .06, 51)
    M0s = np.linspace(0.0, 1.0, 51)

    D = dict()
    for T1 in tqdm(T1s):
        for T2 in T2s:
            for df in dfs:
                for M0 in M0s:
                    D[(T1, T2, df, M0)] = (ssfp(T1, T2, TR, alpha, df, 0, M0),
                                           ssfp(T1, T2, TR, alpha, df, np.pi,
                                                M0))
