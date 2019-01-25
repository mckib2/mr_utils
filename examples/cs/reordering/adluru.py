'''Reconstruct binary smiley using ported Adluru code.

Use Cartesian undersampling pattern (undersample in phase-encode dimension).
I'm not in love in with the port I did of Ganesh's code, I would use the other
convex TV implementation I did (mr_utils.cs.GD_TV) or proximal gradient
descent (mr_utils.cs.proximal_GD).  I could only get this to work if I enforce
data consistency every iteration, which makes me suspect something is wrong
with the implementation...
'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

from mr_utils.recon.reordering import scr_reordering_adluru
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.sim.traj import cartesian_pe

if __name__ == '__main__':

    N = 100
    reorder = True
    m = binary_smiley(N)
    k = np.sum(np.abs(np.diff(m)) > 0)
    np.random.seed(0)
    samp = cartesian_pe(m.shape, undersample=.2, reflines=5)

    # Take samples
    y = np.fft.fftshift(np.fft.fft2(m))*samp

    # Do convex recon
    m_hat = scr_reordering_adluru(
        y,
        samp,
        prior=m,
        alpha0=1,
        alpha1=.001,
        beta2=np.finfo(float).eps,
        reorder=reorder,
        reorder_every_iter=False,
        enforce_consistency=True,
        niters=1000)

    # Look at result
    plt.imshow(np.abs(m_hat), cmap='gray')
    plt.title('GD Recon, MSE: %e' % compare_mse(np.abs(m_hat), m))
    plt.show()
