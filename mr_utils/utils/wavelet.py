import pywt
import numpy as np
from sklearn.utils.extmath import cartesian

def cdf97_2d_forward(x,level):
    '''Forward 2D Cohen–Daubechies–Feauveau 9/7 wavelet.

    x -- 2D signal.
    level -- Decomposition level.

    Returns transform, same shape as input, with locations.  Locations is a
    list of indices instructing cdf97_2d_inverse where the coefficients for
    each block are located.

    Biorthogonal 4/4 is the same as CDF 9/7 according to wikipedia:
        see https://en.wikipedia.org/wiki/Cohen%E2%80%93Daubechies%E2%80%93Feauveau_wavelet#Numbering
    '''

    # periodization seems to be the only way to get shapes to line up.
    cdf97 = pywt.wavedec2(x,wavelet='bior4.4',mode='periodization',level=level)
    wavelet_transform = np.zeros(x.shape,dtype=x.dtype)

    # Initialize
    cVy = 0
    cHx = 0
    locations = []

    ## Strategy:
    #                             -------------------
    #                             |        |        |
    #                             | cA(LL) | cH(LH) |
    #                             |        |        |
    # (cA, (cH, cV, cD))  <--->   -------------------
    #                             |        |        |
    #                             | cV(HL) | cD(HH) |
    #                             |        |        |
    #                             -------------------

    # Start top left
    cA5 = cdf97[0]
    xx,yy = cA5.shape[:]
    wavelet_transform[:xx,:yy] = cA5
    cHx += xx
    cVy += yy
    # locations.append(cartesian((np.arange(xx),np.arange(yy))))
    locations.append(((0,xx),(0,yy)))

    # Iterate over tuples (cHi,cVi,cDi)
    for ii in range(1,len(cdf97)):

        locations.append([])

        # cA is already in place, move on to cH
        xx,yy = cdf97[ii][0].shape[:]
        wavelet_transform[cHx:cHx+xx,:yy] = cdf97[ii][0]
        # locations[-1].append(cartesian((np.arange(cHx,cHx+xx),np.arange(yy))))
        locations[-1].append(((cHx,cHx+xx),(0,yy)))

        # Now get cV
        xx,yy = cdf97[ii][1].shape[:]
        wavelet_transform[:xx,cVy:cVy+yy] = cdf97[ii][1]
        # locations[-1].append(cartesian((np.arange(xx),np.arange(cVy,cVy+yy))))
        locations[-1].append(((0,xx),(cVy,cVy+yy)))

        # Fill in cD
        xx,yy = cdf97[ii][2].shape[:]
        wavelet_transform[cHx:cHx+xx,cVy:cVy+yy] = cdf97[ii][2]
        # locations[-1].append(cartesian((np.arange(cHx,cHx+xx),np.arange(cVy,cVy+yy))))
        locations[-1].append(((cHx,cHx+xx),(cVy,cVy+yy)))

        # Update indices
        cHx += xx
        cVy += yy

    return(wavelet_transform,locations)


def cdf97_2d_inverse(coeffs,locations):
    '''Inverse 2D Cohen–Daubechies–Feauveau 9/7 wavelet.

    coeffs,locations -- Output of cdf97_2d_forward().
    '''

    # Split coefficients out into coefficient list
    coeff_list = []
    xx,yy = locations[0]
    coeff_list.append(coeffs[xx[0]:xx[1],yy[0]:yy[1]])

    for ii in range(1,len(locations)):

        xx,yy = locations[ii][0]
        cHi = coeffs[xx[0]:xx[1],yy[0]:yy[1]]

        xx,yy = locations[ii][1]
        cVi = coeffs[xx[0]:xx[1],yy[0]:yy[1]]

        xx,yy = locations[ii][2]
        cDi = coeffs[xx[0]:xx[1],yy[0]:yy[1]]


        coeff_list.append((cHi,cVi,cDi))

    return(pywt.waverec2(coeff_list,wavelet='bior4.4',mode='periodization'))

if __name__ == '__main__':
    pass
