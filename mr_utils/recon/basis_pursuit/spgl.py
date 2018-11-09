import numpy as np
import matplotlib.pyplot as plt
from spgl1 import spg_bp

if __name__ == '__main__':

    # Ax = b

    # Get original image
    n = 75
    frac = 3/4
    t = np.linspace(-np.pi*frac,np.pi*frac,n)
    x = np.fft.ifft(np.fft.fft(2.5*np.sin(t)))

    # Create dictionary, D
    m = int(n/2)
    D = np.fft.fft(np.eye(n,n))

    # Create A
    np.random.seed(0)
    idx = np.random.permutation(n)
    idx = idx[0:m]
    A = D[idx,:]

    # Sense b in the time domain
    b = x[idx]

    # Run spgl1 solver to get coefficients
    c,resid,grad,info = spg_bp(A,b)

    # Reconstruct estimate of x
    x_hat = D.dot(c)

    # Get estimate from b
    x_b = np.zeros(x.shape,dtype='complex')
    x_b[idx] = b

    plt.plot(np.abs(x))
    plt.plot(np.abs(x_b))
    plt.plot(np.abs(x_hat))
    plt.show()
