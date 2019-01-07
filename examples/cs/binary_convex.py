from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_mse
from tqdm import tqdm

# Objective function to minimize
def obj(x,A,y,lamb):
    '''|| Ax - y ||_2^2 + lambda*|| x ||_1

    x -- Current image estimate.
    A -- CS measurement matrix.
    y -- Measured samples, i.e., y = A.dot(x_true).
    lamb -- Lambda, tradeoff between fidelity and sparsity constraint terms.
    '''
    return(np.linalg.norm(np.dot(A,x) - y)**2 + lamb*np.linalg.norm(x,ord=1))

# Gradient of objective function
# This gets more complicated for Minv when you have a sparsifying transform
def grad(x,A,y,lamb,beta=np.finfo(float).eps):
    ''' d/dx_i || Ax - y ||_2^2 + lambda*|| x ||_1

    x -- Current image estimate.
    A -- CS measurement matrix.
    y -- Measured samples, i.e., y = A.dot(x_true).
    lamb -- Lambda, tradeoff between fidelity and sparsity constraint terms.
    beta -- Small, nonnegative constant, e.g., make 1/(x+beta) defined.
    '''
    r = np.dot(A,x) - y
    fidelity = np.dot(A.conj().T,r)
    Minv = np.diag(1/(x+beta))
    sparse = np.dot(Minv,x)
    return(fidelity + lamb*sparse)

# Hessian?

if __name__ == '__main__':

    N = 2000 # signal length
    n = 500 # Number of measurements
    k = 20 # Number of non-zero elements

    # Generate random measurement matrix (normal), normalize columns
    np.random.seed(seed=1)
    A = np.random.randn(n,N)
    A /= np.sqrt(np.sum(A**2, axis=0))

    # Sparse binary signal x, {+1,-1}
    x = np.sign(np.random.rand(k)-0.5)
    x = np.append(x,np.zeros(N-k))
    x = x[np.random.permutation(np.arange(N))]

    # Simulate measurement according to A
    y = np.dot(A,x)

    # Find the best lambda value to use by cross-validation
    lambdas = np.linspace(1e-8,1e-6,10)
    err = np.zeros(lambdas.size)
    for idx,lamb in enumerate(tqdm(lambdas,desc='Find lambda',leave=False)):
        x0 = np.zeros(N)
        res = minimize(obj,args=(A,y,lamb),x0=x0,method='CG',jac=grad)
        xx = res['x']
        xx[np.argsort(np.abs(xx))[:-k]] = 0
        err[idx] = compare_mse(xx,x)
        # print(idx,lamb,err[idx],res['fun'])

    # Tradeoff between fidelity term and sparsity term
    idx = np.argmin(err)
    lam = lambdas[idx]
    plt.plot(lambdas,err)
    plt.plot(lambdas[idx],err[idx],'*',label='Choose this one')
    plt.xlabel('lambda values')
    plt.ylabel('MSE(x,x_hat)')
    plt.legend()
    plt.show()

    # Start from all 0s
    x0 = np.zeros(N)

    # CG seems to do the best
    # We could find the Hessian expressian, would this help significantly?
    res = minimize(obj,x0=x0,args=(A,y,lam),method='CG',jac=grad)
    x_hat = res['x']
    print(res)

    # Do some hard thresholding to clean things up
    x_hat[np.argsort(np.abs(x_hat))[:-k]] = 0

    plt.plot(x)
    plt.plot(x_hat,'--')
    plt.title('Convex Optimization')
    plt.show()

    # Doesn't seem to get the right amplitudes, but can find where the spikes
    # are
