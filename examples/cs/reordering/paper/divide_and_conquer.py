'''Split the image estimate into many image estimates.'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment as lsa
from scipy.spatial.distance import cdist
from scipy.fftpack import dct, idct
from tqdm import trange, tqdm

from mr_utils.utils.orderings import inverse_permutation

def match_atom(x, D):
    '''Find least cost assignment from x to an atom of D.'''

    cost = np.zeros(D.shape[1])
    assignment = dict()
    for ii in trange(D.shape[1], leave=False):
        C = cdist(x[:, None], D[:, ii][:, None])
        rows, cols = lsa(C)
        assignment[ii] = cols
        cost[ii] = C[rows, cols].sum()
    jj = np.argmin(cost)
    return(jj, assignment[jj])

if __name__ == '__main__':

    # Make a signal
    N = 20
    # x = np.cos(np.linspace(0, 2*np.pi, N))
    np.random.seed(0)
    x = np.random.random(N)

    # Make a dictionary, must be orthonormal!
    # D = orth(np.random.random((N, N)))
    D = dct(np.eye(N))
    D /= np.max(D, axis=0)

    # plt.plot(x)
    # plt.show()

    resid = x.copy()
    maxiter = 500
    s = np.zeros((maxiter, N))
    cond = np.inf
    tol = 1e-1
    kk = 0
    assignments = dict()
    parts = dict()
    # TODO: Parallelize loop
    for kk in trange(maxiter, leave=False):
        ii, idx = match_atom(resid, D)
        assignments[kk] = idx # store each ordering
        iidx = inverse_permutation(idx)

        # c = D[iidx, ii].dot(resid)
        c = np.linalg.lstsq(D[iidx, :], resid, rcond=None)[0][ii]
        s[kk, :] = c*D[:, ii]

        # What part of resid is s[kk, iidx]?
        parts[kk] = s[kk, iidx]/resid

        resid[idx] -= s[kk, :]
        cond = np.linalg.norm(resid)/np.linalg.norm(x)
        tqdm.write('%d: %g, ii: %d' % (kk, cond, ii))

        if cond < tol:
            break

    plt.plot(s[:kk, :].T)
    plt.title('Component signals, sk')
    plt.show()

    plt.plot(dct(s[:kk, :]))
    plt.title('Single DCT coefficients for each sk')
    plt.show()

    # Make sure we can reover the actual signal, should be the same minus
    # remaining residual
    xhat = np.zeros(x.shape)
    for kk in assignments:
        xhat[assignments[kk]] += s[kk, :]
    plt.plot(x)
    plt.plot(xhat, '--')
    plt.show()

    # Now we need to encorporate all the sk in the gradient descent update.
    # Use average sparsity?  Include all terms and adjust lambda?  I'll have
    # to think about the best thing to do here

    # For proximal gradient, seems like there would be a threshold step for
    # each sk, unsparsify each sk, and then add all the updates together to
    # get the final update to compute residual from.  So you could use hard
    # thresholding, expecting only one coefficient per sk -- pretty slick.
    # But it does look like proximal_GD will need to be rewritten with this
    # method in mind...

    # We'll also need to store where (and maybe in what order) each sk is
    # generated.  We'll need this information when we get ready to sparsify
    # before thresholding.  Each sk should be generated the same way sk is
    # generated when finding prior reordering.  This adds another layer of
    # dependence on the quality of the prior image estimate.

    # The idea I had was to group sk by percentage of remaining residual.

    # Now do the compressed sensing thing
    n = int(N*.5)
    samp_idx = np.sort(np.random.choice(np.arange(N), n, False))
    y = np.zeros(x.shape)
    y[samp_idx] = x[samp_idx]
    plt.plot(x)
    plt.plot(y)
    plt.show()

    # Now start thresholding each sk
    recon = np.zeros(x.shape)
    resid = y.copy()
    for kk in assignments:

        # Get the first part of the signal
        sk = resid*parts[kk]
        resid -= sk

        # When reordered it should be 1-sparse
        skt = D.dot(sk[assignments[kk]])
        c0 = np.zeros(skt.shape)
        idx = np.argmax(np.abs(skt))
        c0[idx] = skt[idx]
        sk = D.dot(c0)[inverse_permutation(assignments[kk])]*2/N

        recon += sk

    plt.plot(x, label='True')
    plt.plot(xhat, label='Possible')
    plt.plot(recon, label='Recon')
    plt.show()
