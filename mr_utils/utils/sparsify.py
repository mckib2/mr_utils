'''Picklable class that implements several common transforms.'''

import numpy as np
from scipy.fftpack import dct, idct
import pywt

class Sparsify(object):
    '''Picklable sparsifying transform object.

    Properties
    ----------
    axis : int, optional
        This is the axis to perform the transform along.
    wvlt : str, optional
        The type of wavelet to use when performing forward and inverse
        wavelet transforms.
    '''

    def __init__(self, axis=0, wvlt='db1'):

        # This is the axis we operate along
        self.axis = axis

        # Store what kind of wavelet we want to be doing
        self.wvlt = wvlt

        # We'll need to save the beginning sample to do the inverse
        # finite difference transform
        self.x0 = None

    def forward_fd(self, x):
        '''Sparsifying transform, finite differences.'''
        tmp = np.moveaxis(x, self.axis, -1)
        self.x0 = np.expand_dims((tmp[..., 0]), self.axis)
        return np.diff(x, axis=self.axis)

    def inverse_fd(self, x):
        '''Inverse sparsifying transform, finite differences.'''
        if self.x0 is not None:
            return np.concatenate(
                (self.x0, x), axis=self.axis).cumsum(axis=self.axis)
        return x.cumsum(axis=self.axis)

    def forward_dct(self, x):
        '''Sparsifying transform, discrete cosine transform.'''
        return dct(x, axis=self.axis, norm='ortho')

    def inverse_dct(self, x):
        '''Inverse sparsifying transform, discrete cosine transform.
        '''
        return idct(x, axis=self.axis, norm='ortho')

    def forward_wvlt(self, x):
        '''Sparsifying transform, wavelet transform.'''
        cA, cD = pywt.dwt(x, self.wvlt, axis=self.axis)
        return np.concatenate((cA, cD), axis=self.axis)

    def inverse_wvlt(self, x):
        '''Inverse sparsifying transform, wavelet transform.'''
        c = np.split(x, 2, axis=self.axis)
        return pywt.idwt(c[0], c[1], self.wvlt, axis=self.axis)
