'''Recreate sensitivity plots from PLANET paper.'''

from functools import partial
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET

def runner(enum, T1, T2, TR, df, pcs, M0):
    '''Run PLANET fitting for the current iteration.'''
    idx = enum[0]
    nom_alpha, dev_alpha = enum[1][:]
    I = ssfp(T1, T2, TR, nom_alpha*(1 + dev_alpha), df, pcs, M0)

    try:
        _Meff, T10, T20 = PLANET(I, nom_alpha, TR, T1, disp=False)
        T1s = T10
        T2s = T20
    except AssertionError as _e:
        # tqdm.write(str(e))
        T1s = np.nan
        T2s = np.nan
    except ValueError as _e:
        # tqdm.write(str(e))
        T1s = np.nan
        T2s = np.nan
    except TypeError as _e:
        # tqdm.write(str(e))
        T1s = np.nan
        T2s = np.nan

    return(idx, T1s, T2s)

if __name__ == '__main__':

    N_alpha = 100
    nom_alphas = np.deg2rad(np.linspace(1, 90, N_alpha))[::-1]

    N_dev = 200
    dev_alphas = np.linspace(-.10, .10, N_dev)

    M0 = 1
    T1 = .675
    T2 = .075
    df = 10
    TR = 10e-3
    lpcs = 10
    pcs = np.linspace(0, 2*np.pi, lpcs, endpoint=False) - np.pi

    # Run PLANET in parallel
    prun = partial(runner, T1=T1, T2=T2, TR=TR, df=df, pcs=pcs, M0=M0)
    alphas = np.array(np.meshgrid(nom_alphas, dev_alphas)).T.reshape(-1, 2)
    with Pool() as pool:
        res = list(tqdm(pool.imap(prun, enumerate(alphas.tolist()),
                                  chunksize=200),
                        total=alphas.shape[0], leave=False))

    # Results are not guaranteed to be in the correct order, so put in values
    # where they belong
    T1s = np.zeros((nom_alphas.size, dev_alphas.size))
    T2s = np.zeros(T1s.shape)
    for r in res:
        ii, jj = np.unravel_index(r[0], T1s.shape)
        T1s[ii, jj] = r[1]
        T2s[ii, jj] = r[2]

    # Show me the money!
    plt.subplot(1, 2, 1)
    plt.imshow(100*(T1s - T1)/T1, extent=(.9, 1.1, 1, 90), aspect='auto')
    plt.colorbar()
    plt.title('Errors in T1, %')
    plt.ylabel('Nominal FA, degrees')
    plt.xlabel('Real FA/Nominal FA')

    plt.subplot(1, 2, 2)
    plt.imshow(100*(T2s - T2)/T2, extent=(.9, 1.1, 1, 90), aspect='auto')
    plt.colorbar()
    plt.title('Errors in T2, %')
    plt.ylabel('Nominal FA, degrees')
    plt.xlabel('Real FA/Nominal FA')

    plt.show()
