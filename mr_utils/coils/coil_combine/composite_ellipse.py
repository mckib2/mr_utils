'''Construct a composite ellipse from multiple coil ellipses.'''

import numpy as np
from tqdm import trange

def composite_ellipse(C, coil_axis=-1, disp=False):
    '''Make compositie ellipse.

    Parameters
    ----------
    C : array_like
        Coil ellipses.
    coil_axis : int, optional
        Dimension that holds coils.
    disp : bool, optional
        Display ellipse plot.

    Returns
    -------
    C0 : array_like
        Composite ellipse phase-cycle points.

    Notes
    -----
    The rotation of the ellipse includes both df and phi_rf effects.
    df rotates the ellipse and drives the points around the ellipse,
    but phi_rf only rotates the ellipse, so at a single spatial
    location differences between coil rotations can be explained by
    just phi_rf.  The absolute df can be found using the PLANET
    method [1]_.  However, this requires 5 or more phase-cycles, which
    we do not have.  Then we have ncoils+1 unknowns (phi_rf_i + df)
    and only ncoils equations (phi_i = 2pi(df)TE + phi_rf_i), so the
    actual rotation cannot be determined, so we have no preference.
    '''

    # Get dims and move coil_axis to axis 0
    C = C.copy()
    ncoils = C.shape[coil_axis]
    C = np.moveaxis(C, coil_axis, 0)

    # Find the best coil to use
    ref_coil = np.argmax(np.max(np.abs(C), axis=1))

    # Construct composite coil
    C0 = np.zeros(C.shape, dtype=C.dtype)
    ts = np.zeros(ncoils, dtype='complex')
    Cref = C[ref_coil, :]

    ts = C/Cref
    ts = np.mean(ts, axis=1)
    C0 = C/ts[:, None]

    # # Find rotation/scaling between reference and target coil
    # # ellipses
    # ts = np.linalg.lstsq(
    #     C.T, Cref[:, None], rcond=None)[0].squeeze().conj()
    # C0 = C/ts[:, None]
    # print(ref_coil, ts)
    # C0[ref_coil, :] = C[ref_coil, :]

    if disp:
        import matplotlib.pyplot as plt
        for cc in trange(ncoils, leave=False):
            plt.plot(C0[cc, :].real, C0[cc, :].imag, label='C%d' % cc)

    # Synthesize single ellipse
    w = 1/np.abs(ts)
    w /= np.sum(w)
    C0 = np.dot(w[None, :], C0).squeeze()
    # C0 = np.mean(C0, axis=0)

    if disp:
        plt.plot(C0.real, C0.imag, '--', label='Composite')
        plt.legend()
        plt.show()

    return C0
