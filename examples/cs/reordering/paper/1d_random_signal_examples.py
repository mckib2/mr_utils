'''1D examples to show us that we can find effective orderings.'''

from functools import partial
from time import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from scipy.optimize import minimize

from mr_utils.cs import ordinator1d, relaxed_ordinator
from mr_utils.cs.relaxed_ordinator import obj
from mr_utils.utils import Sparsify


def find_k(lam, x, sparsify, unsparsify, N):
    '''Find best k given lambda.'''

    pobj = partial(obj, x=x, lam=lam, unsparsify=unsparsify, norm=False)
    cost = np.zeros(N)
    for kk in range(int(N)):
        cost[kk] = pobj(sparsify(x[relaxed_ordinator(
            x, lam=lam, k=kk, unsparsify=unsparsify)]))
    return(np.argmin(cost), np.min(cost))

if __name__ == '__main__':

    # Let's make a signal, any start with a random signal
    N = 70
    np.random.seed(2)
    x = np.random.normal(1, 1, N)
    S = Sparsify(x)

    do_fd = False
    do_dct = True

    # Finite differences
    if do_fd:
        pi_sort = np.argsort(x)[::-1]
        pi_ls = relaxed_ordinator(x, lam=4, k=10, unsparsify=S.inverse_fd,
                                  transform_shape=(x.size-1,))

        # Let's look at the results
        plt.plot(-np.sort(-np.abs(S.forward_fd(x))), label='x')
        plt.plot(-np.sort(-np.abs(S.forward_fd(x[pi_sort]))), label='sort(x)')
        plt.plot(-np.sort(-np.abs(S.forward_fd(x[pi_ls]))), label='Lagrangian')
        plt.legend()
        plt.title('Finite Differences')
        plt.show()

    # DCT
    if do_dct:
        pi_sort = np.argsort(x)[::-1]
        # pi_ord = ordinator1d(x, k=3, inverse=S.inverse_dct, chunksize=100)

        # We need to find the correct k and lambda for this N
        # Had to hand tune to lam=0.15 and k=6 for N=70
        lam = 0.15
        k = 6
        pi_ls = relaxed_ordinator(x, lam=lam, k=k, unsparsify=S.inverse_dct)

        # Let's look at the results
        plt.plot(x, label='x')
        plt.plot(x[pi_sort], label='sort(x)')
        # plt.plot(x[pi_ord], label='Exhaustive')
        plt.plot(x[pi_ls], label='Lagrangian')
        plt.legend()
        plt.show()

        plt.plot(-np.sort(-np.abs(S.forward_dct(x))), label='x')
        plt.plot(-np.sort(-np.abs(S.forward_dct(x[pi_sort]))), label='sort(x)')
        # plt.plot(
        #     -np.sort(-np.abs(S.forward_dct(x[pi_ord]))), label='Exhaustive')
        plt.plot(
            -np.sort(-np.abs(S.forward_dct(x[pi_ls]))), label='Lagrangian')
        plt.legend()
        plt.show()
