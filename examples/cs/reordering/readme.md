
## examples.cs.reordering.adluru

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/adluru.py)

```
NAME
    examples.cs.reordering.adluru - Reconstruct binary smiley using ported Adluru code.

DESCRIPTION
    Use Cartesian undersampling pattern (undersample in phase-encode dimension).
    I'm not in love in with the port I did of Ganesh's code, I would use the other
    convex TV implementation I did (mr_utils.cs.GD_TV) or proximal gradient
    descent (mr_utils.cs.proximal_GD).  I could only get this to work if I enforce
    data consistency every iteration, which makes me suspect something is wrong
    with the implementation...


```


## examples.cs.reordering.assignment_problem

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/assignment_problem.py)

```
NAME
    examples.cs.reordering.assignment_problem - Reordering assignment by minimum weight matching.

DESCRIPTION
    This is a simplistic example where we assume a k-sparse signal under the DCT.
    We then take a bunch of random measurements which is not sparse under the DCT.
    Then we match y to x by casting it as the assignment problem and using an
    out-of-the-box scipy solver to do it for us.  Once we've found the assignments,
    we use this as the reordering of y to make it look like x, which was by
    assumption k-sparse!  Assigned y has many nonzero components, but the most
    significant k match those of x.
    
    The point of this exercise is to show that given even random data, we can make
    it match a signal we know to be k-sparse, and thus be approximately k-sparse
    itself.


```


## examples.cs.reordering.basinhopping_coefficient_values

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/basinhopping_coefficient_values.py)

```
NAME
    examples.cs.reordering.basinhopping_coefficient_values - Demonstrate basinhopping to solve for coefficient values.

DESCRIPTION
    Counting xk in x is a nonlinear operation (can't be represented by matrix
    multiplies) as far as I can tell.  The closes I could come is the count
    function in this file that unfortunely needs an element by element inverse.
    You could run all the elements of down the diagonal of an x.size by x.size
    matrix, then you get:
        trace [X*a - xk*a + 1]^-1
    
    But remember that the offdiagonal elements are not truly zero, so the matrix is
    ill-conditioned and does not give you thing answer (I tried it...).  So unless
    there's a way to force all off of-diagonal elements to be zero (by masking?)
    then you're stuck with trying to solve the coefficient value problem
    numerically.
    
    Thus this example: given the location of the coefficients, we use the
    basinhopping algorithm to find the best coefficient values we can.  We even
    dispense with histogram/kernel density estimators in this example in favor
    of the simple object function:
        || sort(xhat) - sort(x) ||_2^2
    
    which has the advantage of being stupid easy, although the gradient w.r.t c
    could be tricky to come up with since we're sorting xhat...  But that was
    always the problem, right?  Finding analytical solutions to combinatorial
    problems is hard.  So jump and around some basins and try to get some
    reasonable values -- that seems like a descent enough idea.
    
    Results:
        Given that we know where the coefficients are, we actually do a great job
        of beating the sort(x), even when we don't find the optimal coefficient
        values -- many local minima appear to beat sorting.  Sorted coefficients
        have very large coefficients and the die off approximately exponentially,
        whereas our coefficient values don't die off -- they are quite large for
        all k, and then if the perfect coefficient values are not found, then they
        die off (exponentially), usually below the coefficient level of sort(x),
        however, this is not always the case (if we don't solve for good
        coefficient values).
    
        Large k is a funny choice (because sort(x) generally dies off pretty
        quickly), but will find coefficients such that after k, the coefficients
        are less than sort(x), and the first k coefficients are much larger than
        sort(x).
    
    Notes on computation:
        Large N is hard on the linear_sum_assignment problem.
        Large k is hard on basinhopping.  Haven't tried tweaking anything on
        basinhopping, might be a fun afternoon activity...

FUNCTIONS
    count(x, xk, a=1e+20)
        Count number of xk in x.
        
        x -- Array with elements xk.
        xk -- Specific xk to count how many of.
        
        This is asymptotically true as a -> inf.
    
    count_all(x, x_ref, c_eq_ref, a=1e+20)
        Count all.
    
    forward(x)
        Forward transform.
    
    inverse(c)
        Inverse transform.
    
    obj(ck, idx, x_ref)
        Objective function for basinhopping.


```


## examples.cs.reordering.bulkup_and_whitledown

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/bulkup_and_whitledown.py)

```
NAME
    examples.cs.reordering.bulkup_and_whitledown - A couple strategies for manipulating sparse coefficients.

DESCRIPTION
    This seems to depend a lot on the transform you want to be sparse in.  We
    choose the DCT amnd CDF 9/7 wavelet for this example.
    
    For the DCT, both techniques appear better than no reordering and are about
    equivalent.
    
    These techniques seem to do much better (for proper choice of k) with the
    wavelet transform.  Both of these can perform much better than no reordering
    at all.


```


