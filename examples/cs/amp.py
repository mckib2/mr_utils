'''Approximate message passing algorithm example.

This is a sanity check example to make sure we can recreate the results from
the reference implementation.  See mr_utils.cs.amp2d for details.
'''

import numpy as np

from mr_utils.cs import amp2d
from mr_utils.cs.models import UFT
from mr_utils.test_data import load_test_data
from mr_utils import view

if __name__ == '__main__':

    # Grab data for the example
    data = load_test_data('mr_utils/test_data/tests/cs/thresholding/amp/',
                          ['x0', 'mask'])
    x, mask = data[0], data[1]
    uft = UFT(mask)

    # Simulate measurement
    y = uft.forward_ortho(x)

    # Reconstruct with AMP
    x_hat = amp2d(
        y,
        forward_fun=uft.forward_ortho,
        inverse_fun=uft.inverse_ortho,
        sigmaType=1,
        randshift=True,
        tol=1e-5,
        x=x,
        ignore_residual=True,
        disp=True,
        maxiter=100)

    view(np.stack((uft.inverse_ortho(y), x_hat)))
