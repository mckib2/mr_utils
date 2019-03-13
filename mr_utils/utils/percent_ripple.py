import numpy as np

def percent_ripple(profile):
    '''Calculate percent ripple of the bSSFP spectral profile.

    Parameters
    ==========
    profile : array_like
        The off-resonance profile as a function of theta.

    Returns
    =======
    float
        Measure of ripple level of profile.

    Notes
    =====
    The residual ripple can be predicted by examining the variations in the
    expected signal profile with free-precession angle, theta.

    Implements percent ripple, Equation [11], from [1]_.

    References
    ==========
    .. [1] Bangerter, Neal K., et al. "Analysis of multiple‐acquisition SSFP."
           Magnetic Resonance in Medicine: An Official Journal of the
           International Society for Magnetic Resonance in Medicine 51.5
           (2004): 1038-1047.
    '''

    Smax = np.max(profile)
    Smin = np.min(profile)
    Smean = np.mean(profile)
    return 100*(Smax - Smin)/Smean
