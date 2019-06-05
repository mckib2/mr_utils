'''Construct composite ellipse using simple approximation.'''

import numpy as np

def simple_composite_ellipse(I, coil_axis=0, pc_axis=1):
    '''Phase of composite ellipse using max intensity coil phase.

    Parameters
    ----------
    I : array_like
        Phase-cycled bSSFP data.
    coil_axis : int, optional
        Dimension holding coil data.
    pc_axis : int, optional
        Dimension holding phase-cycle data.

    Returns
    -------
    array_like
        Phase of the composite ellipse.
    '''

    # Put the coil and pc axes in the places we want them to be:
    # (coil_axis, pc_axis, ...)
    I = np.moveaxis(I, (coil_axis, pc_axis), (0, 1))
    npcs = I.shape[1]
    sh = I.shape[:]

    # We want to do this pixel-wise, so put all pixels in one line
    # as the last dimension
    I = np.reshape(I, I.shape[:2] + (-1,))
    npx = I.shape[2]

    # Get phase substitution using simple method
    phase = np.zeros((npcs, npx))
    for ii in range(npx):
        coil_idxs = np.zeros(npcs, dtype=int)
        for pc in range(npcs):
            midx = np.argmax(np.abs(I[:, pc, ii]))

            # We need to make sure all the phase cycles take
            # from the same coil!
            coil_idxs[pc] = midx
        midx = np.bincount( # pylint: disable=E1101
            coil_idxs).argmax()

        # Steal the phase!
        phase[:, ii] = np.angle(I[midx, :, ii])
    phase = np.reshape(phase, (npcs,) + sh[2:])

    # The average removed the coil dim, but we still need it, so add
    # it back in as the first dimension
    phase = phase[None, ...]

    # Put dimensions back where caller had it
    phase = np.moveaxis(
        phase, (0, 1), (coil_axis, pc_axis))

    # Remove coil axis
    phase = np.moveaxis(phase, coil_axis, 0)
    return phase[0, ...]
