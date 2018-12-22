from scipy.optimize import linprog
from scipy.fftpack import dct,idct
import numpy as np
import matplotlib.pyplot as plt

'''
Consider the problem:
    hat{x} = argmin_z ||z||_1  s.t.  Az = y

This can be solved using linear programming.  Let's try it.
'''

if __name__ == '__main__':

    # Signal we want to measure
    n = 500
    t = np.linspace(0,2*np.pi,n)
    x = np.cos(2*np.pi*t/2)# + np.sin(2*np.pi*t/.05)
    # view(x)
    # view(dct(x))

    # Make DCT dictionary
    D = dct(np.eye(n))

    # Prove that we can sparsely represent this signal
    y = D.dot(x)
    # plt.plot(y)
    # plt.plot(dct(x))
    # plt.show()

    # Choose the indices along that we'll keep
    k = int(n/20)
    idx = np.random.permutation(n)
    idx = idx[0:k]

    # Sample x at the indices and grab the corresponding undersampled
    # dictionary, A
    # y_hat = np.zeros(x.shape)
    y_hat = x[idx]
    # A = np.zeros(D.shape)
    A = D[idx,:]

    # Set us up as a linear programming problem
    Aeq = np.hstack((A,np.zeros(A.shape)))
    cols = A.shape[1]
    c = np.hstack((np.zeros(cols),np.ones(cols)))
    print('Aeq: ',Aeq.shape)
    print('c: ',c.shape)

    # add abs(x) to y_hat
    y_hat = np.concatenate((y_hat,np.abs(y_hat)))
    print('y_hat: ',y_hat.shape)

    Aub0 = np.hstack((np.eye(cols),-np.eye(cols)))
    Aub1 = np.hstack((-np.eye(cols),-np.eye(cols)))
    Aub = np.vstack((Aub0,Aub1))
    bub = np.zeros(2*cols)
    print('Aub0: ',Aub0.shape)
    print('Aub: ',Aub.shape)
    print('bub: ',bub.shape)

    # Do the thing!
    bnds = (0,None)*n + (None,None)*n
    # print(bnds)
    res = linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=y_hat,bounds=bnds,method='interior-point',callback=None,options={'disp':True})
    x_hat = res['x'][:n]
    print(res)

    # Show me what we got:

    # plt.plot(y)
    plt.plot(res['x'])
    plt.show()

    plt.plot(idct(x_hat))
    plt.plot(x)
    # y = np.zeros(x.shape)
    # y[idx] = x[idx]
    # plt.plot(y)
    plt.show()