## examples.cs.reordering.cardiac_radial_scr_gd

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/cardiac_radial_scr_gd.py)

```
NAME
    examples.cs.reordering.cardiac_radial_scr_gd - Spatially total variation constrained cardiac reconstruction.

DESCRIPTION
    Using Ganesh's cardiac example, reconstruct comparing using reordered and not.
    
    This replicates figures in paper:
        G.Adluru, E.V.R. DiBella. "Reordering for improved constrained
        reconstruction from undersampled k-space data". International Journal of
        Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008.
        doi:10.1155/2008/341684.
    
    We assume we know the exact reordering to begin with (this is a ridiculous
    assumption, by the way).  Also, it seems to be weird data (look at log of
    kspace data, strange).  That along with the fact that recon fails when
    orthonormal fourier encoding is used (uft.forward_ortho), it makes me think
    that this is strange data and we should be using another example data set.


```


## examples.cs.reordering.cardiac_radial_scr_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/cardiac_radial_scr_iht.py)

```
NAME
    examples.cs.reordering.cardiac_radial_scr_iht - Use iterative hard thresholding to recover cardiac image.

DESCRIPTION
    This doesn't work very well because we're not truly sparse.


```


## examples.cs.reordering.cardiac_scr_reordering_comparison

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/cardiac_scr_reordering_comparison.py)

```
NAME
    examples.cs.reordering.cardiac_scr_reordering_comparison - Comparison of reordering methods on cardiac reconstruction.

DESCRIPTION
    Compares:
        None
        Bulk up
        Whittle down
        sort2d
        colwise
        rowwise
    
    Uses selective updating, as that really seems to get the job done.
    
    Needs tunable params:
        level -- levels of decomposition for wavelet transform
        percent_to_keep -- how selective the update is
        maxiter -- how long to run the recon
        alpha -- step size
        k -- percent of coefficients to bulk up/whittle
    
    In general, sort2d seems to win everytime, but they all perform similarly.
    Perhaps if you had a strange transform that sorting didn't work with, you'd
    want to give bulk/whittle a try, otherwise, it doesn't seem like it's worth
    the hassle.
    
    If the prior is the true image, then sort2d wins by a landslide, followed by
    col-wise, row-wise, a tie with Bulk/Whittle, and then the not-sorted image.
    If the prior is the corrupted image, then Bulk trends lower for longer.
    
    It's kind of a mixed bag and hard to say with so many tuning parameters and
    the need for cross validation.
    
    Note: there's something strange with the cardiac data, so might want to try
    out a different data set.  See fourier transform, strange phase.


```


## examples.cs.reordering.cartesian_pe_fd_grad_desc

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/cartesian_pe_fd_grad_desc.py)

```
NAME
    examples.cs.reordering.cartesian_pe_fd_grad_desc - Gradient descent reconstruction of undersampled binary smiley face.

DESCRIPTION
    Smiley face is known to be sparse in finite differences domain (hence 'fd' in
    filename).  Cartesian undersampling in the phase encode direction.


```


## examples.cs.reordering.cartesian_pe_fd_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/cartesian_pe_fd_iht.py)

```
NAME
    examples.cs.reordering.cartesian_pe_fd_iht


```


## examples.cs.reordering.cholesky_precond

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/cholesky_precond.py)

```
NAME
    examples.cs.reordering.cholesky_precond - Try to leverage prexisting sorting strategies.

FUNCTIONS
    reverse_cuthill_mckee(...)
        reverse_cuthill_mckee(graph, symmetric_mode=False)
        
        Returns the permutation array that orders a sparse CSR or CSC matrix
        in Reverse-Cuthill McKee ordering.  
        
        It is assumed by default, ``symmetric_mode=False``, that the input matrix 
        is not symmetric and works on the matrix ``A+A.T``. If you are 
        guaranteed that the matrix is symmetric in structure (values of matrix 
        elements do not matter) then set ``symmetric_mode=True``.
        
        Parameters
        ----------
        graph : sparse matrix
            Input sparse in CSC or CSR sparse matrix format.
        symmetric_mode : bool, optional
            Is input matrix guaranteed to be symmetric.
        
        Returns
        -------
        perm : ndarray
            Array of permuted row and column indices.
        
        Notes
        -----
        .. versionadded:: 0.15.0
        
        References
        ----------
        E. Cuthill and J. McKee, "Reducing the Bandwidth of Sparse Symmetric Matrices",
        ACM '69 Proceedings of the 1969 24th national conference, (1969).
        
        Examples
        --------
        >>> from scipy.sparse import csr_matrix
        >>> from scipy.sparse.csgraph import reverse_cuthill_mckee
        
        >>> graph = [
        ... [0, 1 , 2, 0],
        ... [0, 0, 0, 1],
        ... [2, 0, 0, 3],
        ... [0, 0, 0, 0]
        ... ]
        >>> graph = csr_matrix(graph)
        >>> print(graph)
          (0, 1)    1
          (0, 2)    2
          (1, 3)    1
          (2, 0)    2
          (2, 3)    3
        
        >>> reverse_cuthill_mckee(graph)
        array([3, 2, 1, 0], dtype=int32)


```


