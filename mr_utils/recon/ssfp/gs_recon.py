import numpy as np
from mr_utils.sim.ssfp import get_complex_cross_point

def get_max_magnitudes(I1,I2,I3,I4):
    '''Find maximum magnitudes for each pixel over all four input images.'''

    stacked = np.dstack(np.abs((I1,I2,I3,I4)))
    I_mag = np.max(stacked,axis=-1)
    return(I_mag)

def get_max_magnitudes_for_loop(I1,I2,I3,I4):
    '''Find maximum magnitudes for each pixel over all four input images.

    This one loops over each pixel as verification for get_max_magnitudes().
    '''

    # Flatten all the phase cycled images and get magnitude images
    shape0 = I1.shape
    I1 = np.abs(I1.flatten())
    I2 = np.abs(I2.flatten())
    I3 = np.abs(I3.flatten())
    I4 = np.abs(I4.flatten())

    # Get max magnitudes pixel by pixel
    I_mag = np.zeros(I1.shape)
    for ii in range(I1.size):
        I_mag[ii] = np.max([ I1[ii],I2[ii],I3[ii],I4[ii] ])
    return(I_mag.reshape(shape0))

def gs_recon_for_loop(I1,I2,I3,I4):

    # Flatten all the phase cycled images
    shape0 = I1.shape
    I1 = I1.flatten()
    I2 = I2.flatten()
    I3 = I3.flatten()
    I4 = I4.flatten()

    # Demodulate bSSFP signal pixel by pixel
    I = np.zeros(I1.shape,dtype='complex')
    for ii in range(I1.size):
        I[ii] = get_complex_cross_point(I1[ii],I2[ii],I3[ii],I4[ii])

        # Regularize with complex sum
        if (np.abs(I[ii]) > np.abs(I1[ii])) and (np.abs(I[ii]) > np.abs(I2[ii])) and (np.abs(I[ii]) > np.abs(I3[ii])) and (np.abs(I[ii]) > np.abs(I4[ii])):
            I[ii] = I1[ii] + I2[ii] + I3[ii] + I4[ii]
    return(I.reshape(shape0))

def gs_recon(I1,I2,I3,I4):

    # Get geometric solution for demoduled M for all pixels
    I = get_complex_cross_point(I1,I2,I3,I4)

    # Get maximum pixel magnitudes for all input images
    I_max_mag = get_max_magnitudes(I1,I2,I3,I4)

    # Find the complex sum
    CS = I1 + I2 + I3 + I4

    # For each pixel, if the magnitude if greater than the maximum magnitude of
    # all four input images, then replace the pixel with the CS solution.  This
    # step regularizes the direct solution and effectively removes all
    # singularities
    mask = np.abs(I) > I_max_mag
    I[mask] = CS[mask]

    

    return(I)

if __name__ == '__main__':
    pass
