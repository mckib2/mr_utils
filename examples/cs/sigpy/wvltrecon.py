'''Try using modified sigpy app to use reordering.'''


import numpy as np
from sigpy.mri import poisson
from sigpy.mri.app import L1WaveletRecon

from mr_utils.test_data.phantom import modified_shepp_logan
from mr_utils.cs import L1WaveletReconWithOrdering
from mr_utils.cs.models import UFT
from mr_utils import view

if __name__ == '__main__':

    N = 128
    im = np.rot90(modified_shepp_logan((N, N, N))[..., int(N/2)])
    im = (im + 1j*im)/2
    # view(im)

    accel = 3
    mask = poisson(im.shape, accel)
    # view(mask)
    uft = UFT(mask)
    y = uft.forward_ortho(im)
    # view(y)
    mps = np.array([np.ones(im.shape)])
    idx = None

    # Try without reordering
    lamda = .01
    app0 = L1WaveletRecon(
        y, mps, lamda, weights=mask, coord=None, wave_name='db4',
        show_pbar=True)

    # Now with ordering!
    lamda = .01
    idx = np.argsort(
        im.real.flatten()) + 1j*np.argsort(im.imag.flatten())
    app1 = L1WaveletReconWithOrdering(
        y, mps, lamda, weights=mask, coord=None, idx=idx,
        show_pbar=True)

    # Run it and look at the results:
    out0 = app0.run()
    out1 = app1.run()
    view(np.stack((
        uft.inverse_ortho(y),
        app0.x,
        app1.x)))
