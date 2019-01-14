import numpy as np
from mr_utils import view
from mr_utils.cs import GD_TV
from mr_utils.cs.models import UFT
from mr_utils.test_data.phantom import binary_smiley
from mr_utils.sim.traj import cartesian_pe

if __name__ == '__main__':

    # Same binary smiley face example
    do_reordering = True
    N = 1000
    x = binary_smiley(N)
    k = np.sum(np.abs(np.diff(x)) > 0)
    np.random.seed(5)
    samp = cartesian_pe(x.shape,undersample=.2,reflines=5)
    uft = UFT(samp)

    # Make the complex measurement in kspace
    # Note this is different than uft.forward, as fftshift must be performed
    y = np.fft.fftshift(np.fft.fft2(x))*samp

    # Solve inverse problem using gradient descent with TV sparsity constraint
    x_hat = GD_TV(y,forward_fun=uft.forward,inverse_fun=uft.inverse,alpha=.5,lam=.022,do_reordering=do_reordering,x=x,ignore_residual=True,disp=True,maxiter=50)

    # Look at the before/after shots
    view(np.stack((uft.inverse(y),x_hat)))
