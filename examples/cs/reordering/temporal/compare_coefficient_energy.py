'''Compare how significant coefficients perform compared to power law.

Notes
-----
Well this was inconclusive...  Need a better test probably.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.utils import gini, Sparsify, piecewise
from mr_utils.utils.orderings import get_gini_sort2
from mr_utils.cs import proximal_GD
from mr_utils.cs.models import UFT

if __name__ == '__main__':

    # Make a random signal
    num_groups = 100
    groups = np.random.randint(1, 10, num_groups)
    vals = np.random.random(groups.size)
    x = piecewise(groups, vals)
    x = np.random.permutation(x)
    N = x.size
    n = int(.6*N)

    S = Sparsify()
    mask = np.zeros(N, dtype=bool)
    ctr = int(N/2)
    mask[ctr] = True # always sample center
    p = (1 - (2*np.linspace(0, 1, N) - 1)**2)
    p /= np.sum(p)
    samp = np.random.choice(
        np.arange(N).astype(int), size=n, replace=False, p=p)
    mask[samp] = True
    uft = UFT(mask)
    y = uft.forward_ortho(x)
    # plt.plot(np.abs(y))
    # plt.show()

    # Try sorting different ways
    idx_mono = np.argsort(x)
    idx_gini = get_gini_sort2(x)

    # Try finite differences
    dx = np.diff(x)
    dxs = np.diff(x[idx_mono])
    dgs = np.diff(x[idx_gini])

    l1 = lambda x0: np.linalg.norm(x0, ord=1)
    print(l1(dx), gini(dx))
    print(l1(dxs), gini(dxs))
    print(l1(dgs), gini(dgs))

    # Reconstruct
    reorder_funs = [idx_mono, idx_gini]
    xhat = np.zeros((len(reorder_funs), N))
    for ii, reorder_fun0 in enumerate(reorder_funs):
        xhat[ii, :] = proximal_GD(
            y,
            forward_fun=uft.forward_ortho,
            inverse_fun=uft.inverse_ortho,
            sparsify=S.forward_fd,
            unsparsify=S.inverse_fd,
            reorder_fun=lambda x0: reorder_fun0,
            mode='soft',
            alpha=.000001,
            alpha_start=.5,
            thresh_sep=True,
            selective=None,
            x=x,
            ignore_residual=True,
            ignore_mse=False,
            disp=False,
            maxiter=100).real

    plt.plot(x)
    styles = ['--', ':.']
    for ii, reorder_fun in enumerate(reorder_funs):
        plt.plot(xhat[ii, :], styles[ii])
        print(np.linalg.norm(x - xhat[ii, :]))
    plt.show()

    # plt.plot(dx)
    # plt.plot(dxs)
    # plt.plot(dgs)
    # plt.show()
