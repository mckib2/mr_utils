'''Get coil combine functions and labels.'''

import numpy as np
from ismrmrdtools.coils import (
    calculate_csm_walsh as walsh, calculate_csm_inati_iter as inati)

from mr_utils.coils.coil_combine import coil_pca

from bart import bart

def get_coil_combine_funs(N, v='-v0'):
    '''Return list of functions that perform coil combination.'''

    fft = lambda x0, ax=(1, 2): np.fft.fftshift(np.fft.fft2(
        np.fft.fftshift(x0, axes=ax), axes=ax), axes=ax)
    ifft = lambda x0, ax=(1, 2): np.fft.fftshift(np.fft.ifft2(
        np.fft.fftshift(x0, axes=ax), axes=ax), axes=ax)

    return ([
        # Walsh
        lambda x0: np.sum(walsh(x0)[0].conj()*x0, axis=0),

        # Inati
        lambda x0: inati(x0)[1],

        # PCA (imspace)
        lambda x0: coil_pca(
            x0, coil_dim=0, n_components=1),

        # PCA (kspace)
        lambda x0: ifft(coil_pca(fft(
            x0, ax=(1, 2)), coil_dim=0, n_components=1), ax=(1, 2)),

        # Direct method
        lambda x0: np.sum(
            np.moveaxis(bart(1, 'caldir %d' % int(N/2), fft(
                np.moveaxis(x0, 0, -1)[:, :, None, :],
                ax=(0, 1))).squeeze(), -1, 0).conj()*x0, axis=0),

        # Geometric
        lambda x0: ifft(bart(1, 'cc -p 1 -A -G', fft(
            np.moveaxis(x0, 0, -1)[:, :, None, :],
            ax=(0, 1))), ax=(0, 1)).squeeze(),

        # # ESPIRiT -- using cc, don't use this one!
        # lambda x0: ifft(bart(1, 'cc -p 1 -A -E', fft(
        #     x0.T[:, :, None, :], ax=(0, 1))), ax=(0, 1)).squeeze()

        # ESPIRiT -- using ecalib, use this one!
        # use -v for numerical phantom
        lambda x0: np.sum(
            np.moveaxis(bart(1, 'ecalib -a -m1 -P -S %s' % v, fft(
                np.moveaxis(x0, 0, -1)[:, :, None, :],
                ax=(0, 1))).squeeze(), -1, 0).conj()*x0, axis=0),

        # SVD -- suprisingly good!
        lambda x0: ifft(bart(1, 'cc -p 1 -A -S', fft(
            np.moveaxis(x0, 0, -1)[:, :, None, :],
            ax=(0, 1))), ax=(0, 1)).squeeze()
    ], [
        'Walsh',
        'Inati',
        'PCA (image space)',
        'PCA (k-space)',
        'Direct',
        'Geometric',
        'ESPIRiT',
        'SVD'
    ])
