
# UTILS
## mr_utils.utils.cdf

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/cdf.py)

```
NAME
    mr_utils.utils.cdf - ## NOT WORKING

FUNCTIONS
    waveletcdf97(X, Level)
        WAVELETCDF97  Cohen-Daubechies-Feauveau 9/7 wavelet transform.
        
          Y = WAVELETCDF97(X, L) decomposes X with L stages of the
          Cohen-Daubechies-Feauveau (CDF) 9/7 wavelet.  For the
          inverse transform, WAVELETCDF97(X, -L) inverts L stages.
          Filter boundary handling is half-sample symmetric.
        
          X may be of any size; it need not have size divisible by 2^L.
          For example, if X has length 9, one stage of decomposition
          produces a lowpass subband of length 5 and a highpass subband
          of length 4.  Transforms of any length have perfect
          reconstruction (exact inversion).
        
          If X is a matrix, WAVELETCDF97 performs a (tensor) 2D wavelet
          transform.  If X has three dimensions, the 2D transform is
          applied along the first two dimensions.
        
          Example:
          Y = waveletcdf97(X, 5);    % Transform image X using 5 stages
          R = waveletcdf97(Y, -5);   % Reconstruct from Y
        
        Pascal Getreuer 2004-2006


```


## mr_utils.utils.cdf97

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/cdf97.py)

```
NAME
    mr_utils.utils.cdf97 - ## NOT WORKING!

FUNCTIONS
    fwt97(s, width, height)
        Forward Cohen-Daubechies-Feauveau 9 tap / 7 tap wavelet transform
        performed on all columns of the 2D n*n matrix signal s via lifting.
        The returned result is s, the modified input matrix.
        The highpass and lowpass results are stored on the left half and right
        half of s respectively, after the matrix is transposed.
    
    fwt97_2d(m, nlevels=1)
        Perform the CDF 9/7 transform on a 2D matrix signal m.
        nlevel is the desired number of times to recursively transform the
        signal.
    
    iwt97(s, width, height)
        Inverse CDF 9/7.
    
    iwt97_2d(m, nlevels=1)
        Inverse CDF 9/7 transform on a 2D matrix signal m.
        nlevels must be the same as the nlevels used to perform the fwt.


```


## mr_utils.utils.ellipse

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/ellipse.py)

```
NAME
    mr_utils.utils.ellipse - General functions for working with ellipses.

FUNCTIONS
    check_fit(C, x, y)
        General quadratic polynomial function.
        
        C -- coefficients.
        x, y -- Coordinates assumed to be on ellipse.
        
        We want this to equal 0 for a good ellipse fit.   This polynomial is called
        the algebraic distance of the point (x, y) to the given conic.
        
        See:
            Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
            simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
            free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.
        
            Halır, Radim, and Jan Flusser. "Numerically stable direct least squares
            fitting of ellipses." Proc. 6th International Conference in Central
            Europe on Computer Graphics and Visualization. WSCG. Vol. 98. 1998.
    
    fit_ellipse_fitzgibon(x, y)
        Python port of direct ellipse fitting algorithm by Fitzgibon et. al.
        
        x, y -- Coordinates assumed to be on ellipse.
        
        See Figure 1 from:
            Halır, Radim, and Jan Flusser. "Numerically stable direct least squares
            fitting of ellipses." Proc. 6th International Conference in Central
            Europe on Computer Graphics and Visualization. WSCG. Vol. 98. 1998.
        
        Also see previous python port:
            http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
    
    fit_ellipse_halir(x, y)
        Python port of improved ellipse fitting algorithm by Halir and Flusser.
        
        x, y -- Coordinates assumed to be on ellipse.
        
        Note that there should be at least 6 pairs of (x,y).
        
        From the paper's conclusion:
            "Due to its systematic bias, the proposed fitting algorithm cannot be
            used directly in applications where excellent accuracy of the fitting
            is required. But even in that applications our method can be useful as
            a fast and robust estimator of a good initial solution of the fitting
            problem..."
        
        See figure 2 from:
            Halır, Radim, and Jan Flusser. "Numerically stable direct least squares
            fitting of ellipses." Proc. 6th International Conference in Central
            Europe on Computer Graphics and Visualization. WSCG. Vol. 98. 1998.
    
    fit_ellipse_nonlin(x, y, polar=False)
        Fit ellipse only depending on semi-major axis and eccentricity.
        
        x, y -- Coordinates assumed to be on ellipse.
        polar -- Whether or not coordinates are provided as polar or Cartesian.
        
        Note that if polar=True, then x will be assumed to be radius and y will be
        assumed to be theta.
        
        See:
            https://scipython.com/book/chapter-8-scipy/examples/
            non-linear-fitting-to-an-ellipse/
    
    get_center(c)
        Compute center of ellipse from implicit function coefficients.
        
        c -- Coefficients of general quadratic polynomial function for conic funs.
    
    get_semiaxes(c)
        Solve for semi-axes of the cartesian form of the ellipse equation.
        
        c -- Coefficients of general quadratic polynomial function for conic funs.
        
        See:
            https://en.wikipedia.org/wiki/Ellipse
    
    rotate_coefficients(c, phi)
        Rotate coefficients of implicit equations through angle phi.
        
        c -- Coefficients of general quadratic polynomial function for conic funs.
        phi -- Angle in radians to rotate ellipse.
        
        See:
            http://www.mathamazement.com/Lessons/Pre-Calculus/
            09_Conic-Sections-and-Analytic-Geometry/rotation-of-axes.html


```


