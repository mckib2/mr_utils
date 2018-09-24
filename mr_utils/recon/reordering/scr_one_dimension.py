import numpy as np
from time import time
import matplotlib.pyplot as plt

def scr_one_dimension(kspace,mask,prior=None,alpha0=1,alpha1=.002,beta2=1e-8,niters=5000):
    # Find a place to start from
    measuredImgDomain = np.fft.ifft(kspace)
    img_est = measuredImgDomain.copy()
    W_img_est = np.fft.ifft(np.fft.fft(img_est)*mask)


    # If we don't have one...use undersampled data as prior
    if prior is None:
        prior = img_est.copy()

    # Determine ordering
    # sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y = sort_real_imag_parts_space(prior*1000)

    # gradient descent minimization
    t0 = time()
    for ii in range(niters):
        # Find fidelity term
        # W_img_est = np.fft.ifft2(np.fft.fft2(img_est)*mask)
        fidelity_update = alpha0*(measuredImgDomain - W_img_est)

        # Spatial re-ordering - TV
        TV_term_reorder_update_real = np.gradient(img_est.real)
        TV_term_reorder_update_imag = np.gradient(img_est.imag)
        TV_term_reorder_update = alpha1*0.5*(TV_term_reorder_update_real + 1j*TV_term_reorder_update_imag)

        # Computing spatial regul - TV
        TV_term_update = np.gradient(img_est)*alpha1*0.5

        # Take a step
        img_est += fidelity_update + TV_term_update + TV_term_reorder_update

        W_img_est = np.fft.ifft(np.fft.fft(img_est)*mask)

        print('Status: [%d%%]\r' % (100*ii/niters),end='')
    print('Total time: %g sec' % (time()-t0))

    return(img_est)
