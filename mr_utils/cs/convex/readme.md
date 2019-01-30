
# CS
## mr_utils.cs.convex.gd_fourier_encoded_tv

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/convex/gd_fourier_encoded_tv.py)

```
NAME
    mr_utils.cs.convex.gd_fourier_encoded_tv - Gradient descent algorithm for Fourier encoding model and TV constraint.

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


## mr_utils.cs.convex.gd_tv

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/convex/gd_tv.py)

```
NAME
    mr_utils.cs.convex.gd_tv - Gradient descent with built in TV and flexible encoding model.

FUNCTIONS
    GD_TV(y, forward_fun, inverse_fun, alpha=0.5, lam=0.01, do_reordering=False, x=None, ignore_residual=False, disp=False, maxiter=200)
        Gradient descent for a generic encoding model and TV constraint.
        
        y -- Measured data (i.e., y = Ax).
        forward_fun -- A, the forward transformation function.
        inverse_fun -- A^H, the inverse transformation function.
        alpha -- Step size.
        lam -- TV constraint weight.
        do_reordering -- Whether or not to reorder for sparsity constraint.
        x -- The true image we are trying to reconstruct.
        ignore_residual -- Whether or not to break out of loop if resid increases.
        disp -- Whether or not to display iteration info.
        maxiter -- Maximum number of iterations.
        
        Solves the problem:
            min_x || y - Ax ||^2_2  + lam*TV(x)
        
        If x=None, then MSE will not be calculated.


```


## mr_utils.cs.convex.proximal_gd

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/convex/proximal_gd.py)

```
NAME
    mr_utils.cs.convex.proximal_gd - Proximal Gradient Descent.

DESCRIPTION
    Flexible encoding model, flexible sparsity model, and flexible reordering
    model.  This is the one I would use out of all the ones I've coded up.
    Might be slower than the others as there's a little more checking to do each
    iteration.

FUNCTIONS
    proximal_GD(y, forward_fun, inverse_fun, sparsify, unsparsify, reorder_fun=None, mode='soft', alpha=0.5, selective=None, x=None, ignore_residual=False, disp=False, maxiter=200)
        Proximal gradient descent for a generic encoding, sparsity models.
        
        y -- Measured data (i.e., y = Ax).
        forward_fun -- A, the forward transformation function.
        inverse_fun -- A^H, the inverse transformation function.
        sparsify -- Sparsifying transform.
        unsparsify -- Inverse sparsifying transform.
        reorder_fun --
        unreorder_fun --
        mode -- Thresholding mode: {'soft','hard','garotte','greater','less'}.
        alpha -- Step size, used for thresholding.
        selective -- Function returning indicies of update to keep at each iter.
        x -- The true image we are trying to reconstruct.
        ignore_residual -- Whether or not to break out of loop if resid increases.
        disp -- Whether or not to display iteration info.
        maxiter -- Maximum number of iterations.
        
        Solves the problem:
            min_x || y - Ax ||^2_2  + lam*TV(x)
        
        If x=None, then MSE will not be calculated. You probably want mode='soft'.
        For the other options, see docs for pywt.threshold.  selective=None will
        not throw away any updates.


```