## mr_utils.utils.find_nearest

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/find_nearest.py)

```
NAME
    mr_utils.utils.find_nearest

FUNCTIONS
    find_nearest(array, value)
        Given straws and needle, find the closest straw to the needle.
        
        array -- hay stack.
        value -- needle.


```


## mr_utils.utils.grad_tv

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/grad_tv.py)

```
NAME
    mr_utils.utils.grad_tv - Gradient of total variation term for gradient descent update.

FUNCTIONS
    dTV(A, eps=1e-08)
        Compute derivative of the TV with respect to the matrix A.
        
        A -- 2d matrix (can be complex).
        eps -- small positive constant used to avoid a divide by zero.
        
        Implements Equation [13] from:
            Zhang, Yan, Yuanyuan Wang, and Chen Zhang. "Total variation based
            gradient descent algorithm for sparse-view photoacoustic image
            reconstruction." Ultrasonics 52.8 (2012): 1046-1055.


```


## mr_utils.utils.histogram

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/histogram.py)

```
NAME
    mr_utils.utils.histogram - Some functions for working with histograms.

FUNCTIONS
    dH(H1, H2, mode='l2')
        Histogram metrics.
        
        H1, H2 -- 1d histograms with matched bins.
        mode -- Metric to use.
        
        Similar bins means the same number and size over the same range.
        
        Modes:
            l2 -- Euclidean distance
            l1 -- Manhattan distance
            vcos -- Vector cosine distance
            intersect -- Histogram intersection distance
            chi2 -- Chi square distance
            jsd -- Jensen-Shannan Divergence
            emd -- Earth Mover's Distance
        
        Issues:
            I'm not completely convinced that intersect is doing the right thing.
        
        The quality of the metric will depend a lot on the qaulity of the
        histograms themselves.  Obviously more samples and well-chosen bins will
        help out in the comparisons.
    
    hist_match(source, template)
        Adjust the pixel values of a grayscale image such that its histogram
        matches that of a target image
        
        Arguments:
        -----------
            source: np.ndarray
                Image to transform; the histogram is computed over the flattened
                array
            template: np.ndarray
                Template image; can have different dimensions to source
        Returns:
        -----------
            matched: np.ndarray
                The transformed output image
        
        See:
            https://stackoverflow.com/questions/32655686/histogram-matching-of-two-images-in-python-2-x


```


## mr_utils.utils.mi_ssfp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/mi_ssfp.py)

```
NAME
    mr_utils.utils.mi_ssfp

FUNCTIONS
    mi_ssfp(images, pc_axis=0)
        Compute maximum intensity SSFP.
        
        images -- Array of phase-cycled images.
        pc_axis -- Which dimension is the phase-cycle dimension.
        
        Implements Equation [5] from:
            Bangerter, Neal K., et al. "Analysis of multiple‐acquisition SSFP."
            Magnetic Resonance in Medicine: An Official Journal of the
            International Society for Magnetic Resonance in Medicine 51.5 (2004):
            1038-1047.


```


