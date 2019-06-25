'''Do CS in one dimension.

Notes
-----
The number of possible permutations is n!.  This is too many to
feasibly do an exhaustive search in greater than 1 dimension.

Consider the problem of T1 mapping: n images are aquired and pixels
are fit in 1 dimension to an exponential model.  Usually n is small,
so performing n! reconstructions to find the best one is feasbible.

What is the ``best one?''  If we knew the true reconstructed images,
the best one would be the reconstruction that minimizes the MSE
between itself and the true image.  Since we don't know the truth,
we could consider the best one to be the one that minimizes the
cost function.

This appears to work well for DCT, but breaks down for WVLT and FD.

TODO:
 - Try different weights
 - Make sure if no undersampling it works well
'''

from itertools import permutations
from functools import partial
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from skimage.measure import compare_nrmse

from mr_utils.utils import undersample
from mr_utils.cs import proximal_GD

if __name__ == '__main__':

    nT1s = 7
    T1s = np.linspace(0, 2.0, nT1s+1)[1:]

    # Get a T1 phantom to use
    N = 256
    nt = 5
    P = np.zeros((1, nt, N, N))
    r = .2
    X, Y = np.meshgrid(np.linspace(-1, 1, N), np.linspace(-1, 1, N))
    idx = np.sqrt(X**2 + Y**2) < r
    t = np.linspace(0, 3*np.min(T1s), nt+1)[1:]
    P[0, :, idx] = 1 - np.exp(-1*t/T1s[0])
    nph = 6
    tt = np.linspace(0, 2*np.pi, nph, endpoint=False)
    m = .5
    xx, yy = m*np.cos(tt), m*np.sin(tt)
    for ii in range(nph):
        idx = np.sqrt((X - xx[ii])**2 + (Y - yy[ii])**2) < r
        P[0, :, idx] = 1 - np.exp(-1*t/T1s[ii+1])
    P = P.squeeze()
    # from mr_utils import view
    # view(P)

    # Undersample
    kspace = np.zeros(P.shape, dtype='complex')
    mask = np.zeros(P.shape, dtype=bool)
    for ii in range(nt):
        kspace[ii, ...], mask[ii, ...] = undersample(
            P[ii, ...].copy(), R=(3, 1), acs=(.1, .1),
            forward_fun=None, inverse_fun=None, method='gauss',
            ret_kspace=True, ret_mask=True)

    ax = (1, 2)
    forward = lambda x0: 1/np.sqrt(N**2)*np.fft.fftshift(np.fft.fft2(
        np.fft.ifftshift(x0, axes=ax), axes=ax), axes=ax)
    inverse = lambda x0: np.sqrt(N**2)*np.fft.fftshift(np.fft.ifft2(
        np.fft.ifftshift(x0*mask, axes=ax), axes=ax), axes=ax)
    # from  mr_utils import view
    # view(inverse(kspace))

    ## Sparsifying transforms
    # FD
    # sparsify = lambda x0: np.diff(np.concatenate((
    #     np.zeros(x0.shape[1:])[None, ...], x0)), axis=0)
    # unsparsify = lambda x0: x0.cumsum(axis=0)

    # 2nd derivative?
    sparsify = lambda x0: np.diff(
        x0, n=2, axis=0, prepend=np.zeros((2,) + x0.shape[1:]))
    unsparsify = lambda x0: x0.cumsum(axis=0).cumsum(axis=0)

    # # DCT
    # from scipy.fftpack import dct, idct
    # sparsify = lambda x0: dct(x0, type=2, axis=0, norm='ortho')
    # unsparsify = lambda x0: idct(x0, type=2, axis=0, norm='ortho')

    # # WVLT
    # from mr_utils.utils import Sparsify
    # S = Sparsify(wvlt='haar')
    # sparsify = S.forward_wvlt
    # unsparsify = S.inverse_wvlt

    from mr_utils import view
    view(sparsify(P))

    # Make sure transform is working
    assert np.allclose(
        unsparsify(sparsify(inverse(kspace))), inverse(kspace))

    run_recon = partial(
        proximal_GD,
        forward_fun=forward,
        inverse_fun=inverse,
        sparsify=sparsify,
        unsparsify=unsparsify,
        mode='soft',
        thresh_sep=True,
        selective=None,
        x=P,
        ignore_residual=False,
        ignore_mse=True,
        ignore_ssim=True,
        disp=False,
        silent=True,
        strikes=20)

    # Need to be able to put permutation indices into sparse term!
    cost_fun = lambda x0, alpha0: (
        .5*np.linalg.norm(np.abs(P) - np.abs(x0))**2 +
        alpha0*np.linalg.norm(sparsify(np.abs(x0)).flatten(), ord=1))

    # Find good alpha
    nalpha = 3
    # alphas = np.linspace(0, .02, nalpha+1)[1:]
    alphas = [0, 1e-2, 1e-1]
    cost = np.zeros(nalpha)
    for ii, alpha0 in tqdm(
            enumerate(alphas), leave=False, total=nalpha,
            desc='Find alpha'):
        recon = run_recon(y=kspace.copy(), alpha=alpha0)
        cost[ii] = cost_fun(recon, alpha0)

    num = (
        cost[0]*(alphas[1]**2 - alphas[2]**2) +
        cost[1]*(alphas[2]**2 - alphas[0]**2) +
        cost[2]*(alphas[0]**2 - alphas[1]**2))
    den = (
        cost[0]*(alphas[1] - alphas[2]) +
        cost[1]*(alphas[2] - alphas[0]) +
        cost[2]*(alphas[0] - alphas[1]))
    alpha0 = num/(2*den)

    print('Choosing alpha0: %g' % alpha0)

    # Try all different permutations
    perms = np.array(list(set(permutations(list(range(nt))))))
    print('WARNING: DOING %d RECONSTRUCTIONS!' % perms.shape[0])
    def run_loop(ii):
        '''Run for each possible permutation.'''

        # Get ordering
        idx = perms[ii]
        idx = idx + 1j*idx
        reorder = lambda x0: idx

        # Do reconstruction along T1 growth dimension
        recon = run_recon(
            y=kspace.copy(), alpha=alpha0, reorder_fun=reorder)

        # Compare MSE with truth and cost function value
        err = compare_nrmse(np.abs(P), np.abs(recon))
        cost = cost_fun(recon, alpha0)
        return(ii, err, cost)

    # Run in parallel
    chunksize = 3
    with Pool() as pool:
        res = list(tqdm(
            pool.imap(run_loop, range(perms.shape[0]), chunksize),
            total=perms.shape[0], leave=False))
    res = np.array(res)
    res = res[res[:, 0].argsort()]
    err = res[:, 1]
    cost = res[:, 2]

    print('Best MSE  was %d' % np.argmin(err))
    print('Best COST was %d' % np.argmin(cost))

    plt.plot(err/np.max(err), label='MSE')
    plt.plot(cost/np.max(cost), label='COST')
    plt.plot(
        np.argmin(cost),
        (cost/np.max(cost))[np.argmin(cost)], '*', label='Best Cost')
    plt.plot(
        np.argmin(err),
        (err/np.max(err))[np.argmin(err)], '*', label='Best MSE')
    plt.legend()
    plt.title('Normalized MSE and COST')
    plt.show()

    # Run without reordering
    recon_no = run_recon(
        kspace.copy(), alpha=alpha0, reorder_fun=None)

    # Run with the best COST
    # idx = perms[np.argmin(cost)]
    idx = perms[np.argmin(err)] # minimize err to make sure working
    print('Perm: %s' % str(idx.tolist()))
    idx = idx + 1j*idx
    reorder = lambda x0: idx
    recon_wo = run_recon(
        kspace.copy(), alpha=alpha0, reorder_fun=reorder)

    # Show diff between the two
    print('Diff: %g' % compare_nrmse(
        np.abs(recon_no), np.abs(recon_wo)))

    from mr_utils import view
    view(recon_wo)
    # view(recon_no - recon_wo)
    view(P - recon_wo)

    # Compare T1 relaxation curve
    px, py = int(N/2), int(N/2)
    plt.plot(np.abs(recon_wo[:, px, py]), label='Recon With Order')
    plt.plot(np.abs(recon_no[:, px, py]), label='Recon No Order')
    plt.plot(np.abs(P[:, px, py]), '--', label='True')
    plt.plot(
        np.abs(inverse(kspace)[:, px, py]), ':', label='Zero-pad')
    plt.legend()
    plt.show()
