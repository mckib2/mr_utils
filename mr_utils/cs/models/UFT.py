import numpy as np
import matplotlib.pyplot as plt

class UFT(object):
    '''Undersampled Fourier Transform (UFT) data acquisiton model.'''

    def __init__(self,samp):
        self.samp = samp

    def forward(self,x):
        return(np.fft.fft2(x)*self.samp)

    def inverse(self,x):
        return(np.fft.ifft2(x))
