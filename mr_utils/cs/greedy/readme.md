
## mr_utils.cs.greedy.cosamp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/greedy/cosamp.py)

```
NAME
    mr_utils.cs.greedy.cosamp

FUNCTIONS
    cosamp(A, y, k, lstsq='exact', tol=1e-08, maxiter=500, x=None, disp=False)
        Compressive sampling matching pursuit (CoSaMP) algorithm.
        
        A -- Measurement matrix.
        y -- Measurements (i.e., y = Ax).
        k -- Number of expected nonzero coefficients.
        lstsq -- How to solve intermediate least squares problem.
        tol -- Stopping criteria.
        maxiter -- Maximum number of iterations.
        x -- True signal we are trying to estimate.
        disp -- Whether or not to display iterations.
        
        lstsq function:
            lstsq = { 'exact', 'lm', 'gd' }.
        
            'exact' solves it using numpy's linalg.lstsq method.
            'lm' uses solves with the Levenberg-Marquardt algorithm.
            'gd' uses 3 iterations of a gradient descent solver.
        
        Implements Algorithm 8.7 from:
            Eldar, Yonina C., and Gitta Kutyniok, eds. Compressed sensing: theory
            and applications. Cambridge University Press, 2012.


```

