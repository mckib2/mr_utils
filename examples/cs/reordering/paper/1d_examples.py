'''1D examples to show us that we can find effective orderings.'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct

class Sparsify(object):
    '''Picklable sparsifying transform object.'''

    def __init__(self, prior):
        self.x0 = np.atleast_1d(prior[0])

    def forward_fd(self, x):
        '''Sparsifying transform, finite differences.'''
        return np.diff(x)

    def inverse_fd(self, x):
        '''Inverse sparsifying transform, finite differences.'''
        return np.concatenate((self.x0, x)).cumsum()

    def forward_dct(self, x):
        '''Sparsifying transform, discrete cosine transform.'''
        return dct(x, norm='ortho')

    def inverse_dct(self, x):
        '''Inverse sparsifying transform, discrete cosine transform.'''
        return idct(x, norm='ortho')

if __name__ == '__main__':

    # Let's make a signal, any signal will do
    N = 70
    x = np.random.normal(1, 1, N)
    S = Sparsify(x)

    plt.plot(x)
    plt.show()

    # Finite differences
    
