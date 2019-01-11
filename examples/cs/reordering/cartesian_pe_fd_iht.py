import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse
from mr_utils.cs import IHT_FE_TV
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.sim.traj import cartesian_pe

if __name__ == '__main__':

    do_reordering = True
    N = 1000
    x = binary_smiley(N)
    k = np.sum(np.abs(np.diff(x)) > 0)
    np.random.seed(5)
    samp = cartesian_pe(x.shape,undersample=.2,reflines=5)

    # Show sampling pattern
    plt.imshow(samp,cmap='gray')
    plt.title('Sampling Pattern')
    plt.show()

    # Simulate acquisiton
    kspace = np.fft.fftshift(np.fft.fft2(x))
    kspace_u = kspace*samp
    imspace_u = np.fft.ifft2(kspace_u)

    # Look at the aliased acquired signal
    plt.imshow(np.abs(imspace_u),cmap='gray')
    plt.title('Acquired')
    plt.show()

    # Do IHT, enforcing sparsity in finite differences domain
    x_hat = IHT_FE_TV(kspace_u,samp,k,mu=1,tol=1e-8,do_reordering=do_reordering,x=x,ignore_residual=False,disp=True,maxiter=500)

    # Check it out
    plt.imshow(x_hat,cmap='gray')
    plt.title('IHT Recon, MSE: %g' % compare_mse(x_hat,x))
    plt.show()
