
# OPTIMIZATION
## mr_utils.optimization.gd

[Source](../master/mr_utils/optimization/gd.py)

```
NAME
    mr_utils.optimization.gd

FUNCTIONS
    gd(f, grad, x0, alpha=None, iter=1000000.0, tol=1e-08)
        Gradient descent algorithm.
        
        f -- Function to be optimized.
        grad -- Function that computes the gradient of f.
        x0 -- Initial point to start to start descent.
        alpha -- Either a fixed step size or a function that returns step size.
        iter -- Do not exceed this number of iterations.
        tol -- Run until change in norm of gradient is within this number.


```


## mr_utils.optimization.gradient

[Source](../master/mr_utils/optimization/gradient.py)

```
NAME
    mr_utils.optimization.gradient

FUNCTIONS
    cd_gen_complex_step(f, x0, h=None, v=None)
        Compute generalized central difference complex step derivative of f.
        
        f -- Function to compute derivative of at x0.
        x0 -- Point to compute derivative of f on.
        h -- Real part of forward and backward derivatives.
        v -- Imaginary part of forward and backwards derivatives.
        
        If you choose h,v such that 3*h**2 =/= v**2, there will be an additional
        error term proportional to 3rd order derivative (not implemented).  So
            it's in your best interest to choose h,v so this error is minimized.
        
        Implements Equation 5 from:
            Abreu, Rafael, et al. "On the accuracy of the
            Complex-Step-Finite-Difference method." Journal of Computational and
            Applied Mathematics 340 (2018): 390-403.
    
    complex_step_6th_order(f, x0, h=None, v=None)
    
    fd_complex_step(f, x0, h=2.220446049250313e-16)
        Compute forward difference complex step of function f.
    
    fd_gen_complex_step(f, x0, h=0, v=2.220446049250313e-16)
        Compute generalized forward difference complex step derivative of f.
        
        f -- Function to compute derivative of at x0.
        x0 -- Point to compute derivative of f on.
        h -- Real part of forward perturbation.
        v -- Imaginary part of forward perturbation.
        
        Implements Equation 4 from:
            Abreu, Rafael, et al. "On the accuracy of the
            Complex-Step-Finite-Difference method." Journal of Computational and
            Applied Mathematics 340 (2018): 390-403.


```


## mr_utils.optimization.linesearch

[Source](../master/mr_utils/optimization/linesearch.py)

```
NAME
    mr_utils.optimization.linesearch

FUNCTIONS
    linesearch(obj, x0, a0, s)
    
    linesearch_quad(f, x, a, s)


```