## mr_utils.utils.orderings

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/orderings.py)

```
NAME
    mr_utils.utils.orderings - Methods for orderings for signals.

DESCRIPTION
    Methods return flattened indices.
    Hopefully these orderings make the signals more sparse in some domain.

FUNCTIONS
    brute_force1d(x, T)
        Given transform matrix, T, sort 1d signal exhaustively.
        
        This IS NOT A GOOD IDEA.
    
    bulk_up(x, T, Ti, k)
        Given existing nonzero coefficients, try to make large ones larger.
        
        x -- Array to find ordering of.
        T -- Transform function.
        Ti -- Inverse transform function.
        k -- Percent of coefficients to shoot for.
    
    col_stacked_order(x)
        Find ordering of monotonically varying flattened array, x.
        
        x -- Array to find ordering of.
        
        Note that you might want to provide abs(x) if x is a complex array.
    
    colwise(x)
        Find ordering of monotonically varying columns.
        
        x -- Array to find ordering of.
    
    factorial(...)
        factorial(x) -> Integral
        
        Find x!. Raise a ValueError if x is negative or non-integral.
    
    gen_sort1d(x, T)
        Given 1D transform T, sort 1d signal, x.
    
    inverse_permutation(ordering)
        Given some permutation, find the inverse permutation.
        
        ordering -- Flattened indicies, such as output of np.argsort.
    
    random_match(x, T, return_sorted=False)
        Match x to T as closely as possible pixel by pixel.
        
        x -- Array to find ordering of.
        T -- Target matrix.
        return_sorted -- Whether or not to return the sorted matrix.
    
    random_match_by_col(x, T, return_sorted=False)
        Given matrix T, choose reordering of x that matches it col by col.
        
        x -- Array to find ordering of.
        T -- Target matrix.
        return_sorted -- Whether or not to return the sorted matrix.
    
    random_search(x, T, k, compare='l1', compare_opts=None, disp=False)
        Given transform T, find the best of k permutations.
        
        x -- Array to find the ordering of.
        T -- Transform matrix/function that we want x to be sparse under.
        k -- Number of permutations to try (randomly selected).
        compare -- How to compare two permutations.
        compare_opts -- Arguments to pass to compare function.
        disp -- Verbose mode.
        
        compare={'nonzero', 'l1', fun}.
    
    rowwise(x)
        Find ordering of monotonically varying rows.
        
        x -- Array to find ordering of.
    
    whittle_down(x, T, Ti, k)
        Given existing nonzero coefficients, try to remove lower ones.
        
        x -- Array to find ordering of.
        T -- Transform function.
        Ti -- Inverse transform function.
        k -- Percent of coefficients to shoot for.


```


## mr_utils.utils.package_script

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/package_script.py)

```
NAME
    mr_utils.utils.package_script - Package a script together with all its dependencies.

DESCRIPTION
    For example, on a remote computer I know for a fact that numpy and scipy are
    available, but I cannot or cannot easily gaurantee that module x will be
    installed.  I want to run script MyScript.py on this remote machine, but it
    depends on module x.  package_script() will recurse through MyScript.py and
    prepend module x (and all of module x's dependencies down to numpy, scipy, and
    default python modules, assuming I've set existing_modules=['numpy', 'scipy']).

FUNCTIONS
    get_imports(filename, existing_modules=None)
        Removes import statements and gets filenames of where imports are.
    
    get_std_lib()
        Get list of all Python standard library modules.
    
    package_script(filename, existing_modules=None)
        Package a script together with all dependencies.
        
        filename -- Path to Python script we wish to package.
        existing_modules -- List of terminating modules.
        
        "Terminating module" is a module we assume is available on the machine we
        want to run the packaged script on.  These are python's built-in modules
        plus all existing_modules specified by caller.


```


## mr_utils.utils.percent_ripple

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/percent_ripple.py)

