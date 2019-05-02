'''Utils for working with patches as opposed to pixel-wise.'''

import numpy as np
from skimage.util import view_as_windows as vaw

def avg_patch_vals(A, patch_size=(3, 3), pad_mode='edge'):
    '''Get the average value of each patch of A.

    Parameters
    ----------
    A : array_like
        Array to patch-ify.
    patch_size : tuple, optional
        Size of patches.
    pad_mode : str, optional
        Mode to pass to numpy.pad.
    '''

    patches = vaw(A, patch_size)
    pad_width = [int((A.shape[ii] - patches.shape[ii])/2) for
                 ii in range(A.ndim)]
    patches = np.pad(patches, pad_width, pad_mode)
    return np.mean(np.mean(patches, axis=-1), axis=-1)

if __name__ == '__main__':

    N = 10
    A = np.arange(N*N).reshape((N, N))
    # A = np.ones((N, N))

    B = avg_patch_vals(A)
    print(B.shape)
    print(B)
