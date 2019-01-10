import numpy as np
from mr_utils.test_data import SCRReordering
from mr_utils import view

if __name__ == '__main__':

    # Load in the test data
    kspace = np.fft.fftshift(SCRReordering.Coil1_data())
    imspace = np.fft.ifft2(kspace)

    # We need a mask
    mask = np.fft.fftshift(SCRReordering.mask())

    # Undersample data to get prior
    kspace_u = kspace*mask
    imspace_u = np.fft.ifft2(kspace_u)

    
