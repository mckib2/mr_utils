'''Compare Gini index to l1, l0.
'''

import numpy as np
from tqdm import trange

from mr_utils.utils import gini, piecewise as make_signal
from mr_utils.utils.orderings import get_gini_sort, get_gini_sort2

if __name__ == '__main__':

    # Define params for piecewise constant signal
    k = 10 # number of groups
    M = 100 # length of groups

    # l1 norm, what we normally want to minimize
    l1 = lambda x0: np.linalg.norm(x0, ord=1)
    l0 = lambda x0: np.linalg.norm(x0, ord=0)

    # plt.plot(x)
    # plt.title('Piecewise constant signal')
    # plt.show()

    # # Make sure sorting does what we think it does
    # a = np.sort(x)
    # b = make_signal(n, vals, np.argsort(vals))
    # plt.plot(x)
    # plt.plot(a)
    # plt.plot(b, '--')
    # plt.show()

    # Monte Carlo it
    niter = 10000
    gini0 = np.zeros(niter)
    gini1 = gini0.copy()
    gini2 = gini0.copy()
    gini3 = gini0.copy()
    for ii in trange(niter, leave=False):

        # Make new signal
        n = np.random.randint(1, M, k)
        vals = np.random.random(k)
        x = make_signal(n, vals)
        x = np.random.permutation(x)

        # See what we get
        y = np.diff(x)
        ys = np.diff(np.sort(x))
        # l1_0 = l1(y)
        # l1_1 = l1(ys)
        # print('%g -> %g, %%%g' % (l1_0, l1_1, l1_0/l1_1))

        gini0[ii] = gini(y)
        gini1[ii] = gini(ys)
        # print('%g -> %g, %%%g' % (gini0, gini1, gini0/gini1))

        idx0 = get_gini_sort(vals)
        gs0 = np.diff(make_signal(n, vals[idx0]))

        idx1 = get_gini_sort2(vals)
        gs1 = np.diff(make_signal(n, vals[idx1]))

        # import matplotlib.pyplot as plt
        # plt.plot(gs)
        # plt.plot(ys)
        # plt.show()
        gini2[ii] = gini(gs0)
        gini3[ii] = gini(gs1)
        # print('%g -> %g, %%%g' % (gini0, gini2, gini0/gini2))

    print(np.mean(gini0))
    print(np.mean(gini1))
    print(np.mean(gini2))
    print(np.mean(gini3))
