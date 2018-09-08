# Python port of Gadgetron's 2D partial_fourier_POCS
import numpy as np

ISMRMRD_FILTER_GAUSSIAN = 0
ISMRMRD_FILTER_HANNING = 1
ISMRMRD_FILTER_TAPERED_HANNING =2
ISMRMRD_FILTER_NONE = 3

def compute_2d_filter(fx,fy):

    RO = fx.shape[0]
    E1 = fy.shape[0]

    fxy = np.zeros((RO,E1))
    for yy in range(E1):
        for xx in range(RO):
            fxy[yy,xx] = fx[xx]*fy[yy]
    return(fxy)

def apply_kspace_filter_ROE1(data,FRO,FE1):

    # Make sure we can do the thing
    assert(data.shape[0] == FRO.shape[0])
    assert(data.shape[1] == FE1.shape[0])

    # Make the filter
    FROE1 = compute_2d_filter(FRO,FE1)

    # Filter
    dataFiltered = data*FROE1
    return(dataFiltered)


def generate_symmetric_filter(
    length,
    filterType,
    sigma=1.5,
    width=15):

    # Don't make a useless filter
    assert(length != 0)
    length = int(length)

    # preallocate
    filter = np.zeros(length)

    if ((width == 0) or (width >= length)):
        width = 1

    if (filterType == ISMRMRD_FILTER_GAUSSIAN):
        r = -1.0*sigma*sigma/2

        if (np.mod(length,2) == 0):
            # to make sure the zero points match and boundary of filters are symmetric
            stepSize = 2.0/(length - 2)
            for ii in range(length-1):
                x = -1 + ii*stepSize
                filter[ii + 1] = np.exp(r*(x*x))
        else:
            stepSize = 2.0/(length - 1)
            for ii in range(length):
                x = -1 + ii*stepSize
                filter[ii] = np.exp(r*(x*x))

    elif (filterType == ISMRMRD_FILTER_TAPERED_HANNING):
        w = np.zeros(width)

        for ii in range(1,width):
            w[ii - 1] = (0.5 * (1 - np.cos(2.0*np.pi*ii / (2 * width + 1))))

        # make sure the center of the filter will end up being 1:
        filter[:] = 1

        if (np.mod(length,2) == 0):
            for ii in range(1,width):
                filter[ii] = w[ii - 1]
                filter[length - ii] = filter[ii]

            filter[0] = 0

        else:
            for ii in range(1,width):
                filter[ii - 1] = w[ii - 1]
                filter[length - ii] = filter[ii - 1]

    elif (filterType == ISMRMRD_FILTER_HANNING):

        if (np.mod(length,2) == 0):

            N = length - 1
            halfLen = int((N + 1)/2)
            for ii in range(1,halfLen):
                filter[ii] = (0.5 * (1 - np.cos(2.0*np.pi*ii / (N + 1))))

            for ii in range(halfLen,N):
                filter[ii + 1] = filter[N - ii]

            filter[0] = 0

        else:

            halfLen = int((length + 1)/2)
            for ii in range(1,halfLen):
                filter[ii - 1] = (0.5 * (1 - np.cos(2.0*np.pi*ii / (length + 1))))

            for ii in range(halfLen,length):
                filter[ii] = filter[length - 1 - ii]

    elif (filterType == ISMRMRD_FILTER_NONE):
        filter[:] = 1
    else:
        raise Exception('unrecognized fiter type...')

    sos = 0.0
    for ii in range(length):
        sos += filter[ii]*filter[ii]

    r = 1.0 / np.sqrt(np.abs(sos) / (length))
    for ii in range(length):
        filter[ii] *= r

    return(filter)

def generate_symmetric_filter_ref(length,start,end):

    # Check to make sure the input is reasonable
    assert(length >= 2)
    assert((start >= 0) and (end <= length - 1) and (start <= end))

    if ((start == 0) and (end == length - 1)):
        filter = generate_symmetric_filter(length,ISMRMRD_FILTER_HANNING)
        return(filter)

    centerInd = length/2

    lenFilter = 0 # make a symmetric filter with zero at the center
    lenFilterEnd = 2*(end - centerInd) + 1
    lenFilterStart = 2*(centerInd - start) + 1

    if ((start == 0) and (end < length - 1)):
        lenFilter = lenFilterEnd
    elif ((start > 0) and (end == length - 1)):
        lenFilter = lenFilterStart
    elif ((start > 0) and (end < length - 1)):
        if lenFilterStart < lenFilterEnd:
            lenFilter = lenFilterStart
        else:
            lenFilter = lenFilterEnd
    else:
        raise Exception('invalid inputs...')

    # Make sure we do in fact have a filter
    assert(lenFilter > 0)

    # Go grab a hanning filter
    filterSym = generate_symmetric_filter(lenFilter,ISMRMRD_FILTER_HANNING)

    # Initialize the filter
    filter = np.zeros(length)

    if ((start == 0) and (end < length - 1)):
        start_ = end - lenFilter + 1
        filter[start_:start_+len(filterSym)] = filterSym
        return(filter)
    elif ((start > 0) and (end == length - 1)):
        filter[start:start+len(filterSym)] = filterSym
        return(filter)
    elif ((start > 0) and (end < length - 1)):
        if (lenFilter == lenFilterStart):
            filter[start:start+len(filterSym)] = filterSym
        else:
            start_ = end - lenFilter + 1
            filter[start_:start_+len(filterSym)] = filterSym
        return(filter)
    else:
        raise Exception('invalid inputs : start - end - length')

