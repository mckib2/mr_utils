'''Recreate sensitivity plots from PLANET paper.'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from mr_utils.sim.ssfp import ssfp
from mr_utils.recon.ssfp import PLANET

if __name__ == '__main__':

    N_alpha = 100
    nom_alphas = np.deg2rad(np.linspace(.1, 90, N_alpha))[::-1]

    N_dev = 100
    dev_alphas = np.linspace(-.10, .10, N_dev)

    M0 = 1
    T1 = .675
    T2 = .075
    df = 10
    TR = 10e-3
    lpcs = 10
    pcs = np.linspace(0, 2*np.pi, lpcs, endpoint=False)

    T1_err = np.zeros((nom_alphas.size, dev_alphas.size))
    T2_err = np.zeros(T1_err.shape)
    for ii, nom_alpha in tqdm(
            enumerate(nom_alphas), total=N_alpha, leave=False):
        for jj, dev_alpha in enumerate(dev_alphas):

            I = np.zeros(lpcs, dtype='complex')
            for kk, pc in enumerate(pcs):
                I[kk] = ssfp(T1, T2, TR, nom_alpha*(1 + dev_alpha), df, pc, M0)

            try:
                Meff, T10, T20 = PLANET(I, nom_alpha, TR, T1, disp=False)
                T1_err[ii, jj] = (T10 - T1)/T1*100
                T2_err[ii, jj] = (T20 - T2)/T2*100
            except AssertionError as e:
                tqdm.write(str(e))
                T1_err[ii, jj] = np.nan
                T2_err[ii, jj] = np.nan

            except ValueError as e:
                tqdm.write(str(e))
                T2_err[ii, jj] = np.nan
                T1_err[ii, jj] = np.nan

            except TypeError as e:
                tqdm.write(str(e))
                T2_err[ii, jj] = np.nan
                T1_err[ii, jj] = np.nan

    plt.subplot(1, 2, 1)
    plt.imshow(T1_err, extent=(.9, 1.1, .1, 90), aspect='auto')
    plt.title('Errors in T1, %')
    plt.ylabel('Nominal FA, degrees')
    plt.xlabel('Real FA/Nominal FA')

    plt.subplot(1, 2, 2)
    plt.imshow(T2_err, extent=(.9, 1.1, .1, 90), aspect='auto')
    plt.title('Errors in T2, %')
    plt.ylabel('Nominal FA, degrees')
    plt.xlabel('Real FA/Nominal FA')

    plt.show()
