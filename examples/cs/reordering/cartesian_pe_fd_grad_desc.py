import numpy as np
from mr_utils import view
from mr_utils.cs import GD_FE_TV
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.sim.traj import cartesian_pe

if __name__ == '__main__':

    # Same binary smiley face example
    do_reordering = True
    N = 1000
    m = binary_smiley(N)
    k = np.sum(np.abs(np.diff(m)) > 0)
    np.random.seed(5)
    samp = cartesian_pe(m.shape,undersample=.2,reflines=5)

    # Make the complex measurement in kspace
    y = np.fft.fftshift(np.fft.fft2(m))*samp

    # Solve inverse problem using gradient descent with TV sparsity constraint
    m_hat = GD_FE_TV(kspace=y,samp=samp,alpha=.5,lam=.022,do_reordering=do_reordering,im_true=m,ignore_residual=True,disp=True,maxiter=50)

    # Look at before/after shots
    view(np.stack((np.fft.ifft2(y),m_hat)))
