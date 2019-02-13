'''Attempting to solve for coefficients which minimize MSE using KDE.'''

import numpy as np
from scipy.fftpack import dct
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Make a signal k-sparse in DCT
    N = 256
    k = 10
    D = dct(np.eye(N))
    true_idx = [int(N/(ii + 1)) - 1 for ii in range(k)]
    c_true = np.zeros(N)
    c_true[true_idx] = 2.5
    x_pi = np.dot(D, c_true)

    # Now create a scrambled signal that should have an identical distributions
    x = np.random.permutation(x_pi)

    # Instead of matching histograms, let's try matching probability density
    # estimates from kernel density estimators,
    # Make our kernel the standard normal and choose bandwidth in a simple way
    kernel0 = gaussian_kde(x_pi)
    kernel1 = gaussian_kde(x)
    Y = np.linspace(np.min(x), np.max(x), 100)
    plt.plot(kernel0(Y))
    plt.plot(kernel1(Y), '--')
    plt.show()

    # Now solve for the correct values of c
    c = np.zeros(len(true_idx))
    A = D[:, true_idx]
    for kk in true_idx:
        pass

    plt.plot(c_true[true_idx])
    plt.plot(c, '--')
    plt.show()
