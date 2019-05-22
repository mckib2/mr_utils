'''Update ordering estimate at each step.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.cs import gd
from mr_utils.utils import Sparsify, neural_sort

if __name__ == '__main__':

    N = 1000
    x = np.arange(N)
    n = np.random.normal(0, 1, N)
    y = x + n

    # idx = np.argsort(y)
    P = neural_sort(y)
    idx = np.argmax(P, axis=0)

    # plt.plot(x[::-1])
    # plt.plot(x[idx], '--')
    # plt.plot(x[np.argsort(y)][::-1], ':')
    # plt.show()

    print(np.linalg.norm(x[idx] - x[::-1]))
    print(np.linalg.norm(x[np.argsort(y)] - x))


    # S = Sparsify()
    # update = lambda x0: S.forward_fd(x0)
    #
    # recon = gd(
    #     shape=(N,),
    #     updates=[],
    #     x0=y,
    #     alphas=[],
    #     costs=[],
    #     maxiter=200,
    #     tol=1e-8,
    #     disp=False)
