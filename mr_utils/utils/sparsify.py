'''Picklable class that implements several common transforms.'''

import numpy as np
from scipy.fftpack import dct, idct

class Sparsify(object):
    '''Picklable sparsifying transform object.'''

    def __init__(self, prior, axis=0):

        # This is the axis we operate along
        self.axis = axis

        # Move the axis we do work on to the end
        tmp = np.moveaxis(prior, axis, -1)

        # Grab the first sample for finite differences
        self.x0 = np.expand_dims((tmp[..., 0]), axis)


    def forward_fd(self, x):
        '''Sparsifying transform, finite differences.'''
        return np.diff(x, axis=self.axis)

    def inverse_fd(self, x):
        '''Inverse sparsifying transform, finite differences.'''
        return np.concatenate(
            (self.x0, x), axis=self.axis).cumsum(axis=self.axis)

    def forward_dct(self, x):
        '''Sparsifying transform, discrete cosine transform.'''
        return dct(x, axis=self.axis, norm='ortho')

    def inverse_dct(self, x):
        '''Inverse sparsifying transform, discrete cosine transform.
        '''
        return idct(x, axis=self.axis, norm='ortho')
