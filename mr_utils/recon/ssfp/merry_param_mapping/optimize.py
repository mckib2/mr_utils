'''Objective function wrapper used with MATLAB, unnecessary.'''

from scipy.optimize import least_squares

from mr_utils.recon.ssfp.merry_param_mapping.elliptical_fit import ellipticalfit

def optimize(I, TE, TR, phasecycles, offres, M0, alpha, T1, T2):
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

    if offres > ub[2]:
        offres = ub[2]
    if offres < lb[2]:
        offres = lb[2]

    x0 = [T1, T2, offres, M0] # alpha]; %alpha: +/-20percent
    # alpha shouldn't differ by more than 20% of the original flip angle
    # -------------------------------------------------

    # ------ linear constraints -----------------
    # A = [-10, 1, 0, 0]
    # b = [0]
    # Aeq = []
    # beq = []
    # count = 0
    # --------------------------------------

    # ------- common variables ----------
    # these are variables used in both obj and con
    # xcheck = 0*x0
    # c = [];
    # dcdx = [];
    # --------------------------------------
    # dertype='CS';
    # ------------------ optimize --------------------
    # options = optimoptions('lsqnonlin', 'Display', 'iter-detailed')
    #         'Algorithm', 'levenberg-marquardt',...
    #         'ScaleProblem','Jacobian', ...
        # %; only set if making little inital progress
    # %     options = optimset(...
    # %         'Algorithm', 'interior-point', ...  % choose one of: 'interior-point', 'sqp', 'active-set', 'trust-region-reflective'
    # %         'AlwaysHonorConstraints', 'bounds', ...  % forces interior point algorithm to always honor bounds
    # %         'MaxIter', 1000, ...  % maximum number of iterations
    # %         'MaxFunEvals', 10000, ...  % maximum number of function calls
    # %         'TolCon', 1e-6, ...  % convergence tolerance on constraints
    # %         'TolFun', 1e-6, ...  % convergence tolerance on function value
    # %         'GradObj', 'off', ...  % supply gradients of objective
    # %         'GradConstr', 'off');  % display diagnotic information


    # % other potentially useful options.  see documentation for others.
    # %         'FinDiffType', 'forward', ...  % if finite differencing, can also use central
    # %         'DerivativeCheck', 'on', ...  % on if you want to check your supplied gradients against finite differencing
    # %         'Algorithm', 'sqp', ...  % choose one of: 'interior-point', 'sqp', 'active-set', 'trust-region-reflective'
    # %         'AlwaysHonorConstraints', 'bounds', ...  % forces interior point algorithm to always honor bounds
    # %         'display', 'iter-detailed', ...  % display more information
    # %         , ...  % supply gradients of constraints 'Diagnostics', 'on'
    # %    [xopt, fopt, exitflag, output] = fmincon(@obj, x0, A, b, Aeq, beq, lb, ub,[], options);
    # %    [xopt, fopt, residual, exitflag, output] = lsqnonlin(@obj,x0,lb,ub,options);
    # xopt, fopt, residual, exitflag, output = lsqnonlin(@obj, x0, lb, ub, options)

    # ------------------ optimize --------------------

    # ---------- Objective Function ------------------
    def obj(x):
        '''Objective function for least squares fitting.'''
        J = ellipticalfit(
            I, TE, TR, phasecycles, x[2], x[3], alpha, x[0], x[1])
        return J

    # -------------------------------------------------

    res = least_squares(obj, x0, bounds=bounds)
    return(res['x'], res['cost'])
    # return(xopt, fopt, exitflag, output, count)
