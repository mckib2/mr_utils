import numpy as np
import matplotlib.pyplot as plt

class UFT(object):
    '''Undersampled Fourier Transform (UFT) data acquisiton model.'''

    def __init__(self,samp):
        '''Initialize with binary sampling pattern.'''
        self.samp = samp

    def forward(self,x):
        '''Fourier encoding with binary undersampling pattern applied.

        This forward transform has no fftshift applied.
        '''
        return(np.fft.fft2(x)*self.samp)

    def forward_s(self,x):
        '''Fourier encoding with binary undersampling pattern applied.

        This forward transform applies fftshift before masking.
        '''
        return(np.fft.fftshift(np.fft.fft2(x))*self.samp)

    def forward_ortho(self,x):
        '''Normalized Fourier encoding with binary undersampling.

        This forward transform applied fftshift before FFT and after.
        '''
        tmp = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(x)))
        tmp *= self.samp/np.sqrt(tmp.size)
        return(tmp)

    def inverse(self,x):
        '''Inverse fourier encoding.'''
        return(np.fft.ifft2(x))

    def inverse_ortho(self,x):
        '''Inverse Normalized Fourier encoding.

        This transform applied ifftshift before and after ifft2.
        '''
        tmp = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(x)))
        tmp *= np.sqrt(x.size)
        return(tmp)
