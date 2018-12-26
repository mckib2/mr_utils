import numpy as np

def nIHT(A,y,k,maxiter=200):
    '''Normalized iterative hard thresholding.

    Implements Algorithm 8.6 from:
        Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
        and applications. Cambridge University Press, 2012.
    '''

    # length of measurement vector and original signal
    n,N = A.shape[:]

    # Initializations
    x_hat = np.zeros(N)

    val = A.T.dot(y)
    thresh = -np.sort(-np.abs(val))[k-1]
    val[np.abs(val) < thresh] = 0
    T = np.nonzero(val)

    for ii in range(maxiter):

        r = y - np.dot(A,x_hat)
        g = np.dot(A.T,r)
        mu = np.linalg.norm(g)**2/np.linalg.norm(np.dot(A,g))**2

        xn = x_hat + mu*g
        thresh = -np.sort(-np.abs(xn))[k-1]
        xn[np.abs(xn) < thresh] = 0

        Tn = np.nonzero(xn)

        if Tn == T:
            x_hat = xn

        else:

            if mu <= (1 - c)*np.linalg.norm(xn - x_hat)**2/np.linalg.norm(np.dot(A,xn - x_hat))**2:
                x_hat = xn

            else:
                pass


    T = np.nonzero()

if __name__ == '__main__':
    pass
