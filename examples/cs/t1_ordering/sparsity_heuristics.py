'''Take a look at the transforms of T1 curve.'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct
import pywt

from mr_utils.utils import gini

if __name__ == '__main__':

    T1 = 1.2
    # nts = [6, 1000, 1e6]
    nts = [6]
    # Transformations under consideration
    TX = {
        'Identity': lambda x0: x0,
        '1st Diff': lambda x0: np.diff(x0, n=1, prepend=0),
        # '2nd Diff': lambda x0: np.diff(s, n=2, prepend=[0, 0]),
        'DCT': lambda x0: dct(x0, norm='ortho'),
        'WVLT': lambda x0: np.concatenate(pywt.dwt(x0, wavelet='db2'))
    }
    gini_scores = np.zeros((len(nts), len(TX)))
    l1_scores = gini_scores.copy()
    for ii, nt in enumerate(nts):

        t = np.linspace(0, 3*T1, nt+1)[1:]
        s = 1 - np.exp(-1*t/T1)
        # s = s[[4, 1, 3, 0, 5, 2]]
        nx = int(np.ceil(np.sqrt(len(TX))))
        ny = nx

        idx = 0
        for key, fun in TX.items():
            # plt.subplot(nx, ny, idx+1)
            tx = fun(s)
            # plt.plot(t, tx)
            # plt.title('%s: %d samples' % (key, nt))
            gini_scores[ii, idx] = gini(tx)
            l1_scores[ii, idx] = np.linalg.norm(tx, ord=1)
            # plt.xlabel('Gini: %g' % gini_scores[ii, idx])
            idx += 1
        # plt.show()
    l1_scores /= np.max(l1_scores)
    gini_scores = 1 - gini_scores
    # gini_scores = 1/gini_scores
    # gini_scores /= np.max(gini_scores)


    xx = list(TX.keys())
    for ii, nt in enumerate(nts):
        plt.plot(xx, gini_scores[ii, :], label='Gini: %d' % nt)
        plt.plot(xx, l1_scores[ii, :], '--', label='l1: %d' % nt)
    plt.title('Sparsity measures of transformed T1 growth curve')
    plt.legend()
    plt.show()
