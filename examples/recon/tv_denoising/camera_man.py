''' Apply TV-L1 image denoising with the primal-dual algorithm to simple image.
'''

import numpy as np
import matplotlib.pyplot as plt
from skimage.data import camera

from mr_utils.recon.tv_denoising import tv_l1_denoise

if __name__ == '__main__':
    sigma = 10
    im = camera().astype(np.float64)
    im += sigma*np.random.normal(0, 1, im.shape)
    im /= np.max(im)

    im0 = tv_l1_denoise(im, 1, disp=False, niter=300)

    plt.subplot(1, 3, 1)
    plt.imshow(im)
    plt.title('Corrupted Image')
    plt.subplot(1, 3, 2)
    plt.imshow(im0)
    plt.title('TV Denoised')
    plt.subplot(1, 3, 3)
    plt.imshow(np.abs(im - im0))
    plt.title('Residue')
    plt.show()