## examples.cs.reordering.combinatorical_dct_1d

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/combinatorical_dct_1d.py)

```
NAME
    examples.cs.reordering.combinatorical_dct_1d - Do the search through all possible k-sparse to match densities in 1d.

DESCRIPTION
    Here we consider the 1d case of signals known to be k-spare under the DCT.
    We do a brute force search through all possible k-sparse signals to try to
    find the correct one.
    
    Histogram constraints using l2-metric is used.  Coefficient values are solved
    using scipy.optimize.minimize.
    
    What's interesting is that we perform better than sorting especially at small
    N.  So patch based processing with reordering has the potential to be really
    good.

FUNCTIONS
    density(x0, bins, lims)
        Return density estimate of x0.
    
    err_fun(cc, N, bins, lims)
        Error function for parallel loop.
    
    get_xhat(N, locs, _bins, _lims)
        Compute xhat for given coefficient locations.
    
    kthCombination(k, l, r)
        Get the kth combination.
    
    nCr(n, r)
        nCr function.
    
    obj(c00, N, locs, bins, lims)
        Objective: choose c0 to minimize difference between histograms.
    
    reduce(...)
        reduce(function, sequence[, initial]) -> value
        
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.


```


## examples.cs.reordering.full_example

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/full_example.py)

```
NAME
    examples.cs.reordering.full_example - Search all coefficient combinations and use basinhopping at each step.

DESCRIPTION
    Exhaustively search each possible class of k-sparse signals.  For each class,
    solve for coefficient values that minimize the histogram error using a global
    optimization technique.  In this case, we choose the basinhopping algorithm.
    
    I also introduce the notion that we might not expect the coefficient locations
    to be in the high frequency locations -- since the sorted signal removes high
    frequencies.  So we can restrict the effective search space from n choose k to
    something like n/r choose k, where r is a reduction factor (r > 1).

FUNCTIONS
    forward(x)
        Forward transform.
    
    inverse(c)
        Inverse transform.


```


## examples.cs.reordering.minimal_example

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/minimal_example.py)

```
NAME
    examples.cs.reordering.minimal_example - Make a minimal example showing how this is supposed to work.

DESCRIPTION
    Should be small enough for us to exhaustively search for the best solution as
    to show that we can do better than montonically sorting.  We will consider a
    simple 1d signal known to be sparse under the discrete cosine transform after
    reordering.


```


## examples.cs.reordering.paper_results

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/paper_results.py)

```
NAME
    examples.cs.reordering.paper_results - Generate figures for paper.

FUNCTIONS
    H_metric(H1, H2, mode='chi2')
        Histogram metrics.
        
        H1, H2 -- 1d histograms with matched bins.
        mode -- Metric to use.
        
        Modes:
            l2 -- Euclidean distance
            l1 -- Manhattan distance
            vcos -- Vector cosine distance
            intersect -- Histogram intersection distance
            chi2 -- Chi square distance
            jsd -- Jensen-Shannan Divergence
            emd -- Earth Mover's Distance
    
    plot_coeffs(c, *kargs)
        Plot sorted coefficients, c.


```


## examples.cs.reordering.random_search_reordering

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/random_search_reordering.py)

```
NAME
    examples.cs.reordering.random_search_reordering - Example demonstrating how difficult it is to find an effective reordering.

DESCRIPTION
    We use a wavelet transformation and try k different random permutations.

FUNCTIONS
    T(x0)
        Wavelet transform.


```


## examples.cs.reordering.time_curves

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/reordering/time_curves.py)

```
NAME
    examples.cs.reordering.time_curves - Load some time curves from real data to examine histograms.

CLASSES
    builtins.object
        Sparsify
    
    class Sparsify(builtins.object)
     |  Picklable sparsifying transform object.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, prior)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  forward_dct(self, x)
     |      Sparsifying transform, discrete cosine transform.
     |  
     |  forward_fd(self, x)
     |      Sparsifying transform, finite differences.
     |  
     |  inverse_dct(self, x)
     |      Inverse sparsifying transform, discrete cosine transform.
     |  
     |  inverse_fd(self, x)
     |      Inverse sparsifying transform, finite differences.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)


```

