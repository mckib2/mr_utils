'''A couple strategies for manipulating coefficient power.

"Bulking up" the first coefficients seems less effective than "whittling down"
the least coefficients.  In particular, bulking up leads to a tradeoff
between lowering the middle coefficients slightly while raising lower
coefficients quite a bit.
'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.data import camera
from scipy.signal import decimate
from scipy.fftpack import dct, idct

from mr_utils.utils.orderings import whittle_down, bulk_up

if __name__ == '__main__':

    # Get a camera man
    R = 4  # decimate so the matching will go more quickly
    x = decimate(decimate(camera().astype(float), R, axis=0), R, axis=1)

    # Use the discrete cosine transform
    norm = 'ortho'
    T = lambda x: dct(dct(x, axis=0, norm=norm), axis=1, norm=norm)
    Ti = lambda x: idct(idct(x, axis=0, norm=norm), axis=1, norm=norm)
    assert np.allclose(x, Ti(T(x)))

    # Try to "bulk up" the first k percent of coefficients
    k = .01
    idx = bulk_up(x, T, Ti, k)

    match = x[np.unravel_index(idx, x.shape)].reshape(x.shape)
    coeffs0 = -np.sort(-np.abs(T(x).flatten()))
    coeffs1 = -np.sort(-np.abs(T(match).flatten()))
    plt.semilogy(coeffs1/coeffs0)
    plt.title('log(T(x)/T(matched))')
    plt.show()

    # Now try to "whittle down" the last k percent of coefficients
    k = .1
    idx = whittle_down(x, T, Ti, k)

    match = x[np.unravel_index(idx, x.shape)].reshape(x.shape)
    coeffs0 = -np.sort(-np.abs(T(x).flatten()))
    coeffs1 = -np.sort(-np.abs(T(match).flatten()))
    plt.plot(coeffs1/coeffs0)
    plt.title('T(x)/T(matched)')
    plt.show()
