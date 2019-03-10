'''Use iterative hard thresholding to recover cardiac image.

This doesn't work very well because we're not truly sparse.
'''

import numpy as np

from mr_utils.test_data import load_test_data
from mr_utils import view
from mr_utils.cs import IHT_FE_TV
from mr_utils.cs.models import UFT

if __name__ == '__main__':

    # CURRENTLY NOT WORKING!

    # We need a mask
    mask = load_test_data('mr_utils/test_data/tests/recon/reordering',
                          ['mask'])[0]
    mask = np.fft.fftshift(mask)

    # Get the encoding model
    uft = UFT(mask)

    # Load in the test data
    kspace = load_test_data('mr_utils/test_data/tests/recon/reordering',
                            ['coil1'])[0]
    kspace = np.fft.fftshift(kspace)
    imspace = uft.inverse(kspace)
    k = np.sum(np.abs(np.diff(imspace)) > 0) # doesn't look very sparse?

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = uft.inverse(kspace_u)

    x_hat = IHT_FE_TV(kspace_u, mask, k, mu=1, tol=1e-8, do_reordering=False,
                      x=imspace, ignore_residual=True, disp=True, maxiter=10)
    view(x_hat)
