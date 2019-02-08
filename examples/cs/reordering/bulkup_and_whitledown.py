'''A couple strategies for manipulating coefficient power.

This seems to depend a lot on the transform you want to be sparse in.  We
choose the DCT and CDF 9/7 wavelet transform for this example.

For the DCT, both techniques appear better than no reordering and are about
equivalent.

These techniques seem to do much better (for proper choice of k) with the
wavelet transform.  Both of these can perform much better than no reordering
at all.
'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.data import camera
from skimage.measure import compare_mse, compare_ssim
from scipy.signal import decimate
from scipy.fftpack import dct, idct
from pywt import threshold

from mr_utils.utils.orderings import whittle_down, bulk_up, inverse_permutation
from mr_utils.utils.wavelet import cdf97_2d_forward, cdf97_2d_inverse

if __name__ == '__main__':

    # Get a camera man
    R = 4  # decimate so the matching will go more quickly
    x = decimate(decimate(camera().astype(float), R, axis=0), R, axis=1)

    # Let's try a few different transforms:
    Ts = []
    Tis = []

    # Discrete cosine transform
    norm = 'ortho'
    Ts.append(lambda x: dct(dct(x, axis=0, norm=norm), axis=1, norm=norm))
    Tis.append(lambda x: idct(idct(x, axis=0, norm=norm), axis=1, norm=norm))
    assert np.allclose(x, Tis[0](Ts[0](x)))

    # Wavelet transform
    level = 3
    _, locs = cdf97_2d_forward(x, level)
    Ts.append(lambda x: cdf97_2d_forward(x, level)[0])
    Tis.append(lambda x: cdf97_2d_inverse(x, locs))

    # Tuning parameter for each transform and case, k -- percent of coeffs
    nc = int(.2*x.size)  # number of coefficients to keep for comparison
    ks = [
        [.1, .9],  # k for bulk_up, whittle_down for DCT
        [.1, .9]]  # k for bulk_up, whittle_down for wavelet

    for T, Ti, k in zip(Ts, Tis, ks):
        # Try to "bulk up" the first k percent of coefficients
        idx1 = bulk_up(x, T, Ti, k[0])
        idx1i = inverse_permutation(idx1)
        match = x[np.unravel_index(idx1, x.shape)].reshape(x.shape)
        coeffs0 = -np.sort(-np.abs(T(x).flatten()))
        coeffs1 = -np.sort(-np.abs(T(match).flatten()))

        # Fix the number coefficients for comparison
        x0 = Ti(threshold(T(x), value=coeffs0[nc], mode='hard'))
        x1 = Ti(threshold(T(match), value=coeffs1[nc], mode='hard'))
        x1 = x1[np.unravel_index(idx1i, x.shape)].reshape(x.shape)

        # Look at the sorted coefficients
        plt.semilogy(coeffs1/coeffs0)
        plt.title('Sorted coefficients, log(T(x)/T(matched))')
        plt.show(block=False)

        # Now try to "whittle down" the last k percent of coefficients
        idx2 = whittle_down(x, T, Ti, k[1])
        idx2i = inverse_permutation(idx2)
        match = x[np.unravel_index(idx2, x.shape)].reshape(x.shape)
        coeffs1 = -np.sort(-np.abs(T(match).flatten()))

        # Generate thresholded image for comparison
        x2 = Ti(threshold(T(match), value=coeffs1[nc], mode='hard'))
        x2 = x2[np.unravel_index(idx2i, x.shape)].reshape(x.shape)

        # Look at the sorted coefficients on the same plot
        plt.semilogy(coeffs1/coeffs0)

        # Print the results for the current transform
        print('Result:')
        print('    Just thresholded:')
        print('         MSE: %g' % compare_mse(x, x0))
        print('        SSIM: %g' % compare_ssim(x, x0))
        print('    Bulk up:')
        print('         MSE: %g' % compare_mse(x, x1))
        print('        SSIM: %g' % compare_ssim(x, x1))
        print('    Whittle down:')
        print('         MSE: %g' % compare_mse(x, x2))
        print('        SSIM: %g' % compare_ssim(x, x2))

        # Hold at the end of transform
        plt.show(block=True)
