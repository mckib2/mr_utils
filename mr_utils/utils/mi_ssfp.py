'''Simple maximum intensity recon for banding minimization.'''

import numpy as np

def mi_ssfp(images, pc_axis=0):
    '''Compute maximum intensity SSFP.

    Parameters
    ==========
    images : array_like
        Array of phase-cycled images.
    pc_axis : int, optional
        Which dimension is the phase-cycle dimension.

    Returns
    =======
    array_like
        MI image.

    Notes
    =====
    Implements Equation [5] from [1]_.

    References
    ==========
    .. [1] Bangerter, Neal K., et al. "Analysis of multiple‐acquisition SSFP."
           Magnetic Resonance in Medicine: An Official Journal of the
           International Society for Magnetic Resonance in Medicine 51.5
           (2004): 1038-1047.
    '''

    return np.max(np.abs(images), axis=pc_axis)
