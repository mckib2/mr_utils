import numpy as np
from mr_utils.cs import cosamp
import matplotlib.pyplot as plt
from skimage.measure import compare_mse
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

if __name__ == '__main__':
    N = 2000 # signal length
    n = 500 # Number of measurements
    k = 30 # Number of non-zero elements

    # Generate random measurement matrix (normal), normalize columns
    A = np.random.randn(n,N)
    A /= np.sqrt(np.sum(A**2, axis=0))

    # Sparse binary signal x, {+1,-1}
    x = np.sign(np.random.rand(k)-0.5)
    x = np.append(x,np.zeros(N-k))
    x = x[np.random.permutation(np.arange(N))]

    # Simulate measurement according to A
    y = np.dot(A,x)

    # Reconstruct using cosamp
    x_cosamp = cosamp(A,y,k,lstsq='exact',x=x,disp=True)

    # We fail sometimes if we don't get a random matrix that satisfies RIP
    if not np.allclose(x_cosamp,x):
        logging.warning('x_cosamp might not be a good approximation to x!')

    # Look at it!
    plt.plot(x,label='True x[n]')
    plt.plot(x_cosamp,'--',label='Recon x_cosamp[n]')
    plt.xlabel('time index, n')
    plt.title('MSE: %g' % compare_mse(x,x_cosamp))
    plt.legend()
    plt.show()
