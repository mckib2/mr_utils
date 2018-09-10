import numpy as np
from mr_utils.sim.ssfp import get_complex_cross_point

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
    I = I.reshape(shape0)

    return(I)

def gs_recon(I1,I2,I3,I4):

    I = get_complex_cross_point(I1,I2,I3,I4)
    return(I)

if __name__ == '__main__':
    pass
