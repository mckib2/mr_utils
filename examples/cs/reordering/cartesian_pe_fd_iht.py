import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse
from mr_utils.cs import IHT_TV
from mr_utils.cs.models import UFT
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.sim.traj import cartesian_pe

if __name__ == '__main__':

    do_reordering = True
    N = 1000
    x = binary_smiley(N)
    k = np.sum(np.abs(np.diff(x)) > 0)
    np.random.seed(5)
    samp = cartesian_pe(x.shape,undersample=.01,reflines=5)
    uft = UFT(samp) # acquisiton model

    # Show sampling pattern
    plt.imshow(samp,cmap='gray')
    plt.title('Sampling Pattern')
    plt.show()

    # Simulate acquisiton
    kspace_u = uft.forward_s(x)
    imspace_u = uft.inverse(kspace_u)

    # Look at the aliased acquired signal
    plt.imshow(np.abs(imspace_u),cmap='gray')
    plt.title('Acquired')
    plt.show()

    # Do IHT, enforcing sparsity in finite differences domain
    x_hat = IHT_TV(kspace_u,forward_fun=uft.forward_s,inverse_fun=lambda x: np.abs(uft.inverse(x)),k=k,mu=1,tol=1e-8,do_reordering=do_reordering,x=x,ignore_residual=False,disp=True,maxiter=500)

    # Check it out
    plt.imshow(x_hat,cmap='gray')
    plt.title('IHT Recon, MSE: %g' % compare_mse(x_hat,x))
    plt.show()
