'''Wrappers for PyWavelets.'''

import warnings

import pywt
import numpy as np

def combine_chunks(wvlt, shape, dtype=float):
    '''Stitch together the output of PyWavelets wavedec2.

    Parameters
    ==========
    wvlt : array_like
        Output of pywt.wavedec2().
    shape : tuple
        Desired shape.
    dtype : np.dtype
        Type of numpy array.

    Notes
    =====

    .. code-block:: none
    
        We have tuples that look like this:
                                    -------------------
                                    |        |        |
                                    | cA(LL) | cH(LH) |
                                    |        |        |
        (cA, (cH, cV, cD))  <--->   -------------------
                                    |        |        |
                                    | cV(HL) | cD(HH) |
                                    |        |        |
                                    -------------------
    '''

    # Initialize
    wavelet_transform = np.zeros(shape, dtype=dtype)
    cVy = 0
    cHx = 0
    locations = []

    # Start top left
    cA5 = wvlt[0]
    xx, yy = cA5.shape[:]
    wavelet_transform[:xx, :yy] = cA5
    cHx += xx
    cVy += yy
    # locations.append(cartesian((np.arange(xx),np.arange(yy))))
    locations.append(((0, xx), (0, yy)))

    # Iterate over tuples (cHi,cVi,cDi)
    for ii in range(1, len(wvlt)):

        locations.append([])

        # cA is already in place, move on to cH
        xx, yy = wvlt[ii][0].shape[:]
        wavelet_transform[cHx:cHx+xx, :yy] = wvlt[ii][0]
        #locations[-1].append(cartesian((np.arange(cHx,cHx+xx),np.arange(yy))))
        locations[-1].append(((cHx, cHx+xx), (0, yy)))

        # Now get cV
        xx, yy = wvlt[ii][1].shape[:]
        wavelet_transform[:xx, cVy:cVy+yy] = wvlt[ii][1]
        #locations[-1].append(cartesian((np.arange(xx),np.arange(cVy,cVy+yy))))
        locations[-1].append(((0, xx), (cVy, cVy+yy)))

        # Fill in cD
        xx, yy = wvlt[ii][2].shape[:]
        wavelet_transform[cHx:cHx+xx, cVy:cVy+yy] = wvlt[ii][2]
        locations[-1].append(((cHx, cHx+xx), (cVy, cVy+yy)))

        # Update indices
        cHx += xx
        cVy += yy

    return(wavelet_transform, locations)

def split_chunks(coeffs, locations):
    '''Separate the stitched together transform into blocks again.

    x -- Stitched together wavelet transform.
    locations -- Indices where the coefficients for each block are located.

    x, locations are the output of combine_chunks().
    '''

    # Split coefficients out into coefficient list
    coeff_list = []
    xx, yy = locations[0]
    coeff_list.append(coeffs[xx[0]:xx[1], yy[0]:yy[1]])

    for ii in range(1, len(locations)):

        xx, yy = locations[ii][0]
        cHi = coeffs[xx[0]:xx[1], yy[0]:yy[1]]

        xx, yy = locations[ii][1]
        cVi = coeffs[xx[0]:xx[1], yy[0]:yy[1]]

        xx, yy = locations[ii][2]
        cDi = coeffs[xx[0]:xx[1], yy[0]:yy[1]]


        coeff_list.append((cHi, cVi, cDi))

    return coeff_list

def wavelet_forward(x, wavelet, mode='symmetric', level=None, axes=(-2, -1)):
    '''Wrapper for the multilevel 2D discrete wavelet transform.

    x -- Input data.
    wavelet -- Wavelet to use.
    mode -- Signal extension mode.
    level -- Decomposition level (must be >= 0).
    axes -- Axes over which to compute the DWT.

    See PyWavelets documentation on pywt.wavedec2() for more information.

    If level=None (default) then it will be calculated using the dwt_max_level
    function.
    '''

    # Make sure we don't go too deep
    max_level = pywt.dwtn_max_level(x.shape, wavelet)
    if level is not None and level > max_level:
        msg = 'Level %d cannot be achieved, using max level=%d!' \
            % (level, max_level)
        warnings.warn(msg)
        level = max_level

    # Do the pywavelets thing
    wvlt = pywt.wavedec2(x, wavelet, mode, level, axes)

    # But wvlt is a bunch of tuples, and we want them all stitched together:
    return combine_chunks(wvlt, x.shape, x.dtype)

def wavelet_inverse(
        coeffs, locations, wavelet, mode='symmetric', axes=(-2, -1)):
    '''Wrapper for the multilevel 2D inverse discrete wavelet transform.

    coeffs -- Combined coefficients.
    locations -- Indices where the coefficients for each block are located.
    wavelet -- Wavelet to use.
    mode -- Signal extension mode.
    axes -- Axes over which to compute the IDWT.

    coeffs, locations are the output of forward().
    '''

    # Split coefficients out into coefficient list
    coeff_list = split_chunks(coeffs, locations)
    return pywt.waverec2(coeff_list, wavelet, mode, axes)


def cdf97_2d_forward(x, level):
    '''Forward 2D Cohen–Daubechies–Feauveau 9/7 wavelet.

    x -- 2D signal.
    level -- Decomposition level.

    Returns transform, same shape as input, with locations.  Locations is a
    list of indices instructing cdf97_2d_inverse where the coefficients for
    each block are located.

    Biorthogonal 4/4 is the same as CDF 9/7 according to wikipedia:
        see https://en.wikipedia.org/wiki/
            Cohen%E2%80%93Daubechies%E2%80%93Feauveau_wavelet#Numbering
    '''

    # Make sure we don't go too deep
    max_level = pywt.dwtn_max_level(x.shape, 'bior4.4')
    if level > max_level:
        msg = 'Level %d cannot be achieved, using max level=%d!' \
            % (level, max_level)
        warnings.warn(msg)
        level = max_level

    # periodization seems to be the only way to get shapes to line up.
    cdf97 = pywt.wavedec2(
        x, wavelet='bior4.4', mode='periodization', level=level)

    # Now throw all the chuncks together
    return combine_chunks(cdf97, x.shape, x.dtype)


def cdf97_2d_inverse(coeffs, locations):
    '''Inverse 2D Cohen–Daubechies–Feauveau 9/7 wavelet.

    coeffs,locations -- Output of cdf97_2d_forward().
    '''

    # Split coefficients out into coefficient list
    coeff_list = split_chunks(coeffs, locations)

    return pywt.waverec2(coeff_list, wavelet='bior4.4', mode='periodization')

if __name__ == '__main__':
    pass