```
NAME
    mr_utils.utils.percent_ripple

FUNCTIONS
    percent_ripple(profile)
        Calculate percent ripple of the bSSFP spectral profile.
        
        profile -- The off-resonance profile as a function of theta.
        
        The residual ripple can be predicted by examining the variations in the
        expected signal profile with free-precession angle, theta.
        
        Implements percent ripple, Equation [11], from:
            Bangerter, Neal K., et al. "Analysis of multiple‐acquisition SSFP."
            Magnetic Resonance in Medicine: An Official Journal of the
            International Society for Magnetic Resonance in Medicine 51.5 (2004):
            1038-1047.


```


## mr_utils.utils.permutation_rank

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/permutation_rank.py)

```
NAME
    mr_utils.utils.permutation_rank - Determining rank of a permutation and generating permutation given rank.

DESCRIPTION
    This implementation is due to:
        https://rosettacode.org/wiki/Permutations/Rank_of_a_permutation#Python
    
    See:
        Myrvold, Wendy, and Frank Ruskey. "Ranking and unranking permutations in
        linear time." Information Processing Letters 79.6 (2001): 281-284.

FUNCTIONS
    fact = factorial(...)
        factorial(x) -> Integral
        
        Find x!. Raise a ValueError if x is negative or non-integral.
    
    get_random_ranks(permsize, samplesize)
    
    identity_perm(n)
        Generate sequence 0:n-1.
    
    init_pi1(n, pi)
        Get the inverse permutation of pi.
    
    pi2rank(pi, method='rank2', iterative=True)
        Return rank of permutation pi.
        
        pi -- Permutation.
        method -- Which ranking method to use, one of {'rank1', 'rank2'}.
        iterative -- Whether or not to use iterative or recursive version.
        
        The permutation pi should be a permutation of the list range(n) and contain
        n elements.
        
        'method' should be one of {'rank1', 'rank2'} corresponding to the two
        schemes presented in the Myrvold and Ruskey paper.  There is an iterative
        version available for both algorithms.
        
        Implements algorithms from:
            Myrvold, Wendy, and Frank Ruskey. "Ranking and unranking permutations
            in linear time." Information Processing Letters 79.6 (2001): 281-284.
    
    rank2pi(r, n, method='rank2')
        Given rank and permutation length produce the corresponding permutation.
        
        r -- Rank.
        n -- Lenth of the permutation.
        method -- Which ranking method to use, one of {'rank1', 'rank2'}.
        
        Implements algorithms from:
            Myrvold, Wendy, and Frank Ruskey. "Ranking and unranking permutations
            in linear time." Information Processing Letters 79.6 (2001): 281-284.
    
    ranker1(n, pi, pi1)
        Rank1 algorithm from M&R paper.
    
    ranker1_iter(n, pi, pi1)
        Iterative version of ranker1.
    
    ranker2(n, pi, pi1)
        Ranker2 algorithm from M&R paper.
    
    ranker2_iter(n, pi, pi1)
        Iterative version of ranker2.
    
    test1(comment, unranker, ranker)
    
    test2(comment, unranker)
    
    unranker1(n, r, pi)
        Given rank produce the corresponding permutation.
        
        Rank is given by rank1 algorithm of M&R paper.
    
    unranker2(n, r, pi)
        Given rank produce the corresponding permutation.
        
        Rank is given by rank2 algorithm of M&R paper.


```


## mr_utils.utils.printtable

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/printtable.py)

```
NAME
    mr_utils.utils.printtable

CLASSES
    builtins.object
        Table
    
    class Table(builtins.object)
     |  Table with header and columns. Nothing fancy.
     |  
     |  Class meant for simple column printing, e.g., printing updates for each
     |  iteration of an iterative algorithm.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, headings, widths, formatters=None, pad=2, symbol='#')
     |      Initialize the table object.
     |      
     |      headings -- List of strings to use as headings for columns.
     |      widths -- List of widths for each column.
     |      formatters -- List of format options to use for each column.
     |      pad -- Space between columns
     |      symbol -- Character to use as separator between header and table rows.
     |      
     |      widths=[int] will assign each column the same width of [int].
     |      formatters=None will use 'g' for every column.
     |  
     |  header(self)
     |      Return table header.
     |  
     |  row(self, vals)
     |      Return row of table.
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


## mr_utils.utils.rot

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/rot.py)

```
NAME
    mr_utils.utils.rot

FUNCTIONS
    rot(theta)
        2D rotation matrix through angle theta (rad).


