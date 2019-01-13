
# CS
## mr_utils.cs.convex.gd_fourier_encoded_tv

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/convex/gd_fourier_encoded_tv.py)

```
NAME
    mr_utils.cs.convex.gd_fourier_encoded_tv

FUNCTIONS
    GD_FE_TV(kspace, samp, alpha=0.5, lam=0.01, do_reordering=False, im_true=None, ignore_residual=False, disp=False, maxiter=200)
        Gradient descent for Fourier encoding model and TV constraint.
        
        kspace -- Measured image.
        samp -- Sampling mask.
        alpha -- Step size.
        lam -- TV constraint weight.
        do_reordering -- Whether or not to reorder for sparsity constraint.
        im_true -- The true image we are trying to reconstruct.
        ignore_residual -- Whether or not to break out of loop if resid increases.
        disp -- Whether or not to display iteration info.
        maxiter -- Maximum number of iterations.
        
        Solves the problem:
            min_x || kspace - FFT(im*samp) ||^2_2  + lam*TV(im)
        
        If im_true=None, then MSE will not be calculated.


```

