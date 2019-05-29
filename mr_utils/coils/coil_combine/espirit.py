'''Python interface for BART's ESPIRiT.'''

import numpy as np
from bart import bart

def espirit(x0, v='', coil_axis=0):
    '''ESPIRiT coil combine.
    '''

    fft = lambda x0, ax=(1, 2): np.fft.fftshift(np.fft.fft2(
        np.fft.fftshift(x0, axes=ax), axes=ax), axes=ax)

    return np.sum(
        np.moveaxis(bart(1, 'ecalib -a -m1 -P -S %s' % v, fft(
            np.moveaxis(x0, coil_axis, -1)[:, :, None, :],
            ax=(0, 1))).squeeze(), -1, 0).conj()*x0, axis=0)
