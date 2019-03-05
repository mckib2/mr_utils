'''Demonstrate basinhopping to solve for coefficient values.

Counting xk in x is a nonlinear operation (can't be represented by matrix
multiplies) as far as I can tell.  The closes I could come is the count
function in this file that unfortunely needs an element by element inverse.
You could run all the elements of down the diagonal of an x.size by x.size
matrix, then you get:
    trace [X*a - xk*a + 1]^-1

But remember that the offdiagonal elements are not truly zero, so the matrix is
ill-conditioned and does not give you thing answer (I tried it...).  So unless
there's a way to force all off of-diagonal elements to be zero (by masking?)
then you're stuck with trying to solve the coefficient value problem
numerically.

Thus this example: given the location of the coefficients, we use the
basinhopping algorithm to find the best coefficient values we can.  We even
dispense with histogram/kernel density estimators in this example in favor
of the simple object function:
    || sort(xhat) - sort(x) ||_2^2

which has the advantage of being stupid easy, although the gradient w.r.t c
could be tricky to come up with since we're sorting xhat...  But that was
always the problem, right?  Finding analytical solutions to combinatorial
problems is hard.  So jump and around some basins and try to get some
reasonable values -- that seems like a descent enough idea.

Results:
    Given that we know where the coefficients are, we actually do a great job
    of beating the sort(x), even when we don't find the optimal coefficient
    values -- many local minima appear to beat sorting.  Sorted coefficients
    have very large coefficients and the die off approximately exponentially,
    whereas our coefficient values don't die off -- they are quite large for
    all k, and then if the perfect coefficient values are not found, then they
    die off (exponentially), usually below the coefficient level of sort(x),
    however, this is not always the case (if we don't solve for good
    coefficient values).

    Large k is a funny choice (because sort(x) generally dies off pretty
    quickly), but will find coefficients such that after k, the coefficients
    are less than sort(x), and the first k coefficients are much larger than
    sort(x).

Notes on computation:
    Large N is hard on the linear_sum_assignment problem.
    Large k is hard on basinhopping.  Haven't tried tweaking anything on
    basinhopping, might be a fun afternoon activity...
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct
from scipy.optimize import basinhopping, linear_sum_assignment as lsa
from scipy.spatial.distance import cdist

def forward(x):
    '''Forward transform.'''
    return dct(x, norm='ortho')

def inverse(c):
    '''Inverse transform.'''
    return idct(c, norm='ortho')

def count(x, xk, a=1e20):
    '''Count number of xk in x.

    x -- Array with elements xk.
    xk -- Specific xk to count how many of.

    This is asymptotically true as a -> inf.
    '''
    return np.sum(1/((x - xk)*a + 1))

def count_all(x, x_ref, c_eq_ref, a=1e20):
    '''Count all.'''
    c_eq = np.zeros(N)
    for ii, xk in np.ndenumerate(x_ref):
        c_eq[ii] = count(x, xk, a)
    return np.linalg.norm(c_eq - c_eq_ref)

def obj(ck, idx, x_ref):
    '''Objective function for basinhopping.'''
    c = np.zeros(x_ref.size)
    c[idx] = ck
    return np.linalg.norm(np.sort(inverse(c)) - np.sort(x_ref))**2

if __name__ == '__main__':

    # Construct reference signals as usual
    N = 200
    k = 10
    c_true = np.zeros(N)
    idx_true = np.random.choice(np.arange(N), k)
    c_true[idx_true] = 2*np.random.random(k) - 1
    x_pi = inverse(c_true)
    x = np.random.permutation(x_pi)

    # # Make constraints at each xk
    # c_eq = np.zeros(N)
    # for ii, xk in np.ndenumerate(x):
    #     c_eq[ii] = count(x, xk)

    # Assuming we've guessed the right indices, can we find the right values?
    c0 = np.ones(k)
    res = basinhopping(obj, c0, minimizer_kwargs={'args':(idx_true, x,)})
    print(res)

    print(res['x'], c_true[idx_true])

    # Now solve the assignment problem
    c = np.zeros(N)
    c[idx_true] = res['x']
    xhat = inverse(c)
    C = cdist(xhat[:, None], x[:, None])
    rows, cols = lsa(C)

    # Show the people the coefficients!
    plt.plot(-np.sort(-np.abs(forward(xhat))), label='xhat')
    plt.plot(-np.sort(-np.abs(forward(x[cols]))), '--', label='An x_pi')
    plt.plot(-np.sort(-np.abs(forward(np.sort(x)))), ':', label='sort(x)')
    plt.legend()
    plt.title('Sorted DCT Coefficients')
    plt.show()
