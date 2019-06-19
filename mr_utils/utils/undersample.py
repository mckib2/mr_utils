'''Undersample signals.'''

import numpy as np

def undersample(
        x, R=(2, 1), acs=(.1, .1), forward_fun=None,
        inverse_fun=None, method='gauss', ret_kspace=False,
        ret_mask=False):
    '''Create undersampled signal from x.

    Parameters
    ----------
    x : array_like
        Signal to be undersampled.
    R : tuple, optional
        Undersampling factor.
    acs : tuple, optional
        Autocalibration signal, as percentages of dimension sizes.
    forward_fun : callable, optional
        Returns the forward transformation before undersampling.
    inverse_fun : callable, optional
        Returns the inverse transformation after undersampling.
    method : {'gauss'}, optional
        Undersampling pattern.
    ret_kspace : bool, optional
        Return the k-space instead of image space.
    ret_mask : bool, optional
        Return the boolean mask useed for undersampling.

    Returns
    -------
    y : array_like
        Undersampled version of x.
    '''

    k = [int(x.shape[idx]/R[idx]) for idx in range(x.ndim)]

    mask = np.zeros(x.shape, dtype=bool)
    ACS = np.zeros(x.shape, dtype=bool)
    if method == 'gauss':
        from scipy.stats import norm

        for ii in range(x.ndim):

            xx = np.linspace(
                norm.ppf(0.001), norm.ppf(0.999), x.shape[ii])
            p = norm.pdf(xx)
            p /= np.sum(p)
            idx = np.random.choice(
                np.arange(x.shape[ii]), k[ii], replace=False, p=p)

            mask0 = np.zeros(x.shape, dtype=bool)
            mask0 = np.moveaxis(mask0, ii, 0)
            mask0[idx, ...] = True
            mask0 = np.moveaxis(mask0, 0, ii)

            if ii > 0:
                mask = np.logical_and(mask, mask0)
            else:
                mask = mask0.copy()

            # import matplotlib.pyplot as plt
            # plt.imshow(mask)
            # plt.title('%d' % ii)
            # plt.xlabel('%g' % np.sum(mask.flatten()))
            # plt.show()

            # Now for the ACS
            acs0 = np.zeros(x.shape, dtype=bool)
            acs0 = np.moveaxis(acs0, ii, 0)
            ctr = int(x.shape[ii]/2)
            pad = int(acs[ii]*x.shape[ii]/2)
            acs0[ctr-pad:ctr+pad, ...] = True
            acs0 = np.moveaxis(acs0, 0, ii)
            if ii > 0:
                ACS = np.logical_and(ACS, acs0)
            else:
                ACS = acs0.copy()
            # from mr_utils import view
            # view(ACS)

    # Add the ACS
    mask += ACS
    # from mr_utils import view
    # view(mask)

    if (forward_fun is None) and (inverse_fun is None):
        forward_fun = lambda x0: np.fft.fftshift(np.fft.fft2(
            np.fft.fftshift(x0)))
        inverse_fun = lambda x0: np.fft.ifftshift(np.fft.ifft2(
            np.fft.ifftshift(x0)))

    # from mr_utils import view
    # view(forward_fun(x)*mask, log=True)
    if ret_kspace:
        y = forward_fun(x)*mask
    else:
        y = inverse_fun(forward_fun(x)*mask)

    if ret_mask:
        return(y, mask)
    return y
