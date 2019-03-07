
## mr_utils.cs.linear_programming

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/linear_programming.py)

```
NAME
    mr_utils.cs.linear_programming


```


## mr_utils.cs.ordinator

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/ordinator.py)

```
NAME
    mr_utils.cs.ordinator - Performs combinatorial optimization to find permutation maximizing sparsity.

CLASSES
    builtins.object
        pdf_default
    
    class pdf_default(builtins.object)
     |  Picklable object for computing pdfs.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, prior)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  pdf(self, x)
     |      Estimate the pdf of x.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    get_xhat(locs, N, k, inverse, pdf_ref, pdf, pdf_metric)
        Compute xhat for given coefficient locations using basinhopping.
        
        locs -- Coefficient location indices.
        N -- Length of the desired signal (also number of coefficients in total).
        k -- Desired sparsity level.
        inverse -- Inverse sparsifying transform.
        pdf_ref -- Reference pdf of the prior to compare against.
        pdf -- Function that estimates pixel intensity distribution.
        pdf_metric -- Function that returns the distance between pdfs.
    
    obj(ck, N, locs, inverse, pdf_ref, pdf, pdf_metric)
        Objective function for basinhopping.
    
    ordinator1d(prior, k, inverse, chunksize=10, pdf=None, pdf_metric=None, forward=None, disp=False)
        Find permutation that maximizes sparsity of 1d signal.
        
        prior -- Prior signal estimate to base ordering.
        k -- Desired sparsity level.
        inverse -- Inverse sparsifying transform.
        chunksize -- Chunk size for parallel processing pool.
        pdf -- Function that estimates pixel intensity distribution.
        pdf_metric -- Function that returns the distance between pdfs.
        forward -- Sparsifying transform (only required if disp=True).
        disp -- Whether or not to display coefficient plots at the end.
        
        pdf_method=None uses histogram.  pdf_metric=None uses l2 norm. If disp=True
        then forward transform function must be provided.  Otherwise, forward is
        not required, only inverse.
        
        pdf_method should assume the signal will be bounded between (-1, 1).  We do
        this by always normalizing a signal before computing pdf or comparing.
    
    pdf_metric_default(x, y)
        Default pdf metric, l2 norm.
    
    search_fun(locs, N, k, inverse, pdf_ref, pdf, pdf_metric)
        Return function for parallel loop.
        
        locs -- Coefficient location indices.
        N -- Length of the desired signal (also number of coefficients in total).
        k -- Desired sparsity level.
        inverse -- Inverse sparsifying transform.
        pdf_ref -- Reference pdf of the prior to compare against.
        pdf -- Function that estimates pixel intensity distribution.
        pdf_metric -- Function that returns the distance between pdfs.
    
    time(...)
        time() -> floating point number
        
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.


```

