'''Proof of concept multiscale aliasing example.

Notes
-----
The idea is to collect progressively more undersampled averages, i.e.,
first acquisition is R=1, second acquisition is R=2, and so on.  Since
we have the R=1 image, we can do a least squares fit to incorporate
the aliased images' information.

As a simple example, let x be a pixel and x_i be the pixel in the R=i
average.  Then y_1, z_1, etc. are the aliased components of R=2, R=3,
etc.:

x_1 = x_1
x_2 = (x_1 + y_1)/2
x_3 = (x_1 + y_1 + z_1)/3
...

Note that this time domain equivalence is not completely true due to
Gibbs ringing artifacts.  Is this true when acquiring real data?

The original idea was to do something with coding theory, where we can
encode things using aliasing.  Seems to not be worth it from an SNR
perspective, since R=1's noise will dominate the least squares
solution.
'''

from math import ceil

import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse

if __name__ == '__main__':

    # Make a ramp
    N = 500
    s = np.cos(np.linspace(0, 2*np.pi, N))
    time = 100 # how much time it takes for full sampling

    # Noise params
    noise_std = 0.1

    # We want several undersampling factors
    Rs0 = [1, 2, 3]

    # Get the equivalent time fully-sampled averages
    eq_time = np.sum([time/R for R in Rs0])
    print('Equivalent time: %g' % eq_time)
    Rs1 = [1]*ceil(eq_time/time)
    print('Actual compared time: %g' % (len(Rs1)*time))
    Rss = [Rs0, Rs1]

    shat = []
    for Rs in Rss:
        nRs = len(Rs)

        # Get our coefficient matrix set up
        A = np.zeros((nRs*N, N))
        b = np.zeros(nRs*N)

        # Make it so
        for ii, R in enumerate(Rs):

            # Add noise if we wanted it
            if noise_std > 0:
                s00 = s + np.random.normal(0, noise_std, N)
            else:
                s00 = s.copy()

            # Make the aliased signal
            s0 = np.zeros(N)
            for jj in range(R):
                s0 += np.roll(s00, ceil(jj*N/R))
                A0 = np.roll(np.eye(N), ceil(jj*N/R), axis=1)

                # Update A to reflect the contents of s0
                A[(N*ii):(N*(ii+1)), :] += A0/R
            s0 /= R

            # Update observed vector
            b[(N*ii):(N*(ii+1))] = s0

        # Solve the least squares problem
        shat0 = np.linalg.lstsq(A, b, rcond=None)[0]
        shat.append(shat0)

    # Look at how we did
    plt.plot(s)
    for shat0 in shat:
        plt.plot(shat0, '--')
        print(np.var(s - shat0), compare_mse(s, shat0))
    plt.show()
