'''Compare axial brain recons (radial sampling).
'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse, compare_ssim

from mr_utils.test_data import load_test_data
from mr_utils.sim.traj import radial
from mr_utils.cs.models import UFT
from mr_utils.cs import proximal_GD
from mr_utils.utils.wavelet import cdf97_2d_forward, cdf97_2d_inverse
from mr_utils.utils.sort2d import sort2d

if __name__ == '__main__':

    # Load in brain
    path = 'mr_utils/test_data/examples/cs/reordering/paper/figures/'
    im = load_test_data(path, ['ssfp_brain'])[0]
    im /= np.max(np.abs(im.flatten()))*.1

    plt.subplot(1, 3, 1)
    plt.hist(im.real.flatten(), density=True)
    plt.title('Distribution of Real')
    plt.xlabel('Variance: %g' % np.var(im.real.flatten()))

    plt.subplot(1, 3, 2)
    plt.hist(im.imag.flatten(), density=True)
    plt.title('Distribution of Imag')
    plt.xlabel('Variance: %g' % np.var(im.imag.flatten()))

    plt.subplot(1, 3, 3)
    plt.hist(np.abs(im.flatten()), density=True)
    plt.title('Distribution of Mag')
    plt.xlabel('Variance: %g' % np.var(np.abs(im).flatten()))

    plt.show()

    # Radial sampling pattern for retrospective undersampling
    num_spokes = 16
    samp = radial(im.shape, num_spokes, skinny=True, extend=True)
    samp_percent = np.sum(samp.flatten())/samp.size*100
    uft = UFT(samp)
    kspace_u = np.fft.fft2(im)*samp
    imspace_u = np.fft.ifft2(kspace_u)
    # view(samp)
    # view(imspace_u)
    # view(kspace_u)

    # Use wavelet transform
    lvl = 3
    _coeffs, locs = cdf97_2d_forward(im, lvl)
    sparsify = lambda x0: cdf97_2d_forward(x0, lvl)[0]
    unsparsify = lambda x0: cdf97_2d_inverse(x0, locs)
    assert np.allclose(unsparsify(sparsify(im)), im)

    # Recon params
    ignore_mse = False
    ignore_ssim = True
    ignore_residual = True
    thresh_sep = False
    maxiter = 1000
    disp = True
    strikes = 10

    # Do recon no ordering
    recon = proximal_GD(
        kspace_u.copy(),
        forward_fun=lambda x0: np.fft.fft2(x0)*samp,#uft.forward,
        inverse_fun=lambda x0: np.fft.ifft2(x0),#uft.inverse,
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=None,
        alpha=.05,
        thresh_sep=thresh_sep,
        x=im,
        ignore_residual=ignore_residual,
        ignore_mse=ignore_mse,
        ignore_ssim=ignore_ssim,
        disp=disp,
        maxiter=maxiter,
        strikes=strikes)

    # Do recon doing 2d monotonic sort
    idx_mono = sort2d(recon.real)[1] + 1j*(sort2d(recon.imag)[1])
    # from mr_utils.utils import avg_patch_vals as avp
    # idx_mono_r = sort2d(avp(recon.real))[1]
    # idx_mono_i = sort2d(avp(recon.imag))[1]
    # idx_mono = idx_mono_r + 1j*idx_mono_i
    recon_mono = proximal_GD(
        kspace_u.copy(),
        forward_fun=lambda x0: np.fft.fft2(x0)*samp,#uft.forward,
        inverse_fun=lambda x0: np.fft.ifft2(x0),#uft.inverse,
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=lambda x0: idx_mono,
        alpha=.03,
        thresh_sep=thresh_sep,
        x=im,
        ignore_residual=ignore_residual,
        ignore_mse=ignore_mse,
        ignore_ssim=ignore_ssim,
        disp=disp,
        maxiter=35,#maxiter,
        strikes=strikes)

    idx_mono_true = sort2d(im.real)[1] + 1j*(sort2d(im.imag)[1])
    recon_mono_true = proximal_GD(
        kspace_u.copy(),
        forward_fun=lambda x0: np.fft.fft2(x0)*samp,
        inverse_fun=lambda x0: np.fft.ifft2(x0),
        sparsify=sparsify,
        unsparsify=unsparsify,
        reorder_fun=lambda x0: idx_mono_true,
        alpha=.03,
        thresh_sep=thresh_sep,
        x=im,
        ignore_residual=ignore_residual,
        ignore_mse=ignore_mse,
        ignore_ssim=ignore_ssim,
        disp=disp,
        maxiter=maxiter,
        strikes=strikes)

    sh = (3, 3)

    plt.subplot(*sh, 1)
    plt.imshow(np.abs(im))
    plt.title('Reference')

    plt.subplot(*sh, 2)
    plt.imshow(samp)
    plt.title('Sampling Mask (%%%d)' % samp_percent)

    plt.subplot(*sh, 3)
    plt.imshow(np.abs(imspace_u))
    plt.title('Zero-pad')
    plt.xlabel('MSE: %g, SSIM: %g' % (
        compare_mse(np.abs(im), np.abs(imspace_u)),
        compare_ssim(np.abs(im), np.abs(imspace_u))))

    plt.subplot(*sh, 4)
    plt.imshow(np.abs(recon))
    plt.title('Recon 1 (no ordering)')
    plt.xlabel('MSE: %g, SSIM: %g' % (
        compare_mse(np.abs(im), np.abs(recon)),
        compare_ssim(np.abs(im), np.abs(recon))))

    plt.subplot(*sh, 5)
    plt.imshow(np.abs(recon_mono_true))
    plt.title('Recon 2 (True monotonic ordering)')
    plt.xlabel('MSE: %g, SSIM: %g' % (
        compare_mse(np.abs(im), np.abs(recon_mono_true)),
        compare_ssim(np.abs(im), np.abs(recon_mono_true))))

    plt.subplot(*sh, 6)
    plt.imshow(np.abs(recon_mono))
    plt.title('Recon 3 (Estimated monotonic ordering)')
    plt.xlabel('MSE: %g, SSIM: %g' % (
        compare_mse(np.abs(im), np.abs(recon_mono)),
        compare_ssim(np.abs(im), np.abs(recon_mono))))

    plt.subplot(*sh, 7)
    plt.imshow(np.abs(im - recon))
    plt.title('Recon 1 Residual')

    plt.subplot(*sh, 8)
    plt.imshow(np.abs(im - recon_mono_true))
    plt.title('Recon 2 Residual')

    plt.subplot(*sh, 9)
    plt.imshow(np.abs(im - recon_mono))
    plt.title('Recon 3 Residual')

    plt.show()