# kspace: input kspace [RO E1 E2 ...]
# 2D POCS is performed
# startRO, endRO, startE1, endE1: acquired kspace range
# transit_band_RO/E1: transition band width in pixel for RO/E1
# iter: number of maximal iterations for POCS
# thres: iteration threshold
def partial_fourier_pocs(
    kspace,
    startRO,endRO,
    startE1,endE1,
    transit_band_RO=0,
    transit_band_E1=0,
    iter=10,
    thres=0.01):

    # Get Readout and Encoding sizes
    RO,E1 = kspace.shape[:]

    # Start with initial kspace
    res = kspace.copy()

    # Make sure startRO,endRO are reasonable
    assert(startRO < RO)
    assert(endRO <= RO)
    assert(startRO < endRO)

    # Make sure startE1,endE1 are reasonable
    assert(startE1 < E1)
    assert(endE1 <= E1)
    assert(startE1 < endE1)

    # Make sure there is some partial fourier happening here
    assert((endRO - startRO + 1 != RO) or (endE1 - startE1 + 1 != E1))

    # create kspace filters for homodyne phase estimation
    filterRO = generate_symmetric_filter_ref(RO,startRO,endRO)
    filterE1 = generate_symmetric_filter_ref(E1,startE1,endE1)

    kspaceIter = kspace.copy()
    # magnitude of complex images
    mag = np.zeros(kspace.shape)
    magComplex = np.zeros(kspace.shape)

    # kspace filter
    buffer_partial_fourier = kspaceIter.copy()
    buffer = kspaceIter.copy()

    # Gadgetron::apply_kspace_filter_ROE1(kspaceIter,filterRO,filterE1,buffer_partial_fourier)
    buffer_partial_fourier = apply_kspace_filter_ROE1(kspaceIter,filterRO,filterE1)

    # go to image domain
    # Gadgetron::hoNDFFT<typename realType<T>::Type>::instance()->ifft2c(buffer_partial_fourier);
    buffer_partial_fourier = np.fft.ifft2(buffer_partial_fourier)

    # get the complex image phase for the filtered kspace
    # Gadgetron::addEpsilon(mag);
    mag = np.abs(buffer_partial_fourier) + np.finfo(float).eps
    magComplex = mag.copy()
    # Gadgetron::divide(buffer_partial_fourier, magComplex, buffer);
    buffer = buffer_partial_fourier/magComplex

    # complex images, initialized as not filtered complex image
    complexIm = kspaceIter.copy()

    # Gadgetron::hoNDFFT<typename realType<T>::Type>::instance()->ifft2c(kspaceIter, complexIm);
    complexIm = np.fft.ifft2(kspaceIter)

    # hoNDArray<T> complexImPOCS(complexIm);
    complexImPOCS = complexIm.copy()

    # the kspace during iteration is buffered here
    # hoNDArray<T> buffer_partial_fourier_Iter(kspaceIter);
    buffer_partial_fourier_Iter = kspaceIter.copy()

    for ii in range(iter):
        mag = np.abs(complexImPOCS) #Gadgetron::abs(complexImPOCS, mag);
        magComplex = mag.copy() #magComplex.copyFrom(mag);
        complexImPOCS = magComplex*buffer #Gadgetron::multiply(magComplex, buffer, complexImPOCS);

        # go back to kspace
        # Gadgetron::hoNDFFT<typename realType<T>::Type>::instance()->fft2c(complexImPOCS, kspaceIter);
        kspaceIter = np.fft.fft2(complexImPOCS)

        # buffer kspace during iteration
        buffer_partial_fourier_Iter = kspaceIter

        # restore the acquired region
        kspaceIter = partial_fourier_reset_kspace(kspace,kspaceIter,startRO,endRO,startE1,endE1)

        # update complex image
        # Gadgetron::hoNDFFT<typename realType<T>::Type>::instance()->ifft2c(kspaceIter, complexImPOCS);
        complexImPOCS =np.fft.ifft2(kspaceIter)

        # compute threshold to stop the iteration
        # Gadgetron::subtract(complexImPOCS, complexIm, buffer_partial_fourier);
        buffer_partial_fourier = complexImPOCS - complexIm
        # auto prev = Gadgetron::nrm2(complexIm);
        prev = np.linalg.norm(complexIm)
        # auto diff = Gadgetron::nrm2(buffer_partial_fourier);
        diff = np.linalg.norm(buffer_partial_fourier)

        t = diff / prev
        if (t < thres):
            print('Reached Threshold!')
            break

        complexIm = complexImPOCS

    if ((transit_band_RO == 0) and (transit_band_E1 == 0)):
        res = kspaceIter
    else:
        raise Exception('partial_fourier_transition_band NOT IMPLEMENTED')
    #     Gadgetron::partial_fourier_transition_band(kspace, buffer_partial_fourier_Iter, startRO, endRO, startE1, endE1, startE2, endE2, transit_band_RO, transit_band_E1, transit_band_E2);
    #     res = buffer_partial_fourier_Iter

    # Somehow the image gets flipped around...Need to find where this happens
    res = np.flipud(np.fliplr(res))
    return(res)

def partial_fourier_reset_kspace(src,dst,startRO,endRO,startE1,endE1):

    # For some reason we check that we have enough dimensions
    assert(src.ndim >= 2)

    RO,E1 = dst.shape[:]
    RO_src,E1_src = src.shape[:]

    # Some more redundant checking
    assert(RO == RO_src)
    assert(E1 == E1_src)
    assert(src.size == dst.size)

    #  Enforce data consistency
    dst[startRO:endRO:,startE1:endE1:] = src[startRO:endRO:,startE1:endE1:]

    return(dst)

if __name__ == '__main__':
    pass
