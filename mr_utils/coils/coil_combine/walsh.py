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

def walsh(img, noise_ims=None, coil_axis=0):
    '''Stochastic matched filter coil combine.

    Parameters
    ----------
    img : array_like
        Coil images to estimate coil sensitivities.
    noise_ims : array_like, optional
        Noise acquisitons (same size as img).
    coil_axis : int, optional
        Dimension that has coils.

    Notes
    -----
    '''

    if (noise_ims is None) or (
            np.allclose(noise_ims, np.zeros_like(noise_ims))):
        noise_ims = np.zeros(img.shape)
        no_noise = True
    else:
        no_noise = False

    # Move coil axis to be first
    if coil_axis != 0:
        img = np.moveaxis(img, coil_axis, 0)

    # Get some sizes
    ncoils, ny, nx = img.shape[:]

    # Compute the sample autocovariances pointwise, will be Hermitian
    # symmetric, only need lower triangular matrix
    Rs = np.zeros((ncoils, ncoils, ny, nx), dtype=img.dtype)
    Rn = np.zeros((ncoils, ncoils, ny, nx), dtype=noise_ims.dtype)
    for p in range(ncoils):
        # # Autocorrelation has 1s along diagonal:
        Rn[p, p, ...] = 1
        Rs[p, p, ...] = 1
        for q in range(p):
            # Fill in Rn
            val = noise_ims[p, ...]*np.conj(noise_ims[q, ...])
            Rn[p, q, ...] = val
            Rn[q, p, ...] = val.conj()

            # Fill in Rs
            val = img[p, ...]*np.conj(img[q, ...])
            Rs[p, q, ...] = val
            Rs[q, p, ...] = val.conj()

    # Get most significant eigenvector for each pixel
    csm = np.zeros(img.shape, dtype=img.dtype)
    for idx in np.ndindex((nx, ny)):
        xx, yy = idx[:]

        # If no noise, assume identity
        if no_noise:
            Rni = np.eye(ncoils)
        else:
            Rni = np.linalg.inv(Rn[..., yy, xx])

        # Construct P and find most significant eigenvector
        P = np.dot(Rni, Rs[..., yy, xx])

        # # To be really accurate:
        # w, v = np.linalg.eig(P)
        # idx = np.argmax(np.abs(w))
        # v = v[:, idx][:, None]

        # P is approximately Hermitian, so we can do this:
        _w, v = eigh(P, lower=False, eigvals=(ncoils-1, ncoils-1))

        # Normalize to get approximately uniform noise variance
        alpha = np.sqrt((v.T.conj().dot(Rni).dot(v))[0, 0])
        v /= alpha
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

    # Apply phase correction
    if avg_method == 'pc':
        pcs = np.linspace(0, 2*np.pi, npcs, endpoint=False)
        comp = np.exp(-1j*pcs/2)
        img = img*np.tile(
            comp[None, None, None, :], (ncoils, ny, nx, 1))

    # Compute the sample autocovariance for each phase-cycle
    Rs = np.zeros((ncoils, ncoils, ny, nx, npcs), dtype=img.dtype)
    for ii in range(npcs):
        for p in range(ncoils):
            Rs[p, p, ...] = 1
            for q in range(p):
                # Autocorrelation
                Rs[p, q, ..., ii] = img[
                    p, ..., ii]*np.conj(img[q, ..., ii])

    # Combine the autocorrelation matrices
    if avg_method == 'cov':
        Rs = np.mean(Rs, axis=-1)
    elif avg_method == 'pc':
        Rs = np.mean(Rs, axis=-1)
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
