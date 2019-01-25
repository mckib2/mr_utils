'''Gradient of total variation term for gradient descent update.'''

import numpy as np

def dTV(A, eps=1e-8):
    '''Compute derivative of the TV with respect to the matrix A.

    A -- 2d matrix (can be complex).
    eps -- small positive constant used to avoid a divide by zero.

    Implements Equation [13] from:
        Zhang, Yan, Yuanyuan Wang, and Chen Zhang. "Total variation based
        gradient descent algorithm for sparse-view photoacoustic image
        reconstruction." Ultrasonics 52.8 (2012): 1046-1055.
    '''

    # Note: I'm not sure np.roll is the thing to do as it's ambiguous what
    # happens on the edges of the update. Calling it good for now though, as
    # seems to be doing alright regardless.

    num1 = 2*A - np.roll(A, -1, axis=0) - np.roll(A, -1, axis=1)
    den1 = np.sqrt(np.abs(A - np.roll(A, -1, axis=0))**2 + \
        np.abs(A - np.roll(A, -1, axis=1))**2) + eps

    num2 = np.roll(A, 1, axis=0) - A
    den2 = np.sqrt(np.abs(np.roll(A, 1, axis=0) - A)**2 + \
        np.abs(np.roll(A, 1, axis=0) - np.roll(A, (1, -1)))**2) + eps

    num3 = np.roll(A, 1, axis=1) - A
    den3 = np.sqrt(np.abs(np.roll(A, 1, axis=1) - A)**2 + \
        np.abs(np.roll(A, 1, axis=1) - np.roll(A, (-1, 1)))**2) + eps

    update = num1/den1 - num2/den2 - num3/den3

    return update
