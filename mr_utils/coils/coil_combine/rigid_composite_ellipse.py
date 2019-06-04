'''Rigid transformation to find composite ellipses.'''

import numpy as np

def rigid_composite_ellipse(
        I, coil_axis=0, pc_axis=1, sigma2=1, ret_ellipse=False):
    '''Phase of composite ellipse using rigid transformation.

    Parameters
    ----------
    I : array_like
        Phase-cycled bSSFP data.
    coil_axis : int, optional
        Dimension holding coil data.
    pc_axis : int, optional
        Dimension holding phase-cycle data.
    sigma2 : array_like, optional
        Noise variances for each coil.
    ret_ellipse : bool, optional
        Return complex ellipse points.

    Returns
    -------
    array_like
        Phase of the composite ellipse.
    composite_ellipse : array_like, optional
        The actual complex composite ellipse if ret_ellipse=True.

    Notes
    -----
    This is the rigid version, no shift is taken into account as in
    affine transformations, only scaling and rotation.
    '''

    # Put the coil and pc axes in the places we want them to be:
    # (coil_axis, pc_axis, ...)
    I = np.moveaxis(I, (coil_axis, pc_axis), (0, 1))
    ncoils = I.shape[0]
    npcs = I.shape[1]
    sh = I.shape[:]

    # We want to do this pixel-wise, so put all pixels in one line
    # as the last dimension
    I = np.reshape(I, I.shape[:2] + (-1,))
    npx = I.shape[2]

    # Find rigid transformation to arbitrary location at every pixel
    composite_ellipse = np.zeros((npcs, npx), dtype='complex')
    T = np.zeros((ncoils, npx), dtype='complex')
    R = np.zeros((ncoils, npcs, npx), dtype='complex')
    for cc in range(ncoils):
        I0 = I[cc, :, ...]
        T0 = np.linalg.lstsq(
            I0, np.ones(npcs), rcond=None)[0][0]
        T[cc] = T0
        R[cc, ...] = I0*T0

    # Construct composite ellipse for this pixel
    weights = np.abs(1/T)**2
    weights *= sigma2
    weights /= np.sum(weights)
    # Do the weighted average:
    composite_ellipse = np.multiply(
        R, weights[:, None, :]).sum(axis=0)

    # The average removed the coil dim, but we still need it, so add
    # it back in as the first dimension
    composite_ellipse = composite_ellipse[None, ...]

    # Now put the pixels back into the correct shape
    composite_ellipse = np.reshape(
        composite_ellipse, (1, npcs) + sh[2:])

    # Put dimensions back where caller had it
    composite_ellipse = np.moveaxis(
        composite_ellipse, (0, 1), (coil_axis, pc_axis))

    # Remove coil axis
    composite_ellipse = np.moveaxis(composite_ellipse, coil_axis, 0)
    composite_ellipse = composite_ellipse[0, ...]

    if ret_ellipse:
        return composite_ellipse
    return np.angle(composite_ellipse)
