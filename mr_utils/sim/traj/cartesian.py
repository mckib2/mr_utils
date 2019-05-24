'''Create sampling patterns for Cartesian k-space trajectories.'''

import numpy as np
from scipy.stats import norm

def cartesian_pe(shape, undersample=.5, sigma=1, reflines=20):
    '''Randomly collect Cartesian phase encodes (lines).

    Parameters
    ----------
    shape : tuple
        Shape of the image to be sampled.
    undersample : float, optional
        Undersampling factor (0 < undersample <= 1).
    sigma : float, optional
        Standard deviation of Gaussian pdf used to undersample.
    reflines : int, optional
        Number of lines in the center to collect regardless.

    Returns
    -------
    mask : array_like
        Boolean mask of sample locations on Cartesian grid.

    Raises
    ------
    AssertionError
        If undersample factor is outside of interval (0, 1].
    '''

    assert 0 < undersample <= 1, (
        'Undersampling factor must be in (0,1]!')

    M, _N = shape[:]
    k = int(undersample*M)
    # idx = np.random.permutation(M)[:k]
    xx = np.linspace(norm.ppf(0.01), norm.ppf(0.99), M)
    p = norm.pdf(xx, scale=sigma)
    p /= np.sum(p)
    idx = np.random.choice(
        np.arange(M, dtype=int), k, replace=False, p=p)

    mask = np.zeros(shape)*False
    mask[idx, :] = True

    # Make sure we grab center of kspace regardless
    mask[int(M/2-reflines/2):int(M/2+reflines/2), :] = True

    return mask

def cartesian_gaussian(shape, undersample=(.5, .5), reflines=20):
    '''Undersample in Gaussian pattern.

    Parameters
    ----------
    shape : tuple
        Shape of the image to be sampled.
    undersample : tuple, optional
        Undersampling factor in x and y (0 < ux, uy <= 1).
    reflines : int, optional
        Number of lines in the center to collect regardless.

    Returns
    -------
    mask : array_like
        Boolean mask of sample locations on Cartesian grid.

    Raises
    ------
    AssertionError
        If undersample factors are outside of interval (0, 1].
    '''

    assert 0 < undersample[0] <= 1 and 0 < undersample[1] <= 1, \
        'Undersampling factor must be in (0,1]!'

    M, N = shape[:]
    km = int(undersample[0]*M)
    kn = int(undersample[1]*N)

    mask = np.zeros(N*M).astype(bool)
    idx = np.arange(mask.size)
    np.random.shuffle(idx)
    mask[idx[:km*kn]] = True
    mask = mask.reshape(shape)

    # Make sure we grab the reference lines in center of kspace
    mask[int(M/2-reflines/2):int(M/2+reflines/2), :] = True

    return mask
