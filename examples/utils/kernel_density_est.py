'''Attempting to solve for coefficients which minimize MSE using KDE.

What we'd like to do is derive an expression from a standard normal kernel
density estimator to find the values of the current coefficient locations.
What would be super is if these values minimized the mean square error with
the pdf estimate of x.
'''

import numpy as np
from scipy.fftpack import dct
from scipy.stats import gaussian_kde
from scipy.optimize import root #, minimize
from tqdm import trange, tqdm
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Make a signal k-sparse in DCT
    # np.random.seed(0)
    N = 128
    k = 5
    D = dct(np.eye(N))
    true_idx = np.sort(np.random.choice(N, k))
    # print(true_idx)
    # plt.plot(D[:, true_idx])
    # plt.show()
    c_true = np.zeros(N)
    c_true[true_idx] = np.random.random(k)
    x_pi = np.dot(D, c_true)

    # Now create a scrambled signal that should have an identical distributions
    x = np.random.permutation(x_pi)

    # Instead of matching histograms, let's try matching probability density
    # estimates from kernel density estimators,
    # Make our kernel the standard normal and choose bandwidth in a simple way
    L = 100
    Y = np.linspace(np.min(D.flatten()), np.max(D.flatten()), L)
    kernel0 = gaussian_kde(x_pi).evaluate(Y)
    kernel1 = gaussian_kde(x).evaluate(Y)
    # plt.plot(Y, kernel0)
    # plt.plot(Y, kernel1, '--')
    # plt.show()

    # HOW DO I FIND C!?!?
    # We can find it pretty well if we have k <= 2, which isn't very good...
    c0 = np.ones(k)
    h = gaussian_kde(x).factor/4
    kernel_ref = gaussian_kde(x, bw_method=h).evaluate(Y)
    # obj = lambda x: np.linalg.norm(gaussian_kde(
    #     D[:, true_idx].dot(x), bw_method=h).evaluate(Y) - kernel_ref)
    # res = minimize(obj, c0)
    # print(c_true[true_idx])
    # print(res)

    # Try finding c by finding root, do a multistart
    fun = lambda x: gaussian_kde(
        D[:, true_idx].dot(x), bw_method=h).evaluate(Y) - kernel_ref
    winner = np.ones(k)
    winner_score = np.sum(np.abs(fun(winner))**2)
    tol = 1e-8
    for ii in trange(20, leave=False):
        c0 = np.random.random(k)
        res = root(fun, c0, method='lm')
        score = np.sum(np.abs(fun(res['x']))**2)
        if score < winner_score:
            winner = res['x']
            winner_score = score
            tqdm.write('New winner: %g' % winner_score)

            # If we did good enough, run with this one
            if winner_score < tol:
                break

    print(c_true[true_idx], winner)

    plt.plot(Y, kernel_ref)
    plt.plot(Y, gaussian_kde(
        D[:, true_idx].dot(winner), bw_method=h).evaluate(Y), '--')
    plt.show()
