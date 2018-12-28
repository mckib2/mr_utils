import numpy as np
import matplotlib.pyplot as plt
from  mr_utils.cs import IHT
from skimage.measure import compare_mse
import logging

if __name__ == '__main__':
    N = 2000
    n = 2000
    k = 4 # use even numbers

    # Make a dictionary
    D = np.diff(np.eye(N,N+1),axis=1)
    fac = np.sqrt(np.sum(np.abs(D)**2,axis=0))
    D /= fac
    # print(fac)

    # Make a sparse signal in TV domain -- how about a square wave!
    s = np.sin(np.pi*np.arange(N)*k/(N))
    s[s < 0] = 0.0
    s[s > 0] = 1.0
    x = np.dot(D,s)
    # plt.plot(x)
    # plt.show()

    # Pick where to make measurements
    p = np.random.permutation(N)[0:n]
    A = D[p,:]

    # Simulate the random measurements of signal, s
    y = s[p]
    # plt.plot(y)
    # plt.show()

    # Reconstruct using IHT
    x = np.roll(x,-1) # Why do I need to do this?
    x_iht = IHT(A,y,k=k,x=x,disp=True,maxiter=200)

    # Why do I need this?
    x_iht = np.roll(x_iht,int(N/4))

    # plt.plot(x[x.nonzero()])
    # plt.plot(x_iht[x_iht.nonzero()],'--')
    # plt.show()
    # print(compare_mse(x[x.nonzero()],x_iht[x_iht.nonzero()]))
    # print(x.nonzero(),x_iht.nonzero())

    # We fail sometimes if we don't get a random matrix that satisfies RIP
    if not np.allclose(x_iht,x):
        logging.warning('x_iht might not be a good approximation to x!')

    # Look at it!
    plt.plot(x,label='True x[n]')
    plt.plot(x_iht,'--',label='Recon x_iht[n]')
    plt.xlabel('time index, n')
    plt.title('MSE: %g' % compare_mse(x,x_iht))
    plt.legend()
    plt.show()
