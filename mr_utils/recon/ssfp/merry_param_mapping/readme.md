
## mr_utils.recon.ssfp.merry_param_mapping.elliptical_fit

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/merry_param_mapping/elliptical_fit.py)

```
NAME
    mr_utils.recon.ssfp.merry_param_mapping.elliptical_fit - Calculates residuals for least_squares fit.

FUNCTIONS
    ellipticalfit(Ireal, TR, dphis, offres, M0, alpha, T1, T2)
        ELLIPTICALFIT
        
        Ireal - complex pixel hermtian transposed
        TE - echo time
        TR - repetition time
        M0 - estmated from the band reduction algorithm
        phasecycles- phase cycle angles
        offres- offresonance profile
        output- J: real part of difference, imaginary part of the difference
        g gradients


```


## mr_utils.recon.ssfp.merry_param_mapping.optimize

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/merry_param_mapping/optimize.py)

```
NAME
    mr_utils.recon.ssfp.merry_param_mapping.optimize - Objective function wrapper used with MATLAB, unnecessary.

FUNCTIONS
    optimize(I, TR, phasecycles, offres, M0, alpha, T1, T2)
        Using a nested function approach because fmincon requires obj and con
        to be separate functions, but usually we compute them simultaneously.
        We want to avoid redundant calculations to we will save the x we
        used to compute obj(x) and if con(x) is the same locaiton we will
        just use the value without recalling our function.


```


## mr_utils.recon.ssfp.merry_param_mapping.plot_ellipse

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/merry_param_mapping/plot_ellipse.py)

```
NAME
    mr_utils.recon.ssfp.merry_param_mapping.plot_ellipse - Plot an ellipse based on MR parameters.

FUNCTIONS
    plotEllipse(T1, T2, TR, alpha, offres, M0, dphi)
        dphi=1 means use fixed linspace for dphi set, else, use the list of dphis
        provided.


```


## mr_utils.recon.ssfp.merry_param_mapping.ssfp_fit

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/merry_param_mapping/ssfp_fit.py)

```
NAME
    mr_utils.recon.ssfp.merry_param_mapping.ssfp_fit - Python port of SSFPfit.

FUNCTIONS
    SSFPfit(T1, T2, TR, TE, alpha, dphi, offres, M0)
        This function will use the steady state signal given in the paper by
        Xiang, Qing-San and Hoff, Michael N. "Banding Artifact Removal for bSSFP
        Imaging with an Elliptical Signal Model", 2014, to simulate SSFP.


```


## mr_utils.recon.ssfp.merry_param_mapping.taylor_method

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/merry_param_mapping/taylor_method.py)

```
NAME
    mr_utils.recon.ssfp.merry_param_mapping.taylor_method - Python port of Merry's bSSFP parameter mapping code.

DESCRIPTION
    This is an alternative to PLANET.

FUNCTIONS
    optim_wrapper(idx, Is, TR, dphis, offres_est, alpha)
        Wrapper for parallelization.
    
    taylor_method(Is, dphis, alpha, TR, mask=None, chunksize=10, disp=False)
        Parameter mapping for multiple phase-cycled bSSFP.
        
        Is -- List of phase-cycled images.
        dphis -- Phase-cycles (in radians).
        alpha -- Flip angle map (in Hz).
        TR -- Repetition time (milliseconds).
        mask -- Locations to compute map estimates.
        chunksize -- Chunk size to use for parallelized loop.
        disp -- Show debugging plots.
        
        mask=None computes maps for all points.  Note that `Is` must be given as a
        list.


```

