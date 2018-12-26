import numpy as np
from skimage.measure import compare_mse
import matplotlib.pyplot as plt
from mr_utils.cs import IHT
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

if __name__ == '__main__':
    N = 2000 # signal length
    n = 300 # Number of measurements


    # Generate transform matrix, normalize columns
    D = np.fft.fft(np.eye(N))
    fac = np.sqrt(np.sum(np.abs(D)**2,axis=0))
    D /= fac

    # Create sparse signal by choosing one of the columns of D
    s = D[:,1750]
    x = np.dot(D,s.conj())
    plt.plot(s.real)
    plt.show()

    # Pick where to make measurements
    p = np.random.permutation(N)[0:n]
    A = D[p,:]

    # Simulate the random measurements of signal, s
    y = s[p]

    # Reconstruct using IHT
    x_iht = IHT(A,y,k=10,x=x,disp=True)

    # We fail sometimes if we don't get a random matrix that satisfies RIP
    if not np.allclose(x_iht,x):
        logging.warning('x_iht might not be a good approximation to x!')

    # # Check to make sure we're recovering the correct signal after transform
    # plt.plot(s.real)
    # plt.plot(np.dot(D,x_iht).real,'--')
    # plt.show()

    # Look at it!
    plt.plot(np.abs(x*fac),label='True | x[n] |')
    plt.plot(np.abs(x_iht*fac),'--',label='Recon | x_iht[n] |')
    plt.xlabel('time index, n')
    plt.title('MSE: %g' % compare_mse(np.abs(x),np.abs(x_iht)))
    plt.legend()
    plt.show()
