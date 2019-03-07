# I don't think this works yet

# import numpy as np
# from mr_utils.cs import rIHT
# import matplotlib.pyplot as plt
# from skimage.measure import compare_mse
# import logging
#
# logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)
#
# if __name__ == '__main__':
#     N = 2000 # signal length
#     n = 500 # Number of measurements
#     k = 30 # Number of non-zero elements
#
#     # We need a measurement matrix for total variation
#
#     # Generate random measurement matrix (normal), normalize columns
#     A = np.random.randn(n,N)
#     A /= np.sqrt(np.sum(A**2, axis=0))
#
#     # Sparse binary signal x, {+1,-1}
#     x = np.sign(np.random.rand(k)-0.5)
#     x = np.append(x,np.zeros(N-k))
#     x = x[np.random.permutation(np.arange(N))]
#
#     # Simulate measurement according to A
#     y = np.dot(A,x)
#
#     # Reconstruct using rIHT
#     x_riht = rIHT(A,y,k,x=x,disp=True)
#
#     # We fail sometimes if we don't get a random matrix that satisfies RIP
#     if not np.allclose(x_riht,x):
#         logging.warning('x_riht might not be a good approximation to x!')
#
#     # Look at it!
#     plt.plot(x,label='True x[n]')
#     plt.plot(x_riht,'--',label='Recon x_riht[n]')
#     plt.xlabel('time index, n')
#     plt.title('MSE: %g' % compare_mse(x,x_riht))
#     plt.legend()
#     plt.show()
