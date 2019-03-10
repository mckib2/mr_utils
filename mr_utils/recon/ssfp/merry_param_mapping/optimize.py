'''Objective function wrapper used with MATLAB, unnecessary.'''

from scipy.optimize import least_squares

from mr_utils.recon.ssfp.merry_param_mapping.elliptical_fit \
    import ellipticalfit

def optimize(I, TR, phasecycles, offres, M0, alpha, T1, T2):
    '''Using a nested function approach because fmincon requires obj and con
    to be separate functions, but usually we compute them simultaneously.
    We want to avoid redundant calculations to we will save the x we
    used to compute obj(x) and if con(x) is the same locaiton we will
    just use the value without recalling our function.
    '''

    # -------- starting point and bounds --------------
    ub = [30, 50, 1.999, 10] # T1, T2, off resonance 100, alpha in radians, M0
    lb = [1, 1, 0, 0] # alpha-alpha*.2]; %T1, T2, off resonance 0 Hz, alpha, M0
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
    res = least_squares(obj, x0, bounds=bounds)
    return(res['x'], res['cost'])
