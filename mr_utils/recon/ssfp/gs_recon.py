import numpy as np
from mr_utils.sim.ssfp import get_complex_cross_point
import warnings # We know skimage will complain about itself importing imp...
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

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
    Id = np.zeros(I1.shape,dtype='complex')
    for ii in range(I1.size):
        Id[ii] = get_complex_cross_point(I1[ii],I2[ii],I3[ii],I4[ii])

        # Regularize with complex sum
        if (np.abs(Id[ii]) > np.abs(I1[ii])) and (np.abs(Id[ii]) > np.abs(I2[ii])) and (np.abs(Id[ii]) > np.abs(I3[ii])) and (np.abs(Id[ii]) > np.abs(I4[ii])):
            Id[ii] = complex_sum(I1[ii],I2[ii],I3[ii],I4[ii])
    Id = Id.reshape(shape0)

    # Find weighted sums of image pairs (I1,I3) and (I2,I4)
    I1 = I1.reshape(shape0)
    I3 = I3.reshape(shape0)
    I2 = I2.reshape(shape0)
    I4 = I4.reshape(shape0)
    Iw13 = compute_Iw(I1,I3,Id)
    Iw24 = compute_Iw(I2,I4,Id)

    # Final result is found by averaging the two linear solutions for reduced
    # noise
    I = (Iw13 + Iw24)/2
    return(I)

def complex_sum(I1,I2,I3,I4):
    #  Should we divide by 4? That's not in Neal's paper
    CS = (I1 + I2 + I3 + I4)/4
    return(CS)

def gs_recon(I1,I2,I3,I4):
    '''Full Geometric Solution method following Xiang and Hoff's 2014 paper.

    I1,I3 -- 1st diagonal pair of images (offset 180 deg).
    I2,I4 -- 2nd diagonal pair of images (offset 180 deg).

    Implements algorithm shown in Fig 2 of
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.
    '''

    # Get direct geometric solution for demoduled M for all pixels
    Id = get_complex_cross_point(I1,I2,I3,I4)

    # Get maximum pixel magnitudes for all input images
    I_max_mag = get_max_magnitudes(I1,I2,I3,I4)

    # Compute complex sum
    CS = complex_sum(I1,I2,I3,I4)

    # For each pixel, if the magnitude if greater than the maximum magnitude of
    # all four input images, then replace the pixel with the CS solution.  This
    # step regularizes the direct solution and effectively removes all
    # singularities
    mask = np.abs(Id) > I_max_mag
    Id[mask] = CS[mask]

    # Find weighted sums of image pairs (I1,I3) and (I2,I4)
    Iw13 = compute_Iw(I1,I3,Id)
    Iw24 = compute_Iw(I2,I4,Id)

    # Final result is found by averaging the two linear solutions for reduced
    # noise
    I = (Iw13 + Iw24)/2
    return(I)

def compute_Iw(I0,I1,Id,patch_size=(5,5),mode='constant'):
    '''Computes weighted sum of image pair (I0,I1).

    I0 -- 1st of pair of diagonal images (relative phase cycle of 0).
    I1 -- 2nd of pair of diagonal images (relative phase cycle of 180 deg).
    Id -- result of regularized direct solution.
    patch_size -- size of patches in pixels (x,y).
    mode -- mode of numpy.pad. Probably choose 'constant' or 'edge'.

    Image pair (I0,I1) are phase cycled bSSFP images that are different by
    180 degrees.  Id is the image given by the direct method (Equation [13])
    after regularization by the complex sum.  This function solves for the
    weights by regional differential energy minimization.  The 'regional'
    part means that the image is split into patches of size patch_size with
    edge boundary conditions (pads with the edge values given by mode option).
    The weighted sum of the image pair is returned.

    This function implements Equations [14,18], or steps 4--5 from Fig. 2 in
        Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
        bSSFP imaging with an elliptical signal model." Magnetic resonance in
        medicine 71.3 (2014): 927-933.
    '''

    # Expressions for the numerator and denominator
    numerator = np.conj(I1 - Id)*(I1 - I0) + np.conj(I1 - I0)*(I1 - Id)
    den = np.conj(I0 - I1)*(I0 - I1)

    # Pad the image so we can generate patches where we need them
    edge_pad = [ int(p/2) for p in patch_size ]
    numerator = np.pad(numerator,pad_width=edge_pad,mode=mode)
    den = np.pad(den,pad_width=edge_pad,mode=mode)

    # Separate out into patches of size patch_size
    numerator_patches = view_as_windows(numerator,patch_size)
    den_patches = view_as_windows(den,patch_size)
    numerator_weights = np.sum(numerator_patches,axis=(-2,-1))
    den_weights = np.sum(den_patches,axis=(-2,-1))

    # Equation [18]
    weights = numerator_weights/(2*den_weights)

    # Find Iw, the weighted sum of image pair (I0,I1), equation [14]
    Iw = I0*weights + I1*(1 - weights)
    return(Iw)

if __name__ == '__main__':
    pass
