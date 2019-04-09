'''Undersampled Fourier transform encoding model.

I'm calling "encoding model" how we encode the image domain signal to
get to the acquisiton domain.  In the case of MR, we measure k-space
of the image we want, so the encoding model is simply the Fourier
transform (ignoring all the other complications...).  This object
provides methods to go into k-space and get back out assuming we
undersample according to some mask.

forward_ortho, inverse_ortho are probably the ones you want.
'''

import numpy as np

class UFT(object):
    '''Undersampled Fourier Transform (UFT) data acquisiton model.

    Attributes
    ----------
    samp : array_like
        Boolean sampling pattern.
    axes : tuple
        Axes to perform FFT over.
    scale : bool
        Whether or not to scale ortho transforms.
    '''

    def __init__(self, samp, axes=None, scale=True):
        '''Initialize with binary sampling pattern.

        Parameters
        ----------
        samp : array_like
            Boolean sampling mask.
        axes : tuple, optional
            Axes to perform FFT over.
        scale : bool, optional
            Whether or not to scale ortho transforms.
        '''
        self.samp = samp

        if axes is None:
            self.axes = None
        else:
            self.axes = axes

        self.scale = scale

    def forward(self, x, axes=None):
        '''Fourier encoding with binary undersampling pattern applied.

        Parameters
        ----------
        x : array_like
            Matrix to be transformed.
        axes : tuple
            Dimensions to Fourier transform if x is not 2d.

        Returns
        -------
        array_like
             Fourier transform (no fftshift) of `x` with sampling
             mask applied.

        Notes
        -----
        This forward transform has no fftshift applied.
        '''
        if axes is None:
            axes = self.axes
        return np.fft.fftn(x, axes=axes)*self.samp

    def forward_s(self, x):
        '''Fourier encoding with binary undersampling pattern applied.

        Parameters
        ----------
        x : array_like
            Matrix to be transformed.

        Returns
        -------
        array_like
            Fourier transform (with fftshift) of `x` with sampling
            mask applied.

        Notes
        -----
        This forward transform applies fftshift before masking.
        '''
        return np.fft.fftshift(np.fft.fft2(
            x, axes=self.axes), axes=self.axes)*self.samp

    def forward_ortho(self, x, axes=None):
        '''Normalized Fourier encoding with binary undersampling.

        Parameters
        ----------
        x : array_like
            Matrix to be transformed.
        axes: tuple, optional
            Dimensions to perform FFT2 over.

        Returns
        -------
        array_like
            Fourier transform of `x` with sampling mask applied and
            normalized.

        Notes
        -----
        This forward transform applied fftshift before FFT and after.
        '''
        if axes is None:
            axes = self.axes
        tmp = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(
            x), axes=axes), axes=axes)
        if self.scale:
            tmp *= self.samp/np.sqrt(tmp.size)
        return tmp

    def inverse(self, x, axes=None):
        '''Inverse fourier encoding.

        Parameters
        ----------
        x : array_like
            Matrix to be transformed.
        axes : tuple
            Dimensions to Fourier transform if x is not 2d.

        Returns
        -------
        array_like
            Inverse fourier transform of `x`.
        '''
        if axes is None:
            axes = self.axes
        return np.fft.ifftn(x, axes=axes)

    def inverse_s(self, x):
        '''Inverse fourier encoding with fftshift.

        Parameters
        ----------
        x : array_like
            Matrix to be transformed.

        Returns
        -------
        array_like
            Inverse Fourier transform (with fftshift) of `x`

        Notes
        -----
        This inverse transform applies fftshift.
        '''
        return np.fft.fftshift(np.fft.ifft2(
            x, axes=self.axes), axes=self.axes)

    def inverse_ortho(self, x, axes=None):
        '''Inverse Normalized Fourier encoding.

        Parameters
        ----------
        x : array_like
            Matrix to be transformed.
        axes : tuple, optional
            Dimensions to Fourier transform if x is not 2d.

        Returns
        -------
        array_like
            Inverse fourier transform of `x`, fftshifted, and
            normalized.

        Notes
        -----
        This transform applied ifftshift before and after ifft2.
        '''
        if axes is None:
            axes = self.axes
        tmp = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(
            x, axes=axes), axes=axes), axes=axes)
        if self.scale:
            tmp *= np.sqrt(x.size)
        return tmp
