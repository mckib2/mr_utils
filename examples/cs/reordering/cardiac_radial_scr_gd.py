'''Spatially total variation constrained cardiac reconstruction.

Using Ganesh's cardiac example, reconstruct comparing using reordered and not.

This replicates figures in paper:
    G.Adluru, E.V.R. DiBella. "Reordering for improved constrained
    reconstruction from undersampled k-space data". International Journal of
    Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008.
    doi:10.1155/2008/341684.

We assume we know the exact reordering to begin with (this is a ridiculous
assumption, by the way).  Also, it seems to be weird data (look at log of
kspace data, strange).  That along with the fact that recon fails when
orthonormal fourier encoding is used (uft.forward_ortho), it makes me think
that this is strange data and we should be using another example data set.
'''

import numpy as np

from mr_utils.test_data import SCRReordering
from mr_utils import view
from mr_utils.cs import GD_TV
from mr_utils.cs.models import UFT

if __name__ == '__main__':

    # We need a mask
    mask = np.fft.fftshift(SCRReordering.mask())

    # Get the encoding model
    uft = UFT(mask)

    # Load in the test data
    kspace = np.fft.fftshift(SCRReordering.Coil1_data())
    imspace = uft.inverse(kspace)

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = uft.inverse(kspace_u)

    # Do reconstruction using gradient descent without reordering
    do_reordering = False
    x_hat_wo = GD_TV(
        kspace_u,
        forward_fun=uft.forward,
        inverse_fun=uft.inverse,
        alpha=.5,
        lam=.004,
        do_reordering=do_reordering,
        x=imspace,
        ignore_residual=True,
        disp=True,
        maxiter=50)

    # Do reconstruction using gradient descent with reordering
    do_reordering = True
    x_hat_w = GD_TV(
        kspace_u,
        forward_fun=uft.forward,
        inverse_fun=uft.inverse,
        alpha=.5,
        lam=.004,
        do_reordering=do_reordering,
        x=imspace,
        ignore_residual=True,
        disp=True,
        maxiter=50)

    # Checkout how well we did
    view(np.hstack((imspace, imspace_u, x_hat_wo, x_hat_w)))
