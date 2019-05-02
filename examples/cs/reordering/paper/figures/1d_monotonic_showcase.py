'''Make some 1D signals and show how monotinic ordering works.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.utils import Sparsify, piecewise

def fix_axis():
    '''Remove ticks from axis.'''
    frame1 = plt.gca()
    frame1.axes.xaxis.set_visible(False)
    frame1.axes.yaxis.set_visible(False)
    plt.box(False)

if __name__ == '__main__':

    # Create a signal, any signal, for us to work with
    N = 100
    k = 5 # number of sinusoids
    n = np.linspace(0, 2*np.pi, N)
    x = np.sum(
        np.sin(n[None, :]/np.random.random(k)[:, None]), axis=0)
    S = Sparsify()
    l1 = lambda x0: np.linalg.norm(x0, ord=1)
    sh = (3, 3)
    text_loc = (0, 0)

    # Do DCT first
    plt.subplot(*sh, 1)
    plt.plot(x)
    plt.title('x[n]')

    plt.subplot(*sh, 2)
    dx = S.forward_dct(x)
    dxs = S.forward_dct(np.sort(x)[::-1])
    plt.plot(dx, label='DCT(x[n])')
    plt.plot(dxs, label='DCT(sort(x[n]))')
    plt.title('DCT')
    # plt.text(*text_loc, 'l1 norms: %g, %g' % (l1(dx), l1(dxs)))
    plt.legend()

    plt.subplot(*sh, 3)
    plt.plot(-np.sort(-np.abs(dx)), label='DCT(x[n])')
    plt.plot(-np.sort(-np.abs(dxs)), label='DCT(sort(x[n]))')
    plt.title('Decay of sorted DCT coefficients')
    plt.legend()

    # Now TV
    groups = np.random.randint(1, 10, 4*k)
    vals = np.random.random(groups.size)
    y = piecewise(groups, vals)
    plt.subplot(*sh, 4)
    plt.plot(y)
    plt.title('y[n]')

    plt.subplot(*sh, 5)
    ty = S.forward_fd(y)
    tys = S.forward_fd(np.sort(y))
    plt.plot(ty, label='TV(y[n])')
    plt.plot(tys, label='TV(sort(y[n]))')
    plt.title('TV')
    # plt.text(*text_loc, 'l1 norms: %g, %g' % (l1(ty), l1(tys)))
    plt.legend()

    plt.subplot(*sh, 6)
    plt.plot(-np.sort(-np.abs(ty)), label='TV(y[n])')
    plt.plot(-np.sort(-np.abs(tys)), label='TV(sort(y[n]))')
    plt.title('Decay of sorted TV coefficients')
    plt.legend()

    plt.subplot(*sh, 7)
    z = np.random.normal(0, 1, N)
    plt.plot(z)
    plt.title('z[n]')

    plt.subplot(*sh, 8)
    wz = S.forward_wvlt(z)
    wzs = S.forward_wvlt(np.sort(z))
    plt.plot(wz, label='H(z[n])')
    plt.plot(wzs, label='H(sort(z[n]))')
    plt.title('Wavelet')
    # plt.text(*text_loc, 'l1 norms: %g, %g' % (l1(wz), l1(wzs)))
    plt.legend()

    plt.subplot(*sh, 9)
    plt.plot(-np.sort(-np.abs(wz)), label='H(z[n])')
    plt.plot(-np.sort(-np.abs(wzs)), label='H(sort(z[n]))')
    plt.title('Decay of sorted wavelet coefficients')
    plt.legend()


    # Remove all the dumb stuff from axes
    for ii in range(np.prod(sh)):
        plt.subplot(*sh, ii+1)
        fix_axis()

    plt.show()
