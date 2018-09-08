import numpy as np

def rayleigh(M,sigma):
    '''Generates Rayleigh distribution of pixel intensity M.

    Generates the noise distribution of magnitude MR image areas where only
    noise is present. This distribution governs the noise in image regions with
    no NMR signal.

    M -- measured image pixel intensity
    sigma -- standard deviation of the Gaussian noise in the real and the
             imaginary images (which we assume to be equal)

    pM -- computed probability distribution of M

    Computes Equation [2] from:
    Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
        data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    '''

    sigma2 = sigma*sigma
    pM = M/sigma2*np.exp(-M*M/(2*sigma2))
    return(pM)

def rayleigh_mean(sigma):
    '''Mean of the Rayleigh distribution with standard deviation sigma.

    Computes Equation [3] from:
    Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
        data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    '''

    M_bar = sigma*np.sqrt(np.pi/2)
    return(M_bar)

def rayleigh_variance(sigma):
    '''Variance of the Rayleigh distribution with standard deviation sigma.

    Computes Equation [4] from:
    Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
        data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    '''

    var = (2 - np.pi/2)*sigma**2
    return(var)

if __name__ == '__main__':
    pass
