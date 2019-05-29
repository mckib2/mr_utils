'''Python interface for BART's direct coil compression.'''

import numpy as np
from bart import bart

def caldir(x0, coil_axis=-1):
    '''Directly calibrated coil combination.

    Parameters
    ----------
    x0 : array_like
        Image space data.
    coil_axis : int, optional
        Coil dimension.

    Notes
    -----
    Currently only for 2D images.
    '''

    fft = lambda x0, ax=(1, 2): np.fft.fftshift(np.fft.fft2(
        np.fft.fftshift(x0, axes=ax), axes=ax), axes=ax)

    sh = np.delete(x0.shape[:], coil_axis)
    N = np.min(sh)
    return np.sum(
        np.moveaxis(bart(1, 'caldir %d' % int(N/2), fft(
            np.moveaxis(x0, coil_axis, -1)[:, :, None, :],
            ax=(0, 1))).squeeze(), -1, coil_axis).conj()*x0,
        axis=coil_axis)
