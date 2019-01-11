import numpy as np
from mr_utils.test_data import SCRReordering
from mr_utils import view
from mr_utils.cs import GD_FE_TV

if __name__ == '__main__':

    # Load in the test data
    kspace = np.fft.fftshift(SCRReordering.Coil1_data())
    imspace = np.fft.ifft2(kspace)

    # We need a mask
    mask = np.fft.fftshift(SCRReordering.mask())

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = np.fft.ifft2(kspace_u)

    # Do reconstruction using gradient descent
    x_hat = GD_FE_TV(kspace_u,mask,alpha=.5,lam=.015,im_true=imspace,ignore_residual=False,disp=True,maxiter=200)

    # Checkout how well we did
    view(np.vstack((imspace,x_hat)))
