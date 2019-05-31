'''Show the intersection of coil sensitiviy maps.'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from sigpy.mri import birdcage_maps

if __name__ == '__main__':

    # Make coil maps
    N = 258
    ncoils = 8
    mps = birdcage_maps((ncoils, N, N))

    # Set up LaTeX
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=16)

    x = np.arange(N)
    X, Y = np.meshgrid(x, x)
    amps = np.abs(mps)
    max_amps = np.max(np.abs(mps), axis=0)
    for cc in range(ncoils):
        mask = np.abs(mps[cc, ...]) == max_amps
        mask0 = np.ones(mask.shape)
        mask0[mask == 0] = np.nan
        plt.pcolor(
            X, Y, mask*np.angle(mps[cc, ...])*mask0,
            cmap=cm.afmhot) # pylint: disable=E1101

    # # plt.pcolor(X, Y, max_amps)
    # cbar = plt.colorbar(ticks=[.4, .95])
    # cbar.ax.set_yticklabels(['Low', 'High'])

    plt.title('Coil Sensitiviy Phase Discontinuities')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.tick_params(
        top='off', bottom='off', left='off', right='off',
        labelleft='off', labelbottom='off')

    plt.axis('square')
    plt.show()
