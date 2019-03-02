'''Example of ellipse rotations.'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.sim.ssfp import ssfp
from mr_utils.utils import do_planet_rotation

if __name__ == '__main__':

    # We know SSFP signal will make an ellipse!
    lpcs = 16
    pcs = np.linspace(0, 2*np.pi, lpcs, endpoint=False)
    TR, alpha = 6e-3, np.deg2rad(70)
    T1, T2, df = .6, 1.2, 100

    # Simulate phase cycles
    sigma = .1/2
    I = np.zeros(lpcs, dtype='complex')
    for ii, pc in enumerate(pcs):
        I[ii] = ssfp(T1, T2, TR, alpha, df, pc, M0=1) \
            + np.random.normal(0, sigma) + 1j*np.random.normal(0, sigma)

    # Now find the correct rotation
    xr, yr, cr, phi = do_planet_rotation(I)

    plt.plot(I.real, I.imag, '.-')
    plt.plot(xr, yr, '.--')
    plt.show()
