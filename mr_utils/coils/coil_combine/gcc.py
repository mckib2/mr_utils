'''Call BART's GCC.'''

import numpy as np
from bart import bart

def gcc(x0, vcoils=1, coil_axis=-1):
    '''Python interface for Geometric coil compression.

    Parameters
    ----------
    x0 : array_like
        Image space data.
    vcoils : int, optional
        Number of virtual coils.
    coil_axis : int, optional
        Coil dimension.

    Notes
    -----
    For 2D images only.
    '''

    fft = lambda x0, ax=(1, 2): np.fft.fftshift(np.fft.fft2(
        np.fft.fftshift(x0, axes=ax), axes=ax), axes=ax)
    ifft = lambda x0, ax=(1, 2): np.fft.fftshift(np.fft.ifft2(
        np.fft.fftshift(x0, axes=ax), axes=ax), axes=ax)

    val = ifft(bart(1, 'cc -p %d -A -G' % vcoils, fft(
        np.moveaxis(x0, coil_axis, -1)[:, :, None, :],
        ax=(0, 1))), ax=(0, 1))
    return np.moveaxis(val, -1, coil_axis).squeeze()
