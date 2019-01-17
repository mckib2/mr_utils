import numpy as np
from mr_utils.test_data import SCRReordering
from mr_utils import view
from mr_utils.cs import IHT_FE_TV
from mr_utils.cs.models import UFT

if __name__ == '__main__':

    # CURRENTLY NOT WORKING!

    # We need a mask
    mask = np.fft.fftshift(SCRReordering.mask())

    # Get the encoding model
    uft = UFT(mask)

    # Load in the test data
    kspace = np.fft.fftshift(SCRReordering.Coil1_data())
    imspace = uft.inverse(kspace)
    k = np.sum(np.abs(np.diff(imspace)) > 0) # doesn't look very sparse?

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = uft.inverse(kspace_u)

    x_hat = IHT_FE_TV(kspace_u,mask,k,mu=1,tol=1e-8,do_reordering=False,x=imspace,ignore_residual=True,disp=True,maxiter=10)
    view(x_hat)
