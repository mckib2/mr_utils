'''Shuffle ordering.'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from mr_utils.utils import piecewise


if __name__ == '__main__':

    # Sparse in TV
    # k = 5
    # groups = np.random.randint(1, 50, 5*k)
    # vals = np.random.random(groups.size)
    # x = piecewise(groups, vals)
    # N = x.size
    N = 1000
    x = np.sin(np.arange(N)*2*np.pi*2/N) + 1
    x[x > .5] = 1
    x[x < .5] = 0

    fft = lambda x0: np.fft.fftshift(np.fft.fft(np.fft.fftshift(x0)))
    ifft = lambda x0: np.fft.ifftshift(np.fft.ifft(np.fft.ifftshift(
        x0)))

    ufac = .2
    M = int(ufac*N)
    xx = np.linspace(norm.ppf(0.01), norm.ppf(0.99), N)
    p = norm.pdf(xx, scale=.1)
    # plt.plot(p)
    # plt.show()
    idx = np.random.choice(
        np.arange(N), size=M, replace=False, p=p/np.sum(p))
    X = fft(x)
    # plt.plot(np.abs(X))
    # plt.plot(idx, np.abs(X[idx]), 'o')
    # plt.show()

    Xu = np.zeros(N, dtype=X.dtype)
    mask = np.zeros(N, dtype=bool)
    mask[idx] = True
    Xu[idx] = X[idx]
    xu = ifft(Xu)
    # plt.plot(x)
    # plt.plot(np.abs(xu), '--')
    # plt.show()

    # # Solve using the subgradient method
    # fid = lambda x0: .5*np.linalg.norm(fft(x0)*mask - Xu)**2
    # fid_grad = lambda x0: ifft(fft(x0)) - xu
    # D = np.diff(np.eye(N), prepend=0) # pylint: disable=E1123
    # tv = lambda x0: np.linalg.norm(np.dot(D, x0), ord=1)
    # tv_grad = lambda x0: np.dot(D.T, np.sign(np.dot(D, np.abs(x0))))
    #
    # from mr_utils.cs import gd
    # xhat, cost = gd(
    #     (N,),
    #     updates=[fid_grad, tv_grad],
    #     x0=xu,
    #     alphas=[1, .002],
    #     costs=[fid, tv],
    #     maxiter=20,
    #     tol=1e-8,
    #     disp=False)
    #
    # plt.plot(cost)
    # plt.show()
    #
    # plt.plot(x)
    # plt.plot(np.abs(xhat), '--')
    # plt.plot(np.abs(xu), ':')
    # plt.show()

    # Solve using proximal gradient descent
    from mr_utils.cs import proximal_GD
    from mr_utils.utils import neural_sort

    ridx = np.argsort(np.abs(xu))

    def sample_gumbel(shape, eps=1e-20):
        U = np.random.uniform(0, 1, shape)
        return -np.log(-np.log(U + eps) + eps)

    nidx = np.argmax(neural_sort(np.abs(xu) + sample_gumbel(xu.shape), tau=1e-20), axis=0)

    u, c = np.unique(nidx, return_counts=True)
    dup = u[c > 1]
    print(dup)

    methods = [
        (.03, None),
        (.03, lambda x0: ridx[::-1]),
        (.03, lambda x0: np.argsort(np.abs(xhat[:, 0]))[::-1]),
        (.005, lambda x0: nidx[::-1])
    ]

    plt.plot(x)
    plt.plot(np.abs(xu), label='xu')
    xhat = np.zeros((N, len(methods)), dtype=xu.dtype)
    for ii, method in enumerate(methods):
        xhat[..., ii] = proximal_GD(
            Xu.copy(),
            forward_fun=fft,
            inverse_fun=ifft,
            sparsify=lambda x0: np.diff(x0), # pylint: disable=E1123
            unsparsify=lambda x0: np.cumsum(
                np.concatenate(([x[0]], x0))),
            reorder_fun=method[1],
            mode='soft',
            alpha=method[0],
            thresh_sep=False,
            selective=None,
            x=x.copy(),
            ignore_residual=False,
            ignore_mse=True,
            ignore_ssim=True,
            disp=True,
            maxiter=200,
            strikes=0)


        plt.plot(np.abs(xhat[..., ii]), '--', label=str(ii))
    plt.legend()
    plt.show()
