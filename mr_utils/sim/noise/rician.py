'''Noise simulations.'''

import numpy as np

def rician(M, A, sigma):
    '''Generates rician distribution of pixel intensity M.

    Generates the noise distribution of a magnitude MR image.

    Parameters
    ==========
    M : array_like
        measured image pixel intensity
    A : array_like
        image pixel intensity in the absence of noise
    sigma : float
        standard deviation of the Gaussian noise in the real and the
        imaginary images (which we assume to be equal)

    Returns
    =======
    pM : array_like
        computed probability distribution of M

    Notes
    =====
    Computes Equation [1] from [1]_.

    References
    ==========
    .. [1] Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of
           noisy MRI data." Magnetic resonance in medicine 34.6 (1995):
           910-914.
    '''

    sigma2 = sigma*sigma
    pM = M/sigma2*np.exp(-(M*M + A*A)/(2*sigma2))*np.i0(A*M/sigma2)
    return pM

if __name__ == '__main__':
    pass
