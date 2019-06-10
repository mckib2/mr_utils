'''Try matching histogram of aliased image.

Notes
-----
What we have been doing is matching the histogram of the prior image
to the histogram of the transformed k-sparse constructed signal.  The
problem is that we expect the prior image to not be accurate...

So take the histogram of the raw inverse fourier transformed measured
k-space data.  This data will look nasty, naturally.  Then compare the
histogram of the constructed k-sparse signal that has been run through
the same sampling mask, i.e., has comparable aliasing.  This avoids
the problem of having to select an appropriate prior.

I'm not actually sure if this works better or not.  Just an idea.
'''

import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy import optimize
from scipy.spatial.distance import cdist

if __name__ == '__main__':

    fft = lambda x0: np.fft.fftshift(np.fft.fft(np.fft.fftshift(x0)))
    ifft = lambda x0: np.fft.ifftshift(np.fft.ifft(np.fft.ifftshift(
        x0)))

    # Sim params
    N = 70
    k = 5
    wvlt = 'db2'

    # Get a sparse signal
    ksparse = np.zeros(2*N) # LP and HP coefficients: [LP, HP]
    idx = np.random.choice(np.arange(2*N), k, replace=False)
    ksparse[idx] = np.random.random(k)*2
    x = pywt.idwt(ksparse[:N], ksparse[N:], wvlt)

    # Now make sparse under permutation
    p = np.random.permutation(x.size)
    x = x[p]

    # # Check it out
    # plt.plot(x)
    # pi = np.zeros(x.size, dtype=int)
    # pi[p] = np.arange(x.size)
    # plt.plot(np.concatenate(pywt.dwt(x[pi], wvlt)), '--')
    # plt.show()

    # Undersample in k-space, Gaussian sampling mask
    kspace = fft(x)
    mask = np.zeros(x.size, dtype=bool)
    mu, sigma2 = 0, 1
    xx = np.linspace(-sigma2*4, sigma2*4, x.size)
    prob = 1/np.sqrt(2*np.pi*sigma2)*np.exp(-(xx - mu)**2/(2*sigma2))
    prob /= np.sum(prob)
    idx = np.random.choice(
        np.arange(x.size), int(x.size*.5), replace=False, p=prob)
    mask[idx] = True
    kspace_u = kspace*mask

    # # Take a look
    # plt.plot(np.abs(ifft(kspace_u)))
    # plt.plot(np.abs(x))
    # plt.show()

    # Now we want to get it back by comparing against the alaiased
    # histogram

    def H(x0):
        '''Histogram'''
        return np.sort(x0)

    ref = H(ifft(kspace_u))
    def obj(cc):
        '''objective'''
        # cc are the sparse wavelet coefficients, so get the time
        # domain signal
        Ti = pywt.idwt(cc[:N], cc[N:], wvlt)
        Ti_u = ifft(fft(Ti)*mask)

        lam = .2
        return .5*np.linalg.norm(
            H(Ti_u) - ref)**2 + lam*np.linalg.norm(cc)

    c0 = np.random.random(2*N)/2
    chat = optimize.minimize(obj, c0)['x']
    # res = optimize.basinhopping(obj, c0)['x']
    # print(res)

    # Now find the right mapping
    Ti = pywt.idwt(chat[:N], chat[N:], wvlt)
    xhat = np.abs(ifft(fft(Ti)*mask))
    xref = np.abs(ifft(kspace_u))
    C = cdist(xref[:, None], xhat[:, None])
    rows, cols = optimize.linear_sum_assignment(C)

    # Take a look at the result
    plt.plot(np.abs(Ti[cols]))
    plt.plot(np.abs(x), '--')
    plt.plot(np.abs(ifft(kspace_u)), ':')
    plt.show()

    # plt.plot(np.concatenate(pywt.dwt(Ti, wvlt)))
    # plt.plot(np.concatenate(pywt.dwt(x, wvlt)))
    # plt.show()
