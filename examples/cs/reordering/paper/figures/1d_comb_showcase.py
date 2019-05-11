'''Compare monotonic and combinatoric ordering schemes.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.utils import Sparsify, gini, piecewise
from mr_utils.cs import ordinator1d

if __name__ == '__main__':

    S = Sparsify()
    l1 = lambda x0: np.linalg.norm(x0, ord=1)
    sh = (3, 3)

    # plt.subplot(*sh, 1)
    N = 10
    # k = 3 # number of sinusoids
    # n = np.linspace(0, 2*np.pi, N)
    # x = np.sum(
    #     np.sin(n[None, :]/np.random.random(k)[:, None]), axis=0)
    # plt.plot(x)
    # plt.title('x[n]')
    #
    # plt.subplot(*sh, 2)
    # k0 = k
    # idx = ordinator1d(
    #     x, k=k0, forward=S.forward_dct, inverse=S.inverse_dct,
    #     chunksize=10, pdf=None, pdf_metric=None,
    #     sparse_metric=lambda x0: 1/gini(x0), disp=False)
    # # idx = relaxed_ordinator(
    # #     x, lam=.3, k=k0, unsparsify=S.inverse_dct, norm=False,
    # #     warm=False, transform_shape=None, disp=False)
    #
    # dxs = S.forward_dct(np.sort(x)[::-1])
    # dxc = S.forward_dct(x[idx])
    # plt.plot(dxs, label='DCT(sort(x[n]))')
    # plt.plot(dxc[::-1], label='DCT(ord(x[n]))')
    # plt.title('DCT (%g, %g)' % (l1(dxs), l1(dxc)))
    # plt.xlabel('%g, %g' % (gini(dxs), gini(dxc)))
    # plt.legend()
    #
    # plt.subplot(*sh, 3)
    # plt.plot(-np.sort(-np.abs(dxs)), label='DCT(sort(x[n]))')
    # plt.plot(-np.sort(-np.abs(dxc)), label='DCT(ord(x[n]))')
    # plt.title('Decay of sorted DCT coefficients')
    # plt.legend()
    # # np.savez('dct', x, dxs, dxs, k0, idx)
    # # plt.savefig('dct.png')

    # plt.subplot(*sh, 4)
    # groups = np.random.randint(1, 10, k)
    # vals = np.random.random(groups.size)
    # y = piecewise(groups, vals)
    # plt.plot(y)
    # plt.title('y[n]')
    #
    # plt.subplot(*sh, 5)
    # k0 = k
    # idx = ordinator1d(
    #     y, k=k0, forward=S.forward_fd, inverse=S.inverse_fd,
    #     chunksize=10, pdf=None, pdf_metric=None,
    #     sparse_metric=lambda x0: 1/gini(x0), disp=False)
    #
    # dys = S.forward_fd(np.sort(y))
    # dyc = S.forward_fd(y[idx])
    # plt.plot(dys, label='TV(sort(y[n]))')
    # plt.plot(dyc[::-1], label='TV(ord(y[n]))')
    # plt.title('TV (%g, %g)' % (l1(dys), l1(dyc)))
    # plt.xlabel('%g, %g' % (gini(dys), gini(dyc)))
    # plt.legend()
    #
    # plt.subplot(*sh, 6)
    # plt.plot(-np.sort(-np.abs(dys)), label='TV(sort(y[n]))')
    # plt.plot(-np.sort(-np.abs(dyc)), label='TV(ord(y[n]))')
    # plt.title('Decay of sorted TV coefficients')
    # plt.legend()
    #

    plt.subplot(*sh, 7)
    z = np.random.normal(0, 1, N)
    plt.plot(z)
    plt.title('z[n]')

    plt.subplot(*sh, 8)
    k0 = 3
    idx = ordinator1d(
        z, k=k0, forward=S.forward_wvlt, inverse=S.inverse_wvlt,
        chunksize=10, pdf=None, pdf_metric=None,
        sparse_metric=lambda x0: 1/gini(x0), disp=False)

    wzs = S.forward_wvlt(np.sort(z))
    wzc = S.forward_wvlt(z[idx])

    plt.plot(wzs, label='H(sort(z[n]))')
    plt.plot(wzc, label='H(ord(z[n]))')
    plt.title('Wavelet (%g, %g)' % (l1(wzs), l1(wzc)))
    plt.xlabel('%g, %g' % (gini(wzs), gini(wzc)))
    plt.legend()

    plt.subplot(*sh, 9)
    plt.plot(-np.sort(-np.abs(wzs)), label='H(sort(z[n]))')
    plt.plot(-np.sort(-np.abs(wzc)), label='H(ord(z[n]))')
    plt.title('Decay of sorted wavelet coefficients')
    plt.legend()

    plt.show()


    # # Remove all the dumb stuff from axes
    # for ii in range(np.prod(sh)):
    #     plt.subplot(*sh, ii+1)
    #     fix_axis()

    # plt.show()
