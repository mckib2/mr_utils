
## mr_utils.cs.thresholding.amp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/amp.py)

```
NAME
    mr_utils.cs.thresholding.amp

FUNCTIONS
    amp2d(y, forward_fun, inverse_fun, sigmaType=2, randshift=False, tol=1e-08, x=None, ignore_residual=False, disp=False, maxiter=100)
        Approximate message passing using wavelet sparsifying transform.
        
        y -- Measurements, i.e., y = Ax.
        forward_fun -- A, the forward transformation function.
        inverse_fun -- A^H, the inverse transformation function.
        sigmaType -- Method for determining threshold.
        randshift -- Whether or not to randomly circular shift every iteration.
        tol -- Stop when stopping criteria meets this threshold.
        x -- The true image we are trying to reconstruct.
        ignore_residual -- Whether or not to ignore stopping criteria.
        disp -- Whether or not to display iteration info.
        maxiter -- Maximum number of iterations.
        
        Solves the problem:
            min_x || Wavelet(x) ||_1 s.t. || y - forward_fun(x) ||^2_2 < epsilon^2
        
        If x=None, then MSE will not be calculated.
        
        Reference:
            "Message Passing Algorithms for CS" Donoho et al., PNAS 2009;106:18914
        
        Based on MATLAB implementation found here:
            http://kyungs.bol.ucla.edu/Site/Software.html


```


## mr_utils.cs.thresholding.iht_fourier_encoded_total_variation

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/iht_fourier_encoded_total_variation.py)

```
NAME
    mr_utils.cs.thresholding.iht_fourier_encoded_total_variation

FUNCTIONS
    IHT_FE_TV(kspace, samp, k, mu=1, tol=1e-08, do_reordering=False, x=None, ignore_residual=False, disp=False, maxiter=500)
        IHT for Fourier encoding model and TV constraint.
        
        kspace -- Measured image.
        samp -- Sampling mask.
        k -- Sparsity measure (number of nonzero coefficients expected).
        mu -- Step size.
        tol -- Stop when stopping criteria meets this threshold.
        do_reordering -- Reorder column-stacked true image.
        x -- The true image we are trying to reconstruct.
        ignore_residual -- Whether or not to break out of loop if resid increases.
        disp -- Whether or not to display iteration info.
        maxiter -- Maximum number of iterations.
        
        Solves the problem:
            min_x || kspace - FFT(x) ||^2_2  s.t.  || FD(x) ||_0 <= k
        
        If im_true=None, then MSE will not be calculated.


```


## mr_utils.cs.thresholding.iht_tv

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/iht_tv.py)

```
NAME
    mr_utils.cs.thresholding.iht_tv

FUNCTIONS
    IHT_TV(y, forward_fun, inverse_fun, k, mu=1, tol=1e-08, do_reordering=False, x=None, ignore_residual=False, disp=False, maxiter=500)
        IHT for generic encoding model and TV constraint.
        
        y -- Measured data, i.e., y = Ax.
        forward_fun -- A, the forward transformation function.
        inverse_fun -- A^H, the inverse transformation function.
        k -- Sparsity measure (number of nonzero coefficients expected).
        mu -- Step size.
        tol -- Stop when stopping criteria meets this threshold.
        do_reordering -- Reorder column-stacked true image.
        x -- The true image we are trying to reconstruct.
        ignore_residual -- Whether or not to break out of loop if resid increases.
        disp -- Whether or not to display iteration info.
        maxiter -- Maximum number of iterations.
        
        Solves the problem:
            min_x || y - Ax ||^2_2  s.t.  || FD(x) ||_0 <= k
        
        If x=None, then MSE will not be calculated.


```


## mr_utils.cs.thresholding.iterative_hard_thresholding

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/iterative_hard_thresholding.py)

```
NAME
    mr_utils.cs.thresholding.iterative_hard_thresholding

FUNCTIONS
    IHT(A, y, k, mu=1, maxiter=500, tol=1e-08, x=None, disp=False)
        Iterative hard thresholding algorithm (IHT).
        
        A -- Measurement matrix.
        y -- Measurements (i.e., y = Ax).
        k -- Number of expected nonzero coefficients.
        mu -- Step size.
        maxiter -- Maximum number of iterations.
        tol -- Stopping criteria.
        x -- True signal we are trying to estimate.
        disp -- Whether or not to display iterations.
        
        Solves the problem:
            min_x || y - Ax ||^2_2  s.t.  ||x||_0 <= k
        
        If disp=True, then MSE will be calculated using provided x. mu=1 seems to
        satisfy Theorem 8.4 often, but might need to be adjusted (usually < 1).
        See normalized IHT for adaptive step size.
        
        Implements Algorithm 8.5 from:
            Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
            and applications. Cambridge University Press, 2012.


```


## mr_utils.cs.thresholding.iterative_soft_thresholding

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/iterative_soft_thresholding.py)

```
NAME
    mr_utils.cs.thresholding.iterative_soft_thresholding

FUNCTIONS
    IST(A, y, mu=0.8, theta0=None, k=None, maxiter=500, tol=1e-08, x=None, disp=False)
        Iterative soft thresholding algorithm (IST).
        
        A -- Measurement matrix.
        y -- Measurements (i.e., y = Ax).
        mu -- Step size (theta contraction factor, 0 < mu <= 1).
        theta0 -- Initial threshold, decreased by factor of mu each iteration.
        k -- Number of expected nonzero coefficients.
        maxiter -- Maximum number of iterations.
        tol -- Stopping criteria.
        x -- True signal we are trying to estimate.
        disp -- Whether or not to display iterations.
        
        Solves the problem:
            min_x || y - Ax ||^2_2  s.t.  ||x||_0 <= k
        
        If disp=True, then MSE will be calculated using provided x. If theta0=None,
        the initial threshold of the IHT will be used as the starting theta.
        
        Implements Equations [22-23] from:
            Rani, Meenu, S. B. Dhok, and R. B. Deshmukh. "A systematic review of
            compressive sensing: Concepts, implementations and applications." IEEE
            Access 6 (2018): 4875-4894.


```


## mr_utils.cs.thresholding.normalized_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/normalized_iht.py)

```
NAME
    mr_utils.cs.thresholding.normalized_iht

FUNCTIONS
    nIHT(A, y, k, c=0.1, kappa=None, x=None, maxiter=200, tol=1e-08, disp=False)
        Normalized iterative hard thresholding.
        
        A -- Measurement matrix
        y -- Measurements (i.e., y = Ax)
        k -- Number of nonzero coefficients preserved after thresholding.
        c -- Small, fixed constant. Tunable.
        kappa -- Constant, > 1/(1 - c).
        x -- True signal we want to estimate.
        maxiter -- Maximum number of iterations (of the outer loop).
        tol -- Stopping criteria.
        dip -- Whether or not to display iteration info.
        
        Implements Algorithm 8.6 from:
            Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
            and applications. Cambridge University Press, 2012.


```

