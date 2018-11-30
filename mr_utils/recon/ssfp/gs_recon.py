import numpy as np
from mr_utils import view
from mr_utils.sim.ssfp import get_complex_cross_point
import warnings # We know skimage will complain about itself importing imp...
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=DeprecationWarning)
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
    CS = (I1 + I2 + I3 + I4)/4
    return(CS)

def gs_recon3d(I1,I2,I3,I4,slice_axis=-1,isophase=np.pi):
    '''Full 3D Geometric Solution method following Xiang and Hoff's 2014 paper.

    I1--I4 -- Phase-cycled images.
    slice_axis -- Slice dimension, default is the last dimension.
    For more info, see mr_utils.recon.ssfp.gs_recon.
    '''

    num_slices = np.array([ I1.shape[slice_axis],I2.shape[slice_axis],I3.shape[slice_axis],I4.shape[slice_axis] ])
    assert np.allclose(num_slices,np.ones(num_slices.shape)*num_slices[0]),'All images must have the same number of slices!'
    num_slices = num_slices[0]

    # Move the slice dimension to the end
    I1 = np.moveaxis(I1,slice_axis,-1)
    I2 = np.moveaxis(I2,slice_axis,-1)
    I3 = np.moveaxis(I3,slice_axis,-1)
    I4 = np.moveaxis(I4,slice_axis,-1)

    # Run gs_recon for each slice
    recon = np.zeros(I1.shape,dtype='complex')
    for slice in range(num_slices):
        recon[...,slice] = gs_recon(I1[...,slice],I2[...,slice],I3[...,slice],I4[...,slice],isophase=isophase)
    return(recon)

def gs_recon(I1,I2,I3,I4,isophase=np.pi):
    '''Full 2D Geometric Solution method following Xiang and Hoff's 2014 paper.

    I1,I3 -- 1st diagonal pair of images (offset 180 deg).
    I2,I4 -- 2nd diagonal pair of images (offset 180 deg).
    isophase -- Only neighbours with isophase max phase difference contribute.

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
    Iw13 = compute_Iw(I1,I3,Id,isophase=isophase)
    Iw24 = compute_Iw(I2,I4,Id,isophase=isophase)

    # Final result is found by averaging the two linear solutions for reduced
    # noise
    I = (Iw13 + Iw24)/2
    return(I)

def mask_isophase(numerator_patches,patch_size,isophase):
    '''Generate mask that chooses patch pixels that satisfy isophase.

    numerator_patches -- Numerator patches from second pass solution.
    patch_size -- size of patches in pixels (x,y).
    isophase -- Only neighbours with isophase max phase difference contribute.

    Output mask, same size as numerator_patches, to be applied to
    numerator_patches and den_patches before summation.
    '''

    # # Loop through each patch and zero out all the values not
    # mask = np.ones(num_patches.shape).astype(bool)
    # center_x,center_y = int(patch_size[0]/2),int(patch_size[1]/2)
    # for ii in range(mask.shape[0]):
    #     for jj in range(mask.shape[1]):
    #         mask[ii,jj,...] = np.abs(np.angle(num_patches[ii,jj,...])*np.conj(num_patches[ii,jj,center_x,center_y])) < isophase
    # # print(np.sum(mask == False))

    # Now try it without loops - it'll be faster...
    center_x,center_y = [ int(p/2) for p in patch_size ]
    ref_pixels = np.repeat(np.repeat(numerator_patches[:,:,center_x,center_y,None],patch_size[0],axis=-1)[...,None],patch_size[1],axis=-1)
    mask_mat = np.abs(np.angle(numerator_patches)*np.conj(ref_pixels)) < isophase
    # assert np.allclose(mask_mat,mask)

    return(mask_mat)


def compute_Iw(I0,I1,Id,patch_size=(5,5),mode='constant',isophase=np.pi):
    '''Computes weighted sum of image pair (I0,I1).

    I0 -- 1st of pair of diagonal images (relative phase cycle of 0).
    I1 -- 2nd of pair of diagonal images (relative phase cycle of 180 deg).
    Id -- result of regularized direct solution.
    patch_size -- size of patches in pixels (x,y).
    mode -- mode of numpy.pad. Probably choose 'constant' or 'edge'.
    isophase -- Only neighbours with max phase difference isophase contribute.

    Image pair (I0,I1) are phase cycled bSSFP images that are different by
    180 degrees.  Id is the image given by the direct method (Equation [13])
    after regularization by the complex sum.  This function solves for the
    weights by regional differential energy minimization.  The 'regional'
    part means that the image is split into patches of size patch_size with
    edge boundary conditions (pads with the edge values given by mode option).
    The weighted sum of the image pair is returned.

    The isophase does not appear in the paper, but appears in Hoff's MATLAB
    code.  It appears that we only want to consider pixels in the patch that
    have similar tissue properties - in other words, have similar phase.  The
    default isophase is pi as in Hoff's implementation.

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

    # Make sure the phase difference is below a certan bound to include point
    # in weights
    mask = mask_isophase(numerator_patches,patch_size,isophase)
    numerator_patches *= mask
    den_patches *= mask

    numerator_weights = np.sum(numerator_patches,axis=(-2,-1))
    den_weights = np.sum(den_patches,axis=(-2,-1))

    # Equation [18]
    weights = numerator_weights/(2*den_weights + np.finfo(float).eps)

    # Find Iw, the weighted sum of image pair (I0,I1), equation [14]
    Iw = I0*weights + I1*(1 - weights)
    return(Iw)

if __name__ == '__main__':
    pass
