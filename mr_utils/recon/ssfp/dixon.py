import numpy as np

def dixon_2pt(IP,OP):
    '''Two point Dixon method of fat/water separation.

    IP -- In-phase image (corresponding to 0).
    OP -- Out-of-phase image (corresponding to \pi).

    Returns water image, W, and fat image, F.

    Implements method described in:
        Dixon, W. T. (1984). Simple proton spectroscopic imaging. Radiology,
        153(1), 189-194.
    '''

    W = (IP + OP)/2
    F = (IP - OP)/2
    return(W,F)

def dixon_3pt(IP,OP1,OP2):
    '''Three point Dixon method of fat/water separation.

    IP -- In-phase image (corresponding to 0).
    OP1 -- Out-of-phase image (corresponding to \pi).
    OP2 -- Out-of-phase image (corresponding to -\pi).

    Returns water image, W, fat image, F, and B0 image.

    Implements method described in:
        Glover, G. H., & Schneider, E. (1991). Three‐point Dixon technique for
        true water/fat decomposition with B0 inhomogeneity correction. Magnetic
        resonance in medicine, 18(2), 371-383.
    '''

    phi = np.angle(np.conj(IP)*OP2)/2
    W = (IP + OP*np.exp(-1j*phi))/2
    F = (IP - OP*np.exp(-1j*phi))/2
    return(W,F)
