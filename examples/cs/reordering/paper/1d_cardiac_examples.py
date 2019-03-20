'''Show how we perform with an actual blood time curve.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.load_data import load_mat
from mr_utils.utils import Sparsify
from mr_utils import view
from mr_utils.cs import relaxed_ordinator

if __name__ == '__main__':

    filename = 'meas_MID42_CV_Radial7Off_triple_2.9ml_FID242_GROG.mat'
    data = load_mat(filename, key='Image')
    # view(data)

    pt = (133, 130)
    px = data[pt[0], pt[1], :, 0]
    pxr = px.real/np.max(np.abs(px.real))
    pxi = px.imag/np.max(np.abs(px.imag))
    Sr = Sparsify(pxr)
    Si = Sparsify(pxi)

    # plt.plot(px.real)
    # plt.plot(px.imag)
    # plt.title('Real/Imag time curve')
    # plt.show()

    # # Try Finite Differences
    # plt.plot(Sr.forward_fd(px.real))
    # plt.plot(Si.forward_fd(px.imag))
    # plt.show()
    #
    pi_sortr = np.argsort(pxr)[::-1]
    pi_sorti = np.argsort(pxi)[::-1]

    #
    # plt.plot(-np.sort(-np.abs(Sr.forward_fd(px.real[pi_sortr]))))
    # plt.plot(-np.sort(-np.abs(Si.forward_fd(px.imag[pi_sorti]))))
    # plt.show()

    # Try finding a better one?



    pi_lsr = relaxed_ordinator(
        pxr, lam=.08, k=10, unsparsify=Sr.inverse_dct)
    pi_lsi = relaxed_ordinator(
        pxi, lam=.1, k=13, unsparsify=Si.inverse_dct)


    # LOOK AT IT
    plt.plot(-np.sort(-np.abs(Sr.forward_dct(pxr[pi_sortr]))),
             label='DCT, real')
    plt.plot(-np.sort(-np.abs(Si.forward_dct(pxi[pi_sorti]))),
             label='DCT, imag')

    plt.plot(-np.sort(-np.abs(Sr.forward_dct(pxr[pi_lsr]))), '--',
             label='Lagrangian DCT, real')
    plt.plot(-np.sort(-np.abs(Si.forward_dct(pxi[pi_lsi]))), '--',
             label='Lagrangian DCT, imag')
    plt.legend()
    plt.show()
