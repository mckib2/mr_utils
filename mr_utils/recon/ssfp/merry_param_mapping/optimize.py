'''Objective function wrapper used with MATLAB, unnecessary.'''

from scipy.optimize import least_squares

from mr_utils.recon.ssfp.merry_param_mapping.elliptical_fit \
    import ellipticalfit

def optimize(I, TR, phasecycles, offres, M0, alpha, T1, T2):
    '''Optimization driver to find T1, T2, offres, and M0 estimates.

    Parameters
    ==========
    I : list
        List of phase-cycled images.
    TR : float
        Repetition time (in sec).
    phasecycles : array_like
        Phase-cycles (in radians).
    offres : array_like
        Off-resonance map estimation (in Hz).
    M0 : float
        Initial guess for M0.
    alpha : float
        Flip angle (in rad).
    T1 : float
        Inital guess for T1 (in sec).
    T2 : float
        Initial guess for T2 (in sec).

    Returns
    =======
    array_like
        Optimized values for [T1 (sec), T2 (sec), offres (Hz), M0].
    float
        Final objective function value.
    '''

    # -------- starting point and bounds --------------
    ub = [3, .5, 200, 10] # T1, T2, off resonance Hz, alpha in radians, M0
    lb = [.1, .01, 0, 0] # T1, T2, off resonance Hz, alpha, M0
    bounds = (lb, ub)

    # Make sure offres starts within bounds
    if offres > ub[2]:
        offres = ub[2]
    if offres < lb[2]:
        offres = lb[2]

    x0 = [T1, T2, offres, M0] # alpha]; %alpha: +/-20percent
    # alpha shouldn't differ by more than 20% of the original flip angle
    # -------------------------------------------------

    # ---------- Objective Function ------------------
    def obj(x):
        '''Objective function for least squares fitting.'''
        return ellipticalfit(
            I, TR, phasecycles, x[2], x[3], alpha, x[0], x[1])

    # -------------------------------------------------

    # ------------------ optimize --------------------
    # import numpy as np

    # from scipy.optimize import brute
    # robj = lambda x: np.sum(np.abs(obj(x)))
    # res = brute(robj, list(zip(lb, ub)), Ns=3, disp=True)
    # return(res, None)

    # from scipy.optimize import shgo
    # robj = lambda x: np.sum(np.abs(obj(x)))
    # res = shgo(robj, list(zip(lb, ub)))
    # return(res['x'], None)

    # from scipy.optimize import dual_annealing
    # robj = lambda x: np.sum(np.abs(obj(x)))
    # res = dual_annealing(robj, list(zip(lb, ub)))
    # return(res['x'], None)

    res = least_squares(obj, x0, bounds=bounds)
    return(res['x'], res['cost'])
