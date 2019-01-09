import numpy as np
from mr_utils.recon.reordering import scr_reordering_adluru
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

if __name__ == '__main__':

    from mr_utils.test_data.phantom import binary_smiley
    from mr_utils.sim.traj import cartesian_pe

    N = 100
    reorder = True
    m = binary_smiley(N)
    k = np.sum(np.abs(np.diff(m)) > 0)
    np.random.seed(0)
    samp = cartesian_pe(m.shape,undersample=.2,reflines=5)

    # Take samples
    y = np.fft.fftshift(np.fft.fft2(m))*samp

    # Do convex recon
    m_hat = scr_reordering_adluru(y,samp,prior=m,alpha0=1,alpha1=.001,beta2=np.finfo(float).eps,reorder=reorder,reorder_every_iter=False,enforce_consistency=True,niters=1000)

    # Look at result
    plt.imshow(np.abs(m_hat),cmap='gray')
    plt.title('GD Recon, MSE: %e' % compare_mse(np.abs(m_hat),m))
    plt.show()
