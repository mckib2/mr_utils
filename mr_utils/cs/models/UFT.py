'''Undersampled Fourier transform encoding model.

I'm calling "encoding model" how we encode the image domain signal to get to
the acquisiton domain.  In the case of MR, we measure k-space of the image we
want, so the encoding model is simply the Fourier transform (ignoring all the
other complications...).  This object provides methods to go into k-space and
get back out assuming we undersample according to some mask.

forward_ortho, inverse_ortho are probably the ones you want.
'''

import numpy as np

class UFT(object):
    '''Undersampled Fourier Transform (UFT) data acquisiton model.

    Attributes
    ==========
    samp : array_like
        Boolean sampling pattern.
    '''

    def __init__(self, samp):
        '''Initialize with binary sampling pattern.

        Parameters
        ==========
        samp : array_like
            Boolean sampling mask.
        '''
        self.samp = samp

    def forward(self, x, axes=None):
        '''Fourier encoding with binary undersampling pattern applied.

        Parameters
        ==========
        x : array_like
            Matrix to be transformed.
        axes : tuple
            Dimensions to Fourier transform if x is not 2d.

        Returns
        =======
        array_like
             Fourier transform (no fftshift) of `x` with sampling mask applied.

        Notes
        =====
        This forward transform has no fftshift applied.
        '''
        if axes is not None:
            return np.fft.fftn(x, axes=axes)*self.samp
        return np.fft.fft2(x)*self.samp

    def forward_s(self, x):
        '''Fourier encoding with binary undersampling pattern applied.

        Parameters
        ==========
        x : array_like
            Matrix to be transformed.

        Returns
        =======
        array_like
            Fourier transform (with fftshift) of `x` with sampling mask
            applied.

        Notes
        =====
        This forward transform applies fftshift before masking.
        '''
        return np.fft.fftshift(np.fft.fft2(x))*self.samp

    def forward_ortho(self, x):
        '''Normalized Fourier encoding with binary undersampling.

        Parameters
        ==========
        x : array_like
            Matrix to be transformed.

        Returns
        =======
        array_like
            Fourier transform of `x` with sampling mask applied and normalized.

        Notes
        =====
        This forward transform applied fftshift before FFT and after.
        '''
        tmp = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(x)))
        tmp *= self.samp/np.sqrt(tmp.size)
        return tmp

    def inverse(self, x, axes=None):
        '''Inverse fourier encoding.

        Parameters
        ==========
        x : array_like
            Matrix to be transformed.
        axes : tuple
            Dimensions to Fourier transform if x is not 2d.

        Returns
        =======
        array_like
            Inverse fourier transform of `x`.
        '''
        if axes is not None:
            return np.fft.ifftn(x, axes=axes)
        return np.fft.ifft2(x)

    def inverse_ortho(self, x):
        '''Inverse Normalized Fourier encoding.

        Parameters
        ==========
        x : array_like
            Matrix to be transformed.

        Returns
        =======
        array_like
            Inverse fourier transform of `x`, fftshifted, and normalized.

        Notes
        =====
        This transform applied ifftshift before and after ifft2.
        '''
        tmp = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(x)))
        tmp *= np.sqrt(x.size)
        return tmp
