'''Try a simple shape so we can see what's happening.

Simple example: N=6, R=2, NC=2

Desired signal is:
    x = [x0 x1 x2 x3 x4 x5]

Measured signals y0, y1 from each coil with sensitivies sij:
    y0 = [y00         y01         y02         y03 y04 y05]
       = [(x0+x3)*s00 (x1+x4)*s01 (x2+x5)*s02 ...        ]
    y1 = [y10         y11         y12         y13 y14 y15]
       = [(x0+x3)*s10 (x1+x4)*s11 (x2+x5)*s12 ...        ]

    yi = (x + xs).si, xs=fftshift(x)
       = x.si + xs.si
       = x.si + x.ssi, ssi=fftshift(ssi)
       = x.(si + ssi)

       => x = yi.(si + ssi)^-1

Now assume we don't know the sensitivies and we have both R=2,3, NC=2:

    y02 = [(x0+x3)*s00 (x1+x4)*s01 (x2+x5)*s02 (x3+x0)*s03
           (x4+x1)*s04 (x5+x2)*s05]
    y12 = [(x0+x3)*s10 ... ]

    y03 = [(x0+x2+x4)*s00 (x1+x3+x5)*s01 (x0+x2+x4)*s02
           (x1+x3+x5)*s03 (x0+x2+x4)*s04 (x1+x3+x5)*s05]
    y13 = [(x0+x2+x4)*s10 ... ]



    y03 = (x + xs + xss).s0
        = x.(s0 + s0s + s0ss)

        => x = y03.(s0 + s0s + s0ss)^-1

'''

import numpy as np
import matplotlib.pyplot as plt

def get_bl_sig(N, bw=.5, freq=False):
    '''Create a generic bandlimited signal.

    Parameters
    ----------
    N : int
        Number of samples.  Will be rounded up to nearest even number
        for convienence.
    bw : float, 0 < bw < 1, optional
        Percentage of bandwidth used.
    freq : bool, optional
        Whether or not frequency domain representation is returned.

    Returns
    -------
    array_like
        The bandlimited signal (either time domain or frequency
        domain).
    '''

    # Make sure N is even
    if np.mod(N, 2):
        N += 1

    # Get length of inner signal
    M = np.ceil(N*bw).astype(int)

    # Make the inner signal
    sig = np.zeros(M)
    M5 = int(M/5)
    sig[:M5*2] = np.arange(M5*2)/(M5*2)
    sig[(M5*2):(M5*4)] = 1 + np.arange(M5*2)/(M5*8)
    sig[-M5:] = np.arange(M5)[::-1]*np.max(sig)/M5

    # Plug the inner signal into the whole signal
    L = int((N - M)/2)
    osig = np.zeros(N)
    osig[L:L+M] = sig

    # Give back frequency domain or time domain
    if freq:
        return osig
    return np.fft.ifftshift(np.fft.ifft(np.fft.ifftshift(osig)))


if __name__ == '__main__':

    # Make bandlimited signal
    N = 1000
    bw = .8
    freq = False
    s = get_bl_sig(N, bw=bw, freq=freq)

    # Sampling pattern
    mask = np.ones(N)
    ufac = 2
    assert ufac == 2, 'Only works for R=2 right now'
    scale_fac = ufac/(ufac-1)
    mask[ufac-1::ufac] = 0

    fft = lambda x0: np.fft.fftshift(np.fft.fft(np.fft.fftshift(
        x0)))
    su = fft(s*mask)

    s0 = np.zeros(N*2, dtype=su.dtype)
    fs = fft(s)
    pad = int((s0.size - N)/2)
    fsp = np.pad(fs, (pad, pad), mode='constant')
    for ii in range(-ufac, ufac+1):
        val = 1
        if ii != 0:
            val = (-1)**(ufac+ii+1)/(ufac-1)
        s0 += val*np.roll(fsp, np.ceil(ii*N/ufac).astype(int))
    s0 = s0[pad:-pad]

    plt.subplot(1, 3, 1)
    plt.plot((su*scale_fac).real)
    plt.plot(s0.real, '--')
    plt.title('Real')

    plt.subplot(1, 3, 2)
    plt.plot((su*scale_fac).imag)
    plt.plot(s0.imag, '--')
    plt.title('Imaginary')

    plt.subplot(1, 3, 3)
    plt.plot(np.abs(fs))
    plt.plot(np.abs(su*scale_fac), '--')
    plt.plot(np.abs(s0), ':')
    plt.show()
