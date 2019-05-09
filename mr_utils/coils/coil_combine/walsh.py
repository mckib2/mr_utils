'''Walsh coil combine.

Notes
-----
Adapted from [1]_.  Based on the paper [2]_.

References
----------
.. [1] https://github.com/ismrmrd/ismrmrd-python-tools/
       blob/master/ismrmrdtools/coils.py

.. [2] Walsh, David O., Arthur F. Gmitro, and Michael W. Marcellin.
       "Adaptive reconstruction of phased array MR imagery." Magnetic
       Resonance in Medicine: An Official Journal of the
       International Society for Magnetic Resonance in Medicine 43.5
       (2000): 682-690.
'''

import numpy as np
from scipy.linalg import eigh

def walsh(img, coil_axis=0):
    '''Stochastic matched filter coil combine.

    Parameters
    ----------
    img : array_like
        Coil images to estimate coil sensitivities.
    coil_axis : int, optional
        Dimension that has coils.

    Notes
    -----
    In this implementation, Rn (noise correlation matrix) is assumed
    to be the identity matrix.
    '''

    # Move coil axis to be first
    if coil_axis != 0:
        img = np.moveaxis(img, coil_axis, 0)

    # Get some sizes
    ncoils, ny, nx = img.shape[:]

    # Compute the sample covariance pointwise, will be Hermitian
    # symmetric, only need lower triangular matrix
    Rs = np.zeros((ncoils, ncoils, ny, nx), dtype=img.dtype)
    for p in range(ncoils):
        for q in range(p):
            Rs[p, q, ...] = img[p, ...]*np.conj(img[q, ...])

    # Get most significant eigenvector for each pixel
    csm = np.zeros(img.shape, dtype=img.dtype)
    for idx in np.ndindex((nx, ny)):
        xx, yy = idx[:]
        _w, v = eigh(
            Rs[..., yy, xx], lower=True, eigvals=(ncoils-1, ncoils-1))
        v /= np.linalg.norm(v) # assuming Rn = I
        csm[:, yy, xx] = v.squeeze()

    # Move the coil axis to correct place
    if coil_axis != 0:
        csm = np.moveaxis(csm, 0, coil_axis)

    return csm

def walsh_gs(img, coil_axis=0, pc_axis=-1, avg_method='z'):
    '''Walsh tailored for bSSFP GS recon.'''

    # Move coil axis to be first
    if coil_axis != 0:
        img = np.moveaxis(img, coil_axis, 0)

    # Move phase-cycle axis to be last
    img = np.moveaxis(img, pc_axis, -1)

    # Get some sizes
    ncoils, ny, nx, npcs = img.shape[:]

    # Compute the sample covariance for each phase-cycle
    Rs = np.zeros((ncoils, ncoils, ny, nx, npcs), dtype=img.dtype)
    for ii in range(npcs):
        for p in range(ncoils):
            for q in range(p):
                Rs[p, q, ..., ii] = img[
                    p, ..., ii]*np.conj(img[q, ..., ii])

    # Combine the correlation matrices
    if avg_method == 'corr':
        Rs = np.mean(Rs, axis=-1)
    elif avg_method == 'z':
        Rs = np.tanh(np.mean(np.arctanh(Rs), axis=-1))
    else:
        raise NotImplementedError()

    # Get most significant eigenvector for each pixel
    csm = np.zeros(img.shape[:-1], dtype=img.dtype)
    for idx in np.ndindex((nx, ny)):
        xx, yy = idx[:]
        _w, v = eigh(
            Rs[..., yy, xx], lower=True, eigvals=(ncoils-1, ncoils-1))
        v /= np.linalg.norm(v) # assuming Rn = I
        csm[:, yy, xx] = v.squeeze()

    # Move the coil axis to correct place
    if coil_axis != 0:
        csm = np.moveaxis(csm, 0, coil_axis)

    return csm
