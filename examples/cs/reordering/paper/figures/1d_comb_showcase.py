'''Compare monotonic and combinatoric ordering schemes.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.utils import Sparsify, gini
from mr_utils.cs import relaxed_ordinator, ordinator1d

if __name__ == '__main__':

    S = Sparsify()
    l1 = lambda x0: np.linalg.norm(x0, ord=1)
    sh = (1, 3)

    plt.subplot(*sh, 1)
    N = 10
    k = 3 # number of sinusoids
    n = np.linspace(0, 2*np.pi, N)
    x = np.sum(
        np.sin(n[None, :]/np.random.random(k)[:, None]), axis=0)
    plt.plot(x)
    plt.title('x[n]')

    plt.subplot(*sh, 2)
    k0 = 5
    idx = ordinator1d(
        x, k=k0, inverse=S.inverse_dct, chunksize=10, pdf=None,
        pdf_metric=None, forward=S.forward_dct, disp=False)
    # idx = relaxed_ordinator(
    #     x, lam=.3, k=k0, unsparsify=S.inverse_dct, norm=False,
    #     warm=False, transform_shape=None, disp=False)

    dxs = S.forward_dct(np.sort(x)[::-1])
    dxc = S.forward_dct(x[idx])
    plt.plot(dxs, label='DCT(sort(x[n]))')
    plt.plot(dxc[::-1], label='DCT(ord(x[n]))')
    plt.title('DCT (%g, %g)' % (l1(dxs), l1(dxc)))
    plt.xlabel('%g, %g' % (gini(dxs), gini(dxc)))
    plt.legend()

    plt.subplot(*sh, 3)
    plt.plot(-np.sort(-np.abs(dxs)), label='DCT(sort(x[n]))')
    plt.plot(-np.sort(-np.abs(dxc)), label='DCT(ord(x[n]))')
    plt.title('Decay of sorted DCT coefficients')
    plt.legend()



    plt.show()