```


## mr_utils.utils.sort2d

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/sort2d.py)

```
NAME
    mr_utils.utils.sort2d

FUNCTIONS
    sort2d(A)
        Sorting algorithm for two-dimensional arrays.
        
        A -- Array to be sorted.
        
        Note: if A is complex, you may want to provide abs(A).  Returns sorted
        array and flattened indices.
        
        Numpy implementation of algorithm from:
            Zhou, M., & Wang, H. (2010, December). An efficient selection sorting
            algorithm for two-dimensional arrays. In Genetic and Evolutionary
            Computing (ICGEC), 2010 Fourth International Conference on
            (pp. 853-855). IEEE.
    
    sort2d_loop(A)
        An efficient selection sorting algorithm for two-dimensional arrays.
        
        A -- 2d array to be sorted.
        
        Implementation of algorithm from:
            Zhou, M., & Wang, H. (2010, December). An efficient selection sorting
            algorithm for two-dimensional arrays. In Genetic and Evolutionary
            Computing (ICGEC), 2010 Fourth International Conference on
            (pp. 853-855). IEEE.


```


## mr_utils.utils.sos

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/sos.py)

```
NAME
    mr_utils.utils.sos - Simple root sum of squares image combination.

FUNCTIONS
    sos(im, axes=0)
        Root sum of squares combination along given axes.
        
        im -- Input image.
        axes -- Dimensions to sum across.


```


## mr_utils.utils.wavelet

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/utils/wavelet.py)

```
NAME
    mr_utils.utils.wavelet - Wrappers for PyWavelets.

FUNCTIONS
    cdf97_2d_forward(x, level)
        Forward 2D Cohen–Daubechies–Feauveau 9/7 wavelet.
        
        x -- 2D signal.
        level -- Decomposition level.
        
        Returns transform, same shape as input, with locations.  Locations is a
        list of indices instructing cdf97_2d_inverse where the coefficients for
        each block are located.
        
        Biorthogonal 4/4 is the same as CDF 9/7 according to wikipedia:
            see https://en.wikipedia.org/wiki/
                Cohen%E2%80%93Daubechies%E2%80%93Feauveau_wavelet#Numbering
    
    cdf97_2d_inverse(coeffs, locations)
        Inverse 2D Cohen–Daubechies–Feauveau 9/7 wavelet.
        
        coeffs,locations -- Output of cdf97_2d_forward().
    
    combine_chunks(wvlt, shape, dtype=<class 'float'>)
        Stitch together the output of PyWavelets wavedec2.
        
        wvlt -- Output of pywt.wavedec2().
        shape -- Desired shape.
        dtype -- Type of numpy array.
        
        We have tuples that look like this:
                                    -------------------
                                    |        |        |
                                    | cA(LL) | cH(LH) |
                                    |        |        |
        (cA, (cH, cV, cD))  <--->   -------------------
                                    |        |        |
                                    | cV(HL) | cD(HH) |
                                    |        |        |
                                    -------------------
    
    split_chunks(coeffs, locations)
        Separate the stitched together transform into blocks again.
        
        x -- Stitched together wavelet transform.
        locations -- Indices where the coefficients for each block are located.
        
        x, locations are the output of combine_chunks().
    
    wavelet_forward(x, wavelet, mode='symmetric', level=None, axes=(-2, -1))
        Wrapper for the multilevel 2D discrete wavelet transform.
        
        x -- Input data.
        wavelet -- Wavelet to use.
        mode -- Signal extension mode.
        level -- Decomposition level (must be >= 0).
        axes -- Axes over which to compute the DWT.
        
        See PyWavelets documentation on pywt.wavedec2() for more information.
        
        If level=None (default) then it will be calculated using the dwt_max_level
        function.
    
    wavelet_inverse(coeffs, locations, wavelet, mode='symmetric', axes=(-2, -1))
        Wrapper for the multilevel 2D inverse discrete wavelet transform.
        
        coeffs -- Combined coefficients.
        locations -- Indices where the coefficients for each block are located.
        wavelet -- Wavelet to use.
        mode -- Signal extension mode.
        axes -- Axes over which to compute the IDWT.
        
        coeffs, locations are the output of forward().


```

