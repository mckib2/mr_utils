'''Example demonstrating the differences between thresholding methods.

We can:
    Threshold the complex signal
    Threshold the real/imag parts separately.
'''

import numpy as np
from skimage.measure import compare_mse, compare_ssim

from mr_utils.test_data.phantom import binary_smiley
from mr_utils.utils.wavelet import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.cs import proximal_GD
from mr_utils import view

if __name__ == '__main__':

    # Get a phantom
    N = 64
    x = binary_smiley(N)

    # Do some sampling
    num_spokes = 12
    mask = radial(x.shape, num_spokes)
    uft = UFT(mask)
    y = uft.forward_ortho(x)

    # Sparsifying transforms
    level = 3
    wvlt, locations = cdf97_2d_forward(x, level)
    sparsify = lambda x0: cdf97_2d_forward(x0, level)[0]
    unsparsify = lambda x0: cdf97_2d_inverse(x0, locations)

    # Do the recon
    alpha = .15
    disp = True
    ignore = False
    maxiter = 200
    x_c = proximal_GD(y, forward_fun=uft.forward_ortho,
                      inverse_fun=uft.inverse_ortho, sparsify=sparsify,
                      unsparsify=unsparsify, reorder_fun=None,
                      alpha=alpha, thresh_sep=False, selective=None, x=x,
                      ignore_residual=ignore, disp=disp, maxiter=maxiter)

    x_ri = proximal_GD(y, forward_fun=uft.forward_ortho,
                       inverse_fun=uft.inverse_ortho, sparsify=sparsify,
                       unsparsify=unsparsify, reorder_fun=None,
                       alpha=alpha, thresh_sep=True, selective=None, x=x,
                       ignore_residual=ignore, disp=disp, maxiter=maxiter)

    xabs = np.abs(x)
    x_cabs = np.abs(x_c)
    x_riabs = np.abs(x_ri)
    print('Thresholding complex:')
    print('     MSE: %g' % compare_mse(xabs, x_cabs))
    print('    SSIM: %g' % compare_ssim(xabs, x_cabs))
    print('Thresholding real/imag separately:')
    print('     MSE: %g' % compare_mse(xabs, x_riabs))
    print('    SSIM: %g' % compare_ssim(xabs, x_riabs))
    view(np.stack((x, uft.inverse_ortho(y), x_c, x_ri)))
