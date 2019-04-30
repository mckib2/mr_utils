'''Take a look at some sample data and see the distribution of pixels.

Notes
-----
These are not normally distributed (although the noise of real/imag
parts are -- noise of magnitude is Rayleigh).  The real/imag parts
look approximately Laplacian.  What's notable is that the variance of
the pixel intensities is smaller for real/imag separately than the
magnitude data.  This means we get more similar measurements when we
look at real/imag, therefore, when we assume TV, we will do better
by doing finite differences on the data with less variance -- the
real and imaginary parts separately!

Notice that it's hard to compare phase because it's wrapped and we
see approximately uniform distributing between -pi and pi.

So as long as var(real/imag) < var(magnitude), then we prefer to
operate separately on real and imaginary components.
'''

import numpy as np
import matplotlib.pyplot as plt

from mr_utils.test_data import load_test_data

if __name__ == '__main__':

    # Load in STCR recon
    path = ('mr_utils/test_data/examples/cs/temporal/')
    imspace = load_test_data(
        path, ['stcr_recon'])[0]

    real = imspace.real.flatten()
    imag = imspace.imag.flatten()
    mag = np.abs(imspace.flatten())
    phase = np.angle(imspace.flatten())

    # Show the variance of the measurements
    print('Var of real: %g' % np.var(real)) # Laplacian?
    print('Var of imag: %g' % np.var(imag)) # Laplacian?
    print('Var of  mag: %g' % np.var(mag)) # One-sided

    # Phase is approximately uniformly distributed it looks like
    # print(np.var(phase), (2*np.pi)**2/12) # This is wrapped though

    # nbins = 'auto'
    nbins = 100
    plt.subplot(1, 4, 1)
    plt.hist(real, bins=nbins, density=True)
    plt.title('Real')

    plt.subplot(1, 4, 2)
    plt.hist(imag, bins=nbins, density=True)
    plt.title('Imag')

    plt.subplot(1, 4, 3)
    plt.hist(mag, bins=nbins, density=True)
    plt.title('Magnitude')

    plt.subplot(1, 4, 4)
    plt.hist(phase, bins=nbins, density=True)
    plt.title('Phase')

    plt.show()


    # We might think that real/imag variance is always lower than
    # magnitude's variance, but can we find a counter-example?  We
    # can indeed, a very simple one!  Consider a circle in the
    # complex plane:
    sig = np.exp(1j*np.linspace(0, 2*np.pi, 100))
    sig_r = sig.real
    sig_i = sig.imag
    sig_mag = np.abs(sig)
    print('Var of real: %g' % np.var(sig_r))
    print('Var of imag: %g' % np.var(sig_i))
    print('Var of  mag: %g' % np.var(sig_mag))

    plt.plot(sig.real, sig.imag, '*')
    plt.axis('square')
    plt.title('Low var in mag, but not real/imag')
    plt.show()
