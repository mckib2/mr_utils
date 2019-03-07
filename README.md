# mr_utils

mr_utils: magnetic resonance utilities. This repo is a collection of my
implementations of algorithms and tools for MR image reconstruction, mostly
in python.

## Orientation
There are few different things going on here.  There are algorithms, like the [geometric solution to the elliptical signal model](../master/mr_utils/recon/ssfp), as well as simulations, like [simulated bSSFP contrast](../master/mr_utils/sim/ssfp).

There's also some python functions and objects that interact with more polished tools such as [Gadgetron](../master/mr_utils/gadgetron) and [BART](../master/mr_utils/bart). You can use these python interfaces to easily write in Gadgetron, MATLAB, or BART functionality into your python scripts. These functions are written with the assumption of Gadgetron, MATLAB, etc. being run on some processing server (not necessarily on your local machine). If you use these, you'll want to create a [config file](../master/mr_utils/config) file.

## Documentation and Tests

Documentation is almost exclusively found in the docstrings of modules, functions, and classes.  This README file contains the output of help() for all the modules in the project.  README files can also be found in subdirectories containing only the help() output specific to that module.

Another great way to learn how things are used is by looking in the [examples](../master/examples).
Run examples from the root directory (same directory as setup.py) like this:

```bash
python3 examples/cs/reordering/cartesian_pe_fd_iht.py
```

If there's not an example, there might be some [tests](../master/mr_utils/tests). Individual tests can be run like this from the root directory (I recommend that you run tests from the home directory - imports will get messed up otherwise):

```bash
python3 -m unittest mr_utils/tests/recon/test_gs_recon.py
```

# Installation

Say you want to use this package in one of your python scripts.  You can install it using pip like so:

```bash
git clone https://github.com/mckib2/mr_utils
cd mr_utils
pip3 install -e ./
```

You'll need to manually install the ismrmrd-python-tools as it's currently not available on pypi. You can find it here: https://github.com/ismrmrd/ismrmrd-python-tools.git

# MAKE_README
## make_readme

[Source](https://github.com/mckib2/mr_utils/blob/master/make_readme.py)

```
NAME
    make_readme - Generate all README files for all the modules.

DESCRIPTION
    We rely heavily on the pydoc.render_doc() method.


```


# BART
## mr_utils.bart.bart

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/bart/bart.py)

```
NAME
    mr_utils.bart.bart - Simple interface to call BART's python object from mr_utils.

DESCRIPTION
    This will verify that BART's TOOLBOX_PATH is found, if not, an exception will
    be raised.  Consider using Bartholomew, it's meant to be a better interface
    to command-line BART.

FUNCTIONS
    bart(*args)
        Wrapper that passes arguments to BART installation.

```


## mr_utils.bart.bartholomew

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/bart/bartholomew.py)

```
NAME
    mr_utils.bart.bartholomew - More friendly python interface for BART.

DESCRIPTION
    I also want this to be able to run BART on remote computer through ssh, to
    remove BART as a strict dependency for the local machine, much like
    we treat Gadgetron.
    
    Import:
        import Bartholomew as B
    Usage:
        B.[bart-func](args)
    Example:
        traj_rad = B.traj(x=512,y=64,r=True)
        ksp_sim = B.phantom(k=True,s=8,t=traj_rad)
        igrid = B.nufft(ksp_sim,i=True,t=traj_rad)
    
    Notice that input ndarrays are positional arguments (e.g., ksp_sim is the
    first argument for nufft instead of the last).
    
    To get comma separated lists (e.g., -d x:x:x), use the List type:
        img = B.nufft(ksp_sim,i=True,d=[24,24,1],t=traj_rad)
    
    To get space separated lists (e.g., resize [-c] dim1 size1 ... dimn), use
    Tuple type:
        ksp_zerop = B.resize(lowres_ksp,c=(0,308,1,308))

CLASSES
    builtins.object
        BartholomewObject
    
    class BartholomewObject(builtins.object)
     |  Bartholomew object - more simple Python interface for BART.
     |  
     |  User is meant to import instance Bartholomew, e.g.,
     |      from mr_utils.bart import Bartholomew as B
     |  
     |  Methods defined here:
     |  
     |  __getattr__(self, name, *args, **kwargs)
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  format_args(self, args)
     |      Take in positional function arguments and format for command-line.
     |  
     |  format_kwargs(self, kwargs)
     |      Take in named function arguments and format for command-line.
     |  
     |  get_num_outputs(self)
     |      Return how many values the caller is expecting
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


## mr_utils.bart.client

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/bart/client.py)

```
NAME
    mr_utils.bart.client - Connect to BART over a network.

DESCRIPTION
    I do not believe this is working currently!
    
    Uses paramiko to connect to a network machine (could be your own machine),
    opens an instance of BART and returns the result.

FUNCTIONS
    client(num_out, cmd, files, host=None, username=None, password=None, root_dir=None)
        BART client.
        
        num_out -- Number of expected variables returned.
        cmd -- BART command to be run.
        files -- Any files to be provided to BART.
        host -- IP address of machine we want to connect to.
        username -- username to sign in with.
        password -- password to use for sign in (will be plain-text!)
        root_dir --


```


# CONFIG
## mr_utils.config.config

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/config/config.py)

```
NAME
    mr_utils.config.config - Provide an easy way to set things like gadgetron host, port, etc.

DESCRIPTION
    The ProfileConfig object will create (if it's not already created) a file
    called 'profiles.config' in the top level of the project (same directory as
    setup.py).  This file contains one or more profiles, one and only one of which
    must be set as active.  A profile contains ports and hostnames and other
    parameters to use for the gadgetron, MATLAB, siemens_to_ismrmrd, etc. clients.
    
    The config files use python's configparser format.  See implementation for
    details.
    
    Example profiles.config file:
    
        [default]
        gadgetron.host = localhost
        gadgetron.port = 9002
    
        [workcomp]
        gadgetron.host = 10.8.1.12
        gadgetron.port = 9002
        matlab.host = 10.8.1.12
        matlab.port = 9999
        matlab.bufsize = 1024
    
        [config]
        active = workcomp

CLASSES
    builtins.object
        ProfileConfig
    
    class ProfileConfig(builtins.object)
     |  ProfileConfig allows object oriented interaction with profiles.config.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, filename=None)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  activate_profile(self, profile)
     |      Assign a profile to be active.
     |      
     |      profile -- Profile label to make active.
     |      
     |      All other profiles will still persist, but will not be used.  Only one
     |      profile may be active at a time.
     |  
     |  create_profile(self, profile_name, args=None)
     |      Create a new profile.
     |      
     |      profile_name -- New profile's label.
     |      args -- key,value pairs of profile's attributes.
     |  
     |  get_config_val(self, key)
     |      Retrieve a config value.
     |      
     |      key -- Key of the (key,value) pair of the value to be looked up.
     |  
     |  set_config(self, args, profile=None)
     |      Update profile configuration files.
     |      
     |      profile -- The profile to update.
     |      args -- Dictionary of key,value updates.
     |      
     |      Keys -> Values:
     |          'gadgetron.host' -> (string) ip-address/hostname/etc
     |          'gadgetron.port' -> (int) port number
     |  
     |  update_file(self)
     |      Update profiles.config by overwriting contents.
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
    proximal_GD(y, forward_fun, inverse_fun, sparsify, unsparsify, reorder_fun=None, mode='soft', alpha=0.5, thresh_sep=True, selective=None, x=None, ignore_residual=False, disp=False, maxiter=200)
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
        thresh_sep -- Whether or not to threshold real/imag individually.
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


## mr_utils.cs.greedy.cosamp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/greedy/cosamp.py)

```
NAME
    mr_utils.cs.greedy.cosamp - Compressive sampling matching pursuit (CoSaMP) algorithm.

DESCRIPTION
    This implementation currently does not handle complex signals.

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


## mr_utils.cs.linear_programming

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/linear_programming.py)

```
NAME
    mr_utils.cs.linear_programming


```


## mr_utils.cs.models.UFT

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/models/UFT.py)

```
NAME
    mr_utils.cs.models.UFT - Undersampled Fourier transform encoding model.

DESCRIPTION
    I'm calling "encoding model" how we encode the image domain signal to get to
    the acquisiton domain.  In the case of MR, we measure k-space of the image we
    want, so the encoding model is simply the Fourier transform (ignoring all the
    other complications...).  This object provides methods to go into k-space and
    get back out assuming we undersample according to some mask.
    
    forward_ortho, inverse_ortho are probably the ones you want.

CLASSES
    builtins.object
        UFT
    
    class UFT(builtins.object)
     |  Undersampled Fourier Transform (UFT) data acquisiton model.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, samp)
     |      Initialize with binary sampling pattern.
     |  
     |  forward(self, x)
     |      Fourier encoding with binary undersampling pattern applied.
     |      
     |      This forward transform has no fftshift applied.
     |  
     |  forward_ortho(self, x)
     |      Normalized Fourier encoding with binary undersampling.
     |      
     |      This forward transform applied fftshift before FFT and after.
     |  
     |  forward_s(self, x)
     |      Fourier encoding with binary undersampling pattern applied.
     |      
     |      This forward transform applies fftshift before masking.
     |  
     |  inverse(self, x)
     |      Inverse fourier encoding.
     |  
     |  inverse_ortho(self, x)
     |      Inverse Normalized Fourier encoding.
     |      
     |      This transform applied ifftshift before and after ifft2.
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


## mr_utils.cs.thresholding.amp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/thresholding/amp.py)

```
NAME
    mr_utils.cs.thresholding.amp - 2D implementation of Approximate message passing algorithms.

DESCRIPTION
    See docstring of amp2d for reference implementation details.  It's companion
    is LCAMP.  What's interesting is that they circular shift in the transform
    domain.  I'm not sure why they do that, but empirically it seems to work!
    
    The wavelet transform is about what they are using.  I'm trying to keep the
    implementation as simple as possible, so I used a built in transform from
    PyWavelets that is close, but I'm not sure why it doesn't match up completely.

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


# DEFINITIONS
## mr_utils.definitions

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/definitions.py)

```
NAME
    mr_utils.definitions - Provide definitions of paths for root andapplications if they exist.

```


# GADGETRON
## mr_utils.gadgetron.client

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/client.py)

```
NAME
    mr_utils.gadgetron.client - Gadgetron client for running on network machines.

DESCRIPTION
    Adapted from https://github.com/gadgetron/gadgetron-python-ismrmrd-client.git
    Keeps same command line interface, but allows for import into scripts.

FUNCTIONS
    client(data, address=None, port=None, outfile=None, in_group='/dataset', out_group=None, config='default.xml', config_local=None, script=None, existing_modules=['numpy', 'scipy', 'h5py'], script_dir=None, verbose=False)
        Send acquisitions to Gadgetron.
        
        This client allows you to connect to a Gadgetron server and process data.
        
        data -- Input file with file extension or numpy array.
        address -- Hostname of Gadgetron. If not set, taken from profile config.
        port -- Port to connect to. If not set, taken from profile config.
        outfile -- If provided, output will be saved to file with this name.
        in_group -- If input is hdf5, input data group name.
        out_group -- Output group name if file is written.
        config -- Remote configuration file.
        config_local -- Local configuration file.
        script -- File path to the Python script to be bundled and transfered.
        existing_modules -- Python packages to exclude from bundling.
        script_dir -- Directory to send script on remote machine.
        verbose -- Verbose mode.
        
        out_group=None will use the current date as the group name.


```


## mr_utils.gadgetron.configs.default

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/configs/default.py)

```
NAME
    mr_utils.gadgetron.configs.default - Example Gadgetron config generation.

FUNCTIONS
    default()
        Default config file, default.xml.
        
        Generates:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/mri_core/config/default.xml


```


## mr_utils.gadgetron.configs.distributed

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/configs/distributed.py)

```
NAME
    mr_utils.gadgetron.configs.distributed - Example generation of distributed gadget configs.

FUNCTIONS
    distributed_default()
        Generates distributed_default.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/distributed/config/distributed_default.xml
    
    distributed_image_default()
        Generates distributed_image_default.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/distributed/config/distributed_image_default.xml


```


## mr_utils.gadgetron.configs.epi

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/configs/epi.py)

```
NAME
    mr_utils.gadgetron.configs.epi - Example EPI configurations.

FUNCTIONS
    epi()
        Generates epi.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/epi/epi.xml
    
    epi_gtplus_grappa()
        GT Plus configuration file for general 2D epi reconstruction.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/epi/epi_gtplus_grappa.xml


```


## mr_utils.gadgetron.configs.generic

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/configs/generic.py)

```
NAME
    mr_utils.gadgetron.configs.generic - Generic Gadgetron configuration files.

FUNCTIONS
    generic_cartesian_grappa()
        Generic_Cartesian_Grappa.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/mri_core/config/Generic_Cartesian_Grappa.xml


```


## mr_utils.gadgetron.configs.grappa

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/configs/grappa.py)

```
NAME
    mr_utils.gadgetron.configs.grappa - Gadgetron configs for GRAPPA gadgets.

FUNCTIONS
    grappa_cpu()
        Generates grappa_cpu.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_cpu.xml
    
    grappa_float_cpu()
        Generates grappa_float_cpu.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_float_cpu.xml
    
    grappa_unoptimized_cpu()
        Generates grappa_unoptimized_cpu.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_unoptimized.xml
    
    grappa_unoptimized_float_cpu()
        Generates grappa_unoptimized_float_cpu.xml.
        
        See:
            https://github.com/gadgetron/gadgetron/blob/master/gadgets/grappa/config/grappa_unoptimized_float.xml


```


## mr_utils.gadgetron.configs.python

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/configs/python.py)

```
NAME
    mr_utils.gadgetron.configs.python - Configs including python Gadgets.

FUNCTIONS
    python()
        python.xml
    
    python_short()
        python_short.xml


```


## mr_utils.gadgetron.gadgetron_config

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/gadgetron_config.py)

```
NAME
    mr_utils.gadgetron.gadgetron_config - Programmatically generate local configurations for Gadgetron.

DESCRIPTION
    Reconstruction pipelines can be created in the script, modified conditionally,
    etc...  Example config generation can be found in mr_utils.configs.

CLASSES
    builtins.object
        GadgetronConfig
    
    class GadgetronConfig(builtins.object)
     |  Holds config tree for Gadgetron reconstruction.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  add_gadget(self, name, classname=None, dll=None, props=None)
     |      Add gadget to config.
     |      
     |      Looks like:
     |      <gadget>
     |        <name>Acc</name>
     |        <dll>gadgetroncore</dll>
     |        <classname>AccumulatorGadget</classname>
     |      </gadget>
     |  
     |  add_reader(self, slot, classname, dll='gadgetron_mricore')
     |      Add a reader component.
     |      
     |      Looks like:
     |      <reader>
     |        <slot>1008</slot>
     |        <dll>gadgetroncore</dll>
     |        <classname>GadgetIsmrmrdAcquisitionMessageReader</classname>
     |      </reader>
     |  
     |  add_writer(self, slot, classname, dll='gadgetron_mricore')
     |      Add writer component.
     |      
     |      Looks like:
     |      <writer>
     |        <slot>1004</slot>
     |        <dll>gadgetroncore</dll>
     |        <classname>MRIImageWriterCPLX</classname>
     |      </writer>
     |  
     |  get_stream_config(self)
     |      Get XML header information for Gadgetron config.
     |      
     |      Looks like:
     |      <gadgetronStreamConfiguration
     |        xsi:schemaLocation="http://gadgetron.sf.net/gadgetron gadgetron.xsd"
     |        xmlns="http://gadgetron.sf.net/gadgetron"
     |        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
     |  
     |  print(self)
     |      Print xml string of config to console.
     |  
     |  tostring(self)
     |      Return xml string of GadgetronConfig.
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


## mr_utils.gadgetron.gtconnector

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/gtconnector.py)

```
NAME
    mr_utils.gadgetron.gtconnector

CLASSES
    builtins.object
        Connector
        MessageReader
            BlobMessageReader
                BlobAttribMessageReader
            ImageMessageReader
                ImageAttribMessageReader
    
    class BlobAttribMessageReader(BlobMessageReader)
     |  Method resolution order:
     |      BlobAttribMessageReader
     |      BlobMessageReader
     |      MessageReader
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  read(self, sock)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from BlobMessageReader:
     |  
     |  __init__(self, prefix, suffix)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from MessageReader:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class BlobMessageReader(MessageReader)
     |  Method resolution order:
     |      BlobMessageReader
     |      MessageReader
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, prefix, suffix)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  read(self, sock)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from MessageReader:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Connector(builtins.object)
     |  Methods defined here:
     |  
     |  __del__(self)
     |  
     |  __init__(self, hostname=None, port=None)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  connect(self, hostname, port)
     |  
     |  read_task(self)
     |  
     |  register_reader(self, kind, reader)
     |  
     |  register_writer(self, kind, writer)
     |  
     |  send_gadgetron_close(self)
     |  
     |  send_gadgetron_configuration_file(self, filename)
     |  
     |  send_gadgetron_configuration_script(self, contents)
     |  
     |  send_gadgetron_parameters(self, xml)
     |  
     |  send_ismrmrd_acquisition(self, acq)
     |  
     |  wait(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class ImageAttribMessageReader(ImageMessageReader)
     |  Method resolution order:
     |      ImageAttribMessageReader
     |      ImageMessageReader
     |      MessageReader
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  read(self, sock)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from ImageMessageReader:
     |  
     |  __init__(self, filename, groupname)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from MessageReader:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class ImageMessageReader(MessageReader)
     |  Method resolution order:
     |      ImageMessageReader
     |      MessageReader
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, filename, groupname)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  read(self, sock)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from MessageReader:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class MessageReader(builtins.object)
     |  Methods defined here:
     |  
     |  read(self, sock)
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
    readsock(sock, bytecount)
        Reads a specific number of bytes from a socket

```


## mr_utils.gadgetron.ssh_tunnel

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gadgetron/ssh_tunnel.py)

```
NAME
    mr_utils.gadgetron.ssh_tunnel - ## Let's make an ssh tunnel if we find it in profiles.config


```


# GRIDDING
## mr_utils.gridding.scgrog.get_gx_gy

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gridding/scgrog/get_gx_gy.py)

```
NAME
    mr_utils.gridding.scgrog.get_gx_gy - Self calibrating GROG GRAPPA kernels.

DESCRIPTION
    Based on the MATLAB implementation found here:
        https://github.com/edibella/Reconstruction/blob/master/%2BGROG/get_Gx_Gy.m

FUNCTIONS
    get_gx_gy(kspace, traj=None, kxs=None, kys=None, cartdims=None)
        Compute Self Calibrating GRAPPA Gx and Gy operators.


```


## mr_utils.gridding.scgrog.scgrog

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/gridding/scgrog/scgrog.py)

```
NAME
    mr_utils.gridding.scgrog.scgrog - Self calibrating GROG implementation.

DESCRIPTION
    Based on the MATLAB GROG implementation found here:
        https://github.com/edibella/Reconstruction

FUNCTIONS
    grog_interp(kspace, Gx, Gy, traj, cartdims)
        Moves radial k-space points onto a cartesian grid via the GROG method.
        
        kspace -- A 3D (sx,sor,soc) slice of k-space
        Gx,Gy -- The unit horizontal and vertical cartesian GRAPPA kernels
        traj -- k-space trajectory
        cartdims -- (nrows,ncols), size of Cartesian grid
    
    scgrog(kspace, traj, Gx, Gy, cartdims=None)
        Self calibrating GROG interpolation.
        
        kspace -- A 4D (sx,sor,nof,soc) matrix of complex k-space data.
        traj -- k-space trajectory.
        Gx,Gy -- The unit horizontal and vertical cartesian GRAPPA kernels.
        cartdims -- Size of Cartesian grid.
        
        If cartdims=None, we'll guess the Cartesian dimensions are
        (kspace.shape[0], kspace.shape[0], kspace.shape[2], kspace.shape[3]).


```


# LOAD_DATA
## mr_utils.load_data.hdf5

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/hdf5.py)

```
NAME
    mr_utils.load_data.hdf5

FUNCTIONS
    load_hdf5(filename)


```


## mr_utils.load_data.mat

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/mat.py)

```
NAME
    mr_utils.load_data.mat - Load data from MATLAB file type.

DESCRIPTION
    Uses scipy.io.loadmat to load recent versions of .MAT files.  Version 7.3 is
    supported.  It'll try to make some intelligent guesses if it runs into
    trouble, meaning, 'it will die trying!'.  If you don't like that philosophy,
    go ahead and use scipy.io.loadmat directly.

FUNCTIONS
    deal_with_7_3(data)
        Clean up data structures for MATLAB 7.3.
        
        Version 7.3 has a structured datatype that needs to be translated as a
        complex number.
    
    load_mat(filename, key=None)
        Load data from .MAT file.
        
        filename -- path to .mat file.
        key -- Specific key to extract.
        
        If key=None, all keys will be extracted.  If there is only one key, then
        its value will be provided directly, no dictionary will be returned.


```


## mr_utils.load_data.npy

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/npy.py)

```
NAME
    mr_utils.load_data.npy

FUNCTIONS
    load_npy(filename)


```


## mr_utils.load_data.pyport

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/pyport.py)

```
NAME
    mr_utils.load_data.pyport - Python port of siemens_to_ismrmrd.

DESCRIPTION
    Notes:
        The XProtocol parser (xprot_get_val) is a string-search based
        implementation, not an actual parser, so it's really slow, but does get
        the job done very well.  Next steps would be to figure out how to speed
        this up or rewrite the parser to work with everything.  I was working on a
        parser but was stuck on how to handle some of Siemens' very strange
        syntax.
    
        There are several different XML libraries being used.  xml.etree was my
        preference, so that's what I started with.  I needed to use xmltodict to
        convert between dictionaries and xml, because it's quicker/easier to have
        a dictionary hold the config information as we move along.  It turns out
        that schema verification is not supported by xml.etree, so that's when I
        pulled in lxml.etree -- so there's some weirdness trying to get xml.etree
        and lxml.etree to play together nicely.  The last  one is pybx -- a
        bizarrely complicated library that the ismrmrd python library uses.  I hate
        the thing and think it's overly complicated for what we need to use it for.
    
        One of the ideas I had was to pull down the schema/parammaps from the
        interwebs so it would always be current.  While this is a neat feature that
        probably no one will use, it would speed up the raw data conversion to use
        a local copy instead, even if that means pulling it down the first time and
        keeping it.
    
        The script to read in an ismrmrd dset provided in ismrmrd-python-tools is
        great at illustrating how to do it, but is incredibly slow, especiailly if
        you want to remove oversampling in readout direction.  Next steps are to
        figure out how to quickly read in and process these datasets.  I'm kind of
        put off from using this data format because of how unweildy it is, but I
        suppose it's better to be an open standards player...
    
        The only datasets I have are cartesian VB17.  So there's currently little
        support for anything else.
    
        Command-line interface has not been looked at in a long time, might not be
        working still.

FUNCTIONS
    pyport(version=False, list_embed=False, extract=None, user_stylesheet=None, file=None, pMapStyle=None, measNum=1, pMap=None, user_map=None, debug=False, header_only=False, output='output.h5', flash_pat_ref_scan=False, append_buffers=False, study_date_user_supplied='')
        Run the program with arguments.

```


## mr_utils.load_data.raw

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/raw.py)

```
NAME
    mr_utils.load_data.raw

FUNCTIONS
    load_raw(filename, use='bart', bart_args='-A', s2i_ROS=True, as_ismrmrd=False)
        Load Siemens raw data into numpy array.
        
        filename -- File path and filename of raw data file.
        use -- Method to use to read in raw data.
        bart_args -- Arguments to pass to BART.
        s2i_ROS -- Remove oversampling in readout when using use='s2i'.
        as_ismrmrd -- Leave as ismrmrd data type.
        
        use:
            bart -- BART twix raw data reader
            s2i -- siemens_to_ismrmrd
            rdi -- rawdatarinator

```


## mr_utils.load_data.s2i.channel_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/channel_header.py)

```
NAME
    mr_utils.load_data.s2i.channel_header - Holds header data for a single channel.

```


## mr_utils.load_data.s2i.channel_header_and_data

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/channel_header_and_data.py)

```
NAME
    mr_utils.load_data.s2i.channel_header_and_data - Struct to hold both header and data for a single channel.

CLASSES
    builtins.object
        ChannelHeaderAndData
    
    class ChannelHeaderAndData(builtins.object)
     |  Class to hold channel header and data.
     |  
     |  We don't know what the size of the data will be, so we don't create an
     |  np.dtype for this structure.  Instead, since it's just a top
     |  level container, we're fine with just a python class.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
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


## mr_utils.load_data.s2i.defs

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/defs.py)

```
NAME
    mr_utils.load_data.s2i.defs - Constant definitions used by siemens_to_ismrmrd.

```


## mr_utils.load_data.s2i.fill_ismrmrd_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/fill_ismrmrd_header.py)

```
NAME
    mr_utils.load_data.s2i.fill_ismrmrd_header - fill_ismrmrd_header

DESCRIPTION
    This is currently not working and silently failing.

FUNCTIONS
    fill_ismrmrd_header(h, study_date, study_time)
        Add dates/times to ISMRMRD header.


```


## mr_utils.load_data.s2i.get_acquisition

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/get_acquisition.py)

```
NAME
    mr_utils.load_data.s2i.get_acquisition - Populate ISMRMRD Acquisition object with data from ChannelHeaderAndData.

FUNCTIONS
    getAcquisition(flash_pat_ref_scan, trajectory, dwell_time_0, max_channels, _isAdjustCoilSens, _isAdjQuietCoilSens, _isVB, traj, scanhead, channels)
        Create ISMRMRD acqusition object for the current channel data.


```


## mr_utils.load_data.s2i.mdh

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/mdh.py)

```
NAME
    mr_utils.load_data.s2i.mdh - All MDH related structures.

```


## mr_utils.load_data.s2i.parse_xml

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/parse_xml.py)

```
NAME
    mr_utils.load_data.s2i.parse_xml - parseXML

FUNCTIONS
    parseXML(debug_xml, parammap_xsl_content, _schema_file_name_content, xml_config)
        Apply XSLT.


```


## mr_utils.load_data.s2i.process_parameter_map

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/process_parameter_map.py)

```
NAME
    mr_utils.load_data.s2i.process_parameter_map - ProcessParameterMap

FUNCTIONS
    ProcessParameterMap(config_buffer, parammap_file_content)
        Fill in the headers of all parammap_file's fields.
    
    reduce(...)
        reduce(function, sequence[, initial]) -> value
        
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.


```


## mr_utils.load_data.s2i.read_channel_headers

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_channel_headers.py)

```
NAME
    mr_utils.load_data.s2i.read_channel_headers - Store data and header for each channel.

FUNCTIONS
    readChannelHeaders(siemens_dat, VBFILE, scanhead)
        Read the headers for the channels.

```


## mr_utils.load_data.s2i.read_measurement_header_buffers

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_measurement_header_buffers.py)

```
NAME
    mr_utils.load_data.s2i.read_measurement_header_buffers - readMeasurementHeaderBuffers

FUNCTIONS
    readMeasurementHeaderBuffers(siemens_dat, num_buffers)
        Filler.


```


## mr_utils.load_data.s2i.read_parc_file_entries

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_parc_file_entries.py)

```
NAME
    mr_utils.load_data.s2i.read_parc_file_entries - readParcFileEntries

FUNCTIONS
    readParcFileEntries(siemens_dat, ParcRaidHead, VBFILE)
        struct MrParcRaidFileEntry
        {
          uint32_t measId_;
          uint32_t fileId_;
          uint64_t off_;
          uint64_t len_;
          char patName_[64];
          char protName_[64];
        };


```


## mr_utils.load_data.s2i.read_scan_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_scan_header.py)

```
NAME
    mr_utils.load_data.s2i.read_scan_header - readScanHeader

FUNCTIONS
    readScanHeader(siemens_dat, VBFILE)
        Read the header from the scan.

```


## mr_utils.load_data.s2i.read_xml_config

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_xml_config.py)

```
NAME
    mr_utils.load_data.s2i.read_xml_config - readXmlConfig

FUNCTIONS
    readXmlConfig(debug_xml, parammap_file_content, num_buffers, buffers, wip_double, trajectory, dwell_time_0, max_channels, radial_views, baseLineString, protocol_name)
        Read in and format header from raw data file.


```


## mr_utils.load_data.s2i.regex_parser

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/regex_parser.py)

```
NAME
    mr_utils.load_data.s2i.regex_parser - Make a parser using regex.

DESCRIPTION
    Let's see how this goes...

CLASSES
    builtins.object
        Parser
    
    class Parser(builtins.object)
     |  Parse XProtocol.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  isconsistent(self)
     |      Make sure cur_rule is a subset of some rule.
     |  
     |  isrule(self)
     |      Check to see if cur_rule is a rule.
     |  
     |  istoken(self)
     |      Check to see if cur_token is a token.
     |  
     |  parse(self, buf)
     |      Parse buffer into dictionary.
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


## mr_utils.load_data.s2i.scan_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/scan_header.py)

```
NAME
    mr_utils.load_data.s2i.scan_header - Structure to hold the header of a scan.

```


## mr_utils.load_data.s2i.xml_fun

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/xml_fun.py)

```
NAME
    mr_utils.load_data.s2i.xml_fun - All the XML related functions required by siemens_to_ismrmrd.

FUNCTIONS
    get_embedded_file(file)
        Retrieve embedded file from github.
        
        file -- Name of embedded file to get.
    
    get_ismrmrd_schema(method='ET')
        Download XSD file from ISMRMD git repo.
    
    get_list_of_embedded_files()
        List of files to go try to find from the git repo.
    
    getparammap_file_content(parammap_file, usermap_file, VBFILE)
        Filler.


```


## mr_utils.load_data.s2i.xprot_parser_strsearch

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/xprot_parser_strsearch.py)

```
NAME
    mr_utils.load_data.s2i.xprot_parser_strsearch - Quick and lazy -- only read what we need from the XProtocol header.

DESCRIPTION
    This is a way engineered to Get the Job Done(TM).  It could be made a lot
    better and faster, but right now I'm just trying to get it working after the
    debacle with ply...
    
    The lookup table seems like a good idea, but having a little trouble getting it
    to work properly.  Currently it's supressing a lot of fields that don't exist,
    it's just not letting us display the warning that it doesn't exist.

FUNCTIONS
    find_matching_braces(s, lsym='{', rsym='}', qlsym='"', qrsym='"')
        Given string s, find indices of matching braces.
    
    findp(p, config)
        Decode the tag and return index.
        
        p -- Current path node.
        config -- The current header portion we're searching in.
        
        All of these tag assignments are ad hoc -- just to get something to work.
    
    xprot_get_val(config_buffer, val, p_to_buf_table=None, return_table=False)
        Get value from config buffer.
        
        config_buffer -- String containing the XProtocol innards.
        val -- Dot separated path to search for.
        p_to_buf_table --
        return_table --


```


## mr_utils.load_data.siemens_to_ismrmd_client

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/siemens_to_ismrmd_client.py)

```
NAME
    mr_utils.load_data.siemens_to_ismrmd_client

CLASSES
    paramiko.transport.Transport(threading.Thread, paramiko.util.ClosingContextManager)
        FastTransport
    tqdm._tqdm.tqdm(builtins.object)
        TqdmWrap
    
    class FastTransport(paramiko.transport.Transport)
     |  An SSH Transport attaches to a stream (usually a socket), negotiates an
     |  encrypted session, authenticates, and then creates stream tunnels, called
     |  `channels <.Channel>`, across the session.  Multiple channels can be
     |  multiplexed across a single session (and often are, in the case of port
     |  forwardings).
     |  
     |  Instances of this class may be used as context managers.
     |  
     |  Method resolution order:
     |      FastTransport
     |      paramiko.transport.Transport
     |      threading.Thread
     |      paramiko.util.ClosingContextManager
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, sock)
     |      Increase window size in hopes to go faster...
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from paramiko.transport.Transport:
     |  
     |  __repr__(self)
     |      Returns a string representation of this object, for debugging.
     |  
     |  accept(self, timeout=None)
     |      Return the next channel opened by the client over this transport, in
     |      server mode.  If no channel is opened before the given timeout,
     |      ``None`` is returned.
     |      
     |      :param int timeout:
     |          seconds to wait for a channel, or ``None`` to wait forever
     |      :return: a new `.Channel` opened by the client
     |  
     |  add_server_key(self, key)
     |      Add a host key to the list of keys used for server mode.  When behaving
     |      as a server, the host key is used to sign certain packets during the
     |      SSH2 negotiation, so that the client can trust that we are who we say
     |      we are.  Because this is used for signing, the key must contain private
     |      key info, not just the public half.  Only one key of each type (RSA or
     |      DSS) is kept.
     |      
     |      :param .PKey key:
     |          the host key to add, usually an `.RSAKey` or `.DSSKey`.
     |  
     |  atfork(self)
     |      Terminate this Transport without closing the session.  On posix
     |      systems, if a Transport is open during process forking, both parent
     |      and child will share the underlying socket, but only one process can
     |      use the connection (without corrupting the session).  Use this method
     |      to clean up a Transport object without disrupting the other process.
     |      
     |      .. versionadded:: 1.5.3
     |  
     |  auth_gssapi_keyex(self, username)
     |      Authenticate to the server with GSS-API/SSPI if GSS-API kex is in use.
     |      
     |      :param str username: The username to authenticate as.
     |      :returns:
     |          a list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      :raises: `.BadAuthenticationType` --
     |          if GSS-API Key Exchange was not performed (and no event was passed
     |          in)
     |      :raises: `.AuthenticationException` --
     |          if the authentication failed (and no event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  auth_gssapi_with_mic(self, username, gss_host, gss_deleg_creds)
     |      Authenticate to the Server using GSS-API / SSPI.
     |      
     |      :param str username: The username to authenticate as
     |      :param str gss_host: The target host
     |      :param bool gss_deleg_creds: Delegate credentials or not
     |      :return: list of auth types permissible for the next stage of
     |               authentication (normally empty)
     |      :raises: `.BadAuthenticationType` -- if gssapi-with-mic isn't
     |          allowed by the server (and no event was passed in)
     |      :raises:
     |          `.AuthenticationException` -- if the authentication failed (and no
     |          event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  auth_interactive(self, username, handler, submethods='')
     |      Authenticate to the server interactively.  A handler is used to answer
     |      arbitrary questions from the server.  On many servers, this is just a
     |      dumb wrapper around PAM.
     |      
     |      This method will block until the authentication succeeds or fails,
     |      peroidically calling the handler asynchronously to get answers to
     |      authentication questions.  The handler may be called more than once
     |      if the server continues to ask questions.
     |      
     |      The handler is expected to be a callable that will handle calls of the
     |      form: ``handler(title, instructions, prompt_list)``.  The ``title`` is
     |      meant to be a dialog-window title, and the ``instructions`` are user
     |      instructions (both are strings).  ``prompt_list`` will be a list of
     |      prompts, each prompt being a tuple of ``(str, bool)``.  The string is
     |      the prompt and the boolean indicates whether the user text should be
     |      echoed.
     |      
     |      A sample call would thus be:
     |      ``handler('title', 'instructions', [('Password:', False)])``.
     |      
     |      The handler should return a list or tuple of answers to the server's
     |      questions.
     |      
     |      If the server requires multi-step authentication (which is very rare),
     |      this method will return a list of auth types permissible for the next
     |      step.  Otherwise, in the normal case, an empty list is returned.
     |      
     |      :param str username: the username to authenticate as
     |      :param callable handler: a handler for responding to server questions
     |      :param str submethods: a string list of desired submethods (optional)
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty).
     |      
     |      :raises: `.BadAuthenticationType` -- if public-key authentication isn't
     |          allowed by the server for this user
     |      :raises: `.AuthenticationException` -- if the authentication failed
     |      :raises: `.SSHException` -- if there was a network error
     |      
     |      .. versionadded:: 1.5
     |  
     |  auth_interactive_dumb(self, username, handler=None, submethods='')
     |      Autenticate to the server interactively but dumber.
     |      Just print the prompt and / or instructions to stdout and send back
     |      the response. This is good for situations where partial auth is
     |      achieved by key and then the user has to enter a 2fac token.
     |  
     |  auth_none(self, username)
     |      Try to authenticate to the server using no authentication at all.
     |      This will almost always fail.  It may be useful for determining the
     |      list of authentication types supported by the server, by catching the
     |      `.BadAuthenticationType` exception raised.
     |      
     |      :param str username: the username to authenticate as
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      
     |      :raises:
     |          `.BadAuthenticationType` -- if "none" authentication isn't allowed
     |          by the server for this user
     |      :raises:
     |          `.SSHException` -- if the authentication failed due to a network
     |          error
     |      
     |      .. versionadded:: 1.5
     |  
     |  auth_password(self, username, password, event=None, fallback=True)
     |      Authenticate to the server using a password.  The username and password
     |      are sent over an encrypted link.
     |      
     |      If an ``event`` is passed in, this method will return immediately, and
     |      the event will be triggered once authentication succeeds or fails.  On
     |      success, `is_authenticated` will return ``True``.  On failure, you may
     |      use `get_exception` to get more detailed error information.
     |      
     |      Since 1.1, if no event is passed, this method will block until the
     |      authentication succeeds or fails.  On failure, an exception is raised.
     |      Otherwise, the method simply returns.
     |      
     |      Since 1.5, if no event is passed and ``fallback`` is ``True`` (the
     |      default), if the server doesn't support plain password authentication
     |      but does support so-called "keyboard-interactive" mode, an attempt
     |      will be made to authenticate using this interactive mode.  If it fails,
     |      the normal exception will be thrown as if the attempt had never been
     |      made.  This is useful for some recent Gentoo and Debian distributions,
     |      which turn off plain password authentication in a misguided belief
     |      that interactive authentication is "more secure".  (It's not.)
     |      
     |      If the server requires multi-step authentication (which is very rare),
     |      this method will return a list of auth types permissible for the next
     |      step.  Otherwise, in the normal case, an empty list is returned.
     |      
     |      :param str username: the username to authenticate as
     |      :param basestring password: the password to authenticate with
     |      :param .threading.Event event:
     |          an event to trigger when the authentication attempt is complete
     |          (whether it was successful or not)
     |      :param bool fallback:
     |          ``True`` if an attempt at an automated "interactive" password auth
     |          should be made if the server doesn't support normal password auth
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      
     |      :raises:
     |          `.BadAuthenticationType` -- if password authentication isn't
     |          allowed by the server for this user (and no event was passed in)
     |      :raises:
     |          `.AuthenticationException` -- if the authentication failed (and no
     |          event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  auth_publickey(self, username, key, event=None)
     |      Authenticate to the server using a private key.  The key is used to
     |      sign data from the server, so it must include the private part.
     |      
     |      If an ``event`` is passed in, this method will return immediately, and
     |      the event will be triggered once authentication succeeds or fails.  On
     |      success, `is_authenticated` will return ``True``.  On failure, you may
     |      use `get_exception` to get more detailed error information.
     |      
     |      Since 1.1, if no event is passed, this method will block until the
     |      authentication succeeds or fails.  On failure, an exception is raised.
     |      Otherwise, the method simply returns.
     |      
     |      If the server requires multi-step authentication (which is very rare),
     |      this method will return a list of auth types permissible for the next
     |      step.  Otherwise, in the normal case, an empty list is returned.
     |      
     |      :param str username: the username to authenticate as
     |      :param .PKey key: the private key to authenticate with
     |      :param .threading.Event event:
     |          an event to trigger when the authentication attempt is complete
     |          (whether it was successful or not)
     |      :return:
     |          list of auth types permissible for the next stage of
     |          authentication (normally empty)
     |      
     |      :raises:
     |          `.BadAuthenticationType` -- if public-key authentication isn't
     |          allowed by the server for this user (and no event was passed in)
     |      :raises:
     |          `.AuthenticationException` -- if the authentication failed (and no
     |          event was passed in)
     |      :raises: `.SSHException` -- if there was a network error
     |  
     |  cancel_port_forward(self, address, port)
     |      Ask the server to cancel a previous port-forwarding request.  No more
     |      connections to the given address & port will be forwarded across this
     |      ssh connection.
     |      
     |      :param str address: the address to stop forwarding
     |      :param int port: the port to stop forwarding
     |  
     |  close(self)
     |      Close this session, and any open channels that are tied to it.
     |  
     |  connect(self, hostkey=None, username='', password=None, pkey=None, gss_host=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_trust_dns=True)
     |      Negotiate an SSH2 session, and optionally verify the server's host key
     |      and authenticate using a password or private key.  This is a shortcut
     |      for `start_client`, `get_remote_server_key`, and
     |      `Transport.auth_password` or `Transport.auth_publickey`.  Use those
     |      methods if you want more control.
     |      
     |      You can use this method immediately after creating a Transport to
     |      negotiate encryption with a server.  If it fails, an exception will be
     |      thrown.  On success, the method will return cleanly, and an encrypted
     |      session exists.  You may immediately call `open_channel` or
     |      `open_session` to get a `.Channel` object, which is used for data
     |      transfer.
     |      
     |      .. note::
     |          If you fail to supply a password or private key, this method may
     |          succeed, but a subsequent `open_channel` or `open_session` call may
     |          fail because you haven't authenticated yet.
     |      
     |      :param .PKey hostkey:
     |          the host key expected from the server, or ``None`` if you don't
     |          want to do host key verification.
     |      :param str username: the username to authenticate as.
     |      :param str password:
     |          a password to use for authentication, if you want to use password
     |          authentication; otherwise ``None``.
     |      :param .PKey pkey:
     |          a private key to use for authentication, if you want to use private
     |          key authentication; otherwise ``None``.
     |      :param str gss_host:
     |          The target's name in the kerberos database. Default: hostname
     |      :param bool gss_auth:
     |          ``True`` if you want to use GSS-API authentication.
     |      :param bool gss_kex:
     |          Perform GSS-API Key Exchange and user authentication.
     |      :param bool gss_deleg_creds:
     |          Whether to delegate GSS-API client credentials.
     |      :param gss_trust_dns:
     |          Indicates whether or not the DNS is trusted to securely
     |          canonicalize the name of the host being connected to (default
     |          ``True``).
     |      
     |      :raises: `.SSHException` -- if the SSH2 negotiation fails, the host key
     |          supplied by the server is incorrect, or authentication fails.
     |      
     |      .. versionchanged:: 2.3
     |          Added the ``gss_trust_dns`` argument.
     |  
     |  get_banner(self)
     |      Return the banner supplied by the server upon connect. If no banner is
     |      supplied, this method returns ``None``.
     |      
     |      :returns: server supplied banner (`str`), or ``None``.
     |      
     |      .. versionadded:: 1.13
     |  
     |  get_exception(self)
     |      Return any exception that happened during the last server request.
     |      This can be used to fetch more specific error information after using
     |      calls like `start_client`.  The exception (if any) is cleared after
     |      this call.
     |      
     |      :return:
     |          an exception, or ``None`` if there is no stored exception.
     |      
     |      .. versionadded:: 1.1
     |  
     |  get_hexdump(self)
     |      Return ``True`` if the transport is currently logging hex dumps of
     |      protocol traffic.
     |      
     |      :return: ``True`` if hex dumps are being logged, else ``False``.
     |      
     |      .. versionadded:: 1.4
     |  
     |  get_log_channel(self)
     |      Return the channel name used for this transport's logging.
     |      
     |      :return: channel name as a `str`
     |      
     |      .. versionadded:: 1.2
     |  
     |  get_remote_server_key(self)
     |      Return the host key of the server (in client mode).
     |      
     |      .. note::
     |          Previously this call returned a tuple of ``(key type, key
     |          string)``. You can get the same effect by calling `.PKey.get_name`
     |          for the key type, and ``str(key)`` for the key string.
     |      
     |      :raises: `.SSHException` -- if no session is currently active.
     |      
     |      :return: public key (`.PKey`) of the remote server
     |  
     |  get_security_options(self)
     |      Return a `.SecurityOptions` object which can be used to tweak the
     |      encryption algorithms this transport will permit (for encryption,
     |      digest/hash operations, public keys, and key exchanges) and the order
     |      of preference for them.
     |  
     |  get_server_key(self)
     |      Return the active host key, in server mode.  After negotiating with the
     |      client, this method will return the negotiated host key.  If only one
     |      type of host key was set with `add_server_key`, that's the only key
     |      that will ever be returned.  But in cases where you have set more than
     |      one type of host key (for example, an RSA key and a DSS key), the key
     |      type will be negotiated by the client, and this method will return the
     |      key of the type agreed on.  If the host key has not been negotiated
     |      yet, ``None`` is returned.  In client mode, the behavior is undefined.
     |      
     |      :return:
     |          host key (`.PKey`) of the type negotiated by the client, or
     |          ``None``.
     |  
     |  get_username(self)
     |      Return the username this connection is authenticated for.  If the
     |      session is not authenticated (or authentication failed), this method
     |      returns ``None``.
     |      
     |      :return: username that was authenticated (a `str`), or ``None``.
     |  
     |  getpeername(self)
     |      Return the address of the remote side of this Transport, if possible.
     |      
     |      This is effectively a wrapper around ``getpeername`` on the underlying
     |      socket.  If the socket-like object has no ``getpeername`` method, then
     |      ``("unknown", 0)`` is returned.
     |      
     |      :return:
     |          the address of the remote host, if known, as a ``(str, int)``
     |          tuple.
     |  
     |  global_request(self, kind, data=None, wait=True)
     |      Make a global request to the remote host.  These are normally
     |      extensions to the SSH2 protocol.
     |      
     |      :param str kind: name of the request.
     |      :param tuple data:
     |          an optional tuple containing additional data to attach to the
     |          request.
     |      :param bool wait:
     |          ``True`` if this method should not return until a response is
     |          received; ``False`` otherwise.
     |      :return:
     |          a `.Message` containing possible additional data if the request was
     |          successful (or an empty `.Message` if ``wait`` was ``False``);
     |          ``None`` if the request was denied.
     |  
     |  is_active(self)
     |      Return true if this session is active (open).
     |      
     |      :return:
     |          True if the session is still active (open); False if the session is
     |          closed
     |  
     |  is_authenticated(self)
     |      Return true if this session is active and authenticated.
     |      
     |      :return:
     |          True if the session is still open and has been authenticated
     |          successfully; False if authentication failed and/or the session is
     |          closed.
     |  
     |  open_channel(self, kind, dest_addr=None, src_addr=None, window_size=None, max_packet_size=None, timeout=None)
     |      Request a new channel to the server. `Channels <.Channel>` are
     |      socket-like objects used for the actual transfer of data across the
     |      session. You may only request a channel after negotiating encryption
     |      (using `connect` or `start_client`) and authenticating.
     |      
     |      .. note:: Modifying the the window and packet sizes might have adverse
     |          effects on the channel created. The default values are the same
     |          as in the OpenSSH code base and have been battle tested.
     |      
     |      :param str kind:
     |          the kind of channel requested (usually ``"session"``,
     |          ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``)
     |      :param tuple dest_addr:
     |          the destination address (address + port tuple) of this port
     |          forwarding, if ``kind`` is ``"forwarded-tcpip"`` or
     |          ``"direct-tcpip"`` (ignored for other channel types)
     |      :param src_addr: the source address of this port forwarding, if
     |          ``kind`` is ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``
     |      :param int window_size:
     |          optional window size for this session.
     |      :param int max_packet_size:
     |          optional max packet size for this session.
     |      :param float timeout:
     |          optional timeout opening a channel, default 3600s (1h)
     |      
     |      :return: a new `.Channel` on success
     |      
     |      :raises:
     |          `.SSHException` -- if the request is rejected, the session ends
     |          prematurely or there is a timeout openning a channel
     |      
     |      .. versionchanged:: 1.15
     |          Added the ``window_size`` and ``max_packet_size`` arguments.
     |  
     |  open_forward_agent_channel(self)
     |      Request a new channel to the client, of type
     |      ``"auth-agent@openssh.com"``.
     |      
     |      This is just an alias for ``open_channel('auth-agent@openssh.com')``.
     |      
     |      :return: a new `.Channel`
     |      
     |      :raises: `.SSHException` --
     |          if the request is rejected or the session ends prematurely
     |  
     |  open_forwarded_tcpip_channel(self, src_addr, dest_addr)
     |      Request a new channel back to the client, of type ``forwarded-tcpip``.
     |      
     |      This is used after a client has requested port forwarding, for sending
     |      incoming connections back to the client.
     |      
     |      :param src_addr: originator's address
     |      :param dest_addr: local (server) connected address
     |  
     |  open_session(self, window_size=None, max_packet_size=None, timeout=None)
     |      Request a new channel to the server, of type ``"session"``.  This is
     |      just an alias for calling `open_channel` with an argument of
     |      ``"session"``.
     |      
     |      .. note:: Modifying the the window and packet sizes might have adverse
     |          effects on the session created. The default values are the same
     |          as in the OpenSSH code base and have been battle tested.
     |      
     |      :param int window_size:
     |          optional window size for this session.
     |      :param int max_packet_size:
     |          optional max packet size for this session.
     |      
     |      :return: a new `.Channel`
     |      
     |      :raises:
     |          `.SSHException` -- if the request is rejected or the session ends
     |          prematurely
     |      
     |      .. versionchanged:: 1.13.4/1.14.3/1.15.3
     |          Added the ``timeout`` argument.
     |      .. versionchanged:: 1.15
     |          Added the ``window_size`` and ``max_packet_size`` arguments.
     |  
     |  open_sftp_client(self)
     |      Create an SFTP client channel from an open transport.  On success, an
     |      SFTP session will be opened with the remote host, and a new
     |      `.SFTPClient` object will be returned.
     |      
     |      :return:
     |          a new `.SFTPClient` referring to an sftp session (channel) across
     |          this transport
     |  
     |  open_x11_channel(self, src_addr=None)
     |      Request a new channel to the client, of type ``"x11"``.  This
     |      is just an alias for ``open_channel('x11', src_addr=src_addr)``.
     |      
     |      :param tuple src_addr:
     |          the source address (``(str, int)``) of the x11 server (port is the
     |          x11 port, ie. 6010)
     |      :return: a new `.Channel`
     |      
     |      :raises:
     |          `.SSHException` -- if the request is rejected or the session ends
     |          prematurely
     |  
     |  renegotiate_keys(self)
     |      Force this session to switch to new keys.  Normally this is done
     |      automatically after the session hits a certain number of packets or
     |      bytes sent or received, but this method gives you the option of forcing
     |      new keys whenever you want.  Negotiating new keys causes a pause in
     |      traffic both ways as the two sides swap keys and do computations.  This
     |      method returns when the session has switched to new keys.
     |      
     |      :raises:
     |          `.SSHException` -- if the key renegotiation failed (which causes
     |          the session to end)
     |  
     |  request_port_forward(self, address, port, handler=None)
     |      Ask the server to forward TCP connections from a listening port on
     |      the server, across this SSH session.
     |      
     |      If a handler is given, that handler is called from a different thread
     |      whenever a forwarded connection arrives.  The handler parameters are::
     |      
     |          handler(
     |              channel,
     |              (origin_addr, origin_port),
     |              (server_addr, server_port),
     |          )
     |      
     |      where ``server_addr`` and ``server_port`` are the address and port that
     |      the server was listening on.
     |      
     |      If no handler is set, the default behavior is to send new incoming
     |      forwarded connections into the accept queue, to be picked up via
     |      `accept`.
     |      
     |      :param str address: the address to bind when forwarding
     |      :param int port:
     |          the port to forward, or 0 to ask the server to allocate any port
     |      :param callable handler:
     |          optional handler for incoming forwarded connections, of the form
     |          ``func(Channel, (str, int), (str, int))``.
     |      
     |      :return: the port number (`int`) allocated by the server
     |      
     |      :raises:
     |          `.SSHException` -- if the server refused the TCP forward request
     |  
     |  run(self)
     |      Method representing the thread's activity.
     |      
     |      You may override this method in a subclass. The standard run() method
     |      invokes the callable object passed to the object's constructor as the
     |      target argument, if any, with sequential and keyword arguments taken
     |      from the args and kwargs arguments, respectively.
     |  
     |  send_ignore(self, byte_count=None)
     |      Send a junk packet across the encrypted link.  This is sometimes used
     |      to add "noise" to a connection to confuse would-be attackers.  It can
     |      also be used as a keep-alive for long lived connections traversing
     |      firewalls.
     |      
     |      :param int byte_count:
     |          the number of random bytes to send in the payload of the ignored
     |          packet -- defaults to a random number from 10 to 41.
     |  
     |  set_gss_host(self, gss_host, trust_dns=True, gssapi_requested=True)
     |      Normalize/canonicalize ``self.gss_host`` depending on various factors.
     |      
     |      :param str gss_host:
     |          The explicitly requested GSS-oriented hostname to connect to (i.e.
     |          what the host's name is in the Kerberos database.) Defaults to
     |          ``self.hostname`` (which will be the 'real' target hostname and/or
     |          host portion of given socket object.)
     |      :param bool trust_dns:
     |          Indicates whether or not DNS is trusted; if true, DNS will be used
     |          to canonicalize the GSS hostname (which again will either be
     |          ``gss_host`` or the transport's default hostname.)
     |          (Defaults to True due to backwards compatibility.)
     |      :param bool gssapi_requested:
     |          Whether GSSAPI key exchange or authentication was even requested.
     |          If not, this is a no-op and nothing happens
     |          (and ``self.gss_host`` is not set.)
     |          (Defaults to True due to backwards compatibility.)
     |      :returns: ``None``.
     |  
     |  set_hexdump(self, hexdump)
     |      Turn on/off logging a hex dump of protocol traffic at DEBUG level in
     |      the logs.  Normally you would want this off (which is the default),
     |      but if you are debugging something, it may be useful.
     |      
     |      :param bool hexdump:
     |          ``True`` to log protocol traffix (in hex) to the log; ``False``
     |          otherwise.
     |  
     |  set_keepalive(self, interval)
     |      Turn on/off keepalive packets (default is off).  If this is set, after
     |      ``interval`` seconds without sending any data over the connection, a
     |      "keepalive" packet will be sent (and ignored by the remote host).  This
     |      can be useful to keep connections alive over a NAT, for example.
     |      
     |      :param int interval:
     |          seconds to wait before sending a keepalive packet (or
     |          0 to disable keepalives).
     |  
     |  set_log_channel(self, name)
     |      Set the channel for this transport's logging.  The default is
     |      ``"paramiko.transport"`` but it can be set to anything you want. (See
     |      the `.logging` module for more info.)  SSH Channels will log to a
     |      sub-channel of the one specified.
     |      
     |      :param str name: new channel name for logging
     |      
     |      .. versionadded:: 1.1
     |  
     |  set_subsystem_handler(self, name, handler, *larg, **kwarg)
     |      Set the handler class for a subsystem in server mode.  If a request
     |      for this subsystem is made on an open ssh channel later, this handler
     |      will be constructed and called -- see `.SubsystemHandler` for more
     |      detailed documentation.
     |      
     |      Any extra parameters (including keyword arguments) are saved and
     |      passed to the `.SubsystemHandler` constructor later.
     |      
     |      :param str name: name of the subsystem.
     |      :param handler:
     |          subclass of `.SubsystemHandler` that handles this subsystem.
     |  
     |  start_client(self, event=None, timeout=None)
     |      Negotiate a new SSH2 session as a client.  This is the first step after
     |      creating a new `.Transport`.  A separate thread is created for protocol
     |      negotiation.
     |      
     |      If an event is passed in, this method returns immediately.  When
     |      negotiation is done (successful or not), the given ``Event`` will
     |      be triggered.  On failure, `is_active` will return ``False``.
     |      
     |      (Since 1.4) If ``event`` is ``None``, this method will not return until
     |      negotiation is done.  On success, the method returns normally.
     |      Otherwise an SSHException is raised.
     |      
     |      After a successful negotiation, you will usually want to authenticate,
     |      calling `auth_password <Transport.auth_password>` or
     |      `auth_publickey <Transport.auth_publickey>`.
     |      
     |      .. note:: `connect` is a simpler method for connecting as a client.
     |      
     |      .. note::
     |          After calling this method (or `start_server` or `connect`), you
     |          should no longer directly read from or write to the original socket
     |          object.
     |      
     |      :param .threading.Event event:
     |          an event to trigger when negotiation is complete (optional)
     |      
     |      :param float timeout:
     |          a timeout, in seconds, for SSH2 session negotiation (optional)
     |      
     |      :raises:
     |          `.SSHException` -- if negotiation fails (and no ``event`` was
     |          passed in)
     |  
     |  start_server(self, event=None, server=None)
     |      Negotiate a new SSH2 session as a server.  This is the first step after
     |      creating a new `.Transport` and setting up your server host key(s).  A
     |      separate thread is created for protocol negotiation.
     |      
     |      If an event is passed in, this method returns immediately.  When
     |      negotiation is done (successful or not), the given ``Event`` will
     |      be triggered.  On failure, `is_active` will return ``False``.
     |      
     |      (Since 1.4) If ``event`` is ``None``, this method will not return until
     |      negotiation is done.  On success, the method returns normally.
     |      Otherwise an SSHException is raised.
     |      
     |      After a successful negotiation, the client will need to authenticate.
     |      Override the methods `get_allowed_auths
     |      <.ServerInterface.get_allowed_auths>`, `check_auth_none
     |      <.ServerInterface.check_auth_none>`, `check_auth_password
     |      <.ServerInterface.check_auth_password>`, and `check_auth_publickey
     |      <.ServerInterface.check_auth_publickey>` in the given ``server`` object
     |      to control the authentication process.
     |      
     |      After a successful authentication, the client should request to open a
     |      channel.  Override `check_channel_request
     |      <.ServerInterface.check_channel_request>` in the given ``server``
     |      object to allow channels to be opened.
     |      
     |      .. note::
     |          After calling this method (or `start_client` or `connect`), you
     |          should no longer directly read from or write to the original socket
     |          object.
     |      
     |      :param .threading.Event event:
     |          an event to trigger when negotiation is complete.
     |      :param .ServerInterface server:
     |          an object used to perform authentication and create `channels
     |          <.Channel>`
     |      
     |      :raises:
     |          `.SSHException` -- if negotiation fails (and no ``event`` was
     |          passed in)
     |  
     |  stop_thread(self)
     |  
     |  use_compression(self, compress=True)
     |      Turn on/off compression.  This will only have an affect before starting
     |      the transport (ie before calling `connect`, etc).  By default,
     |      compression is off since it negatively affects interactive sessions.
     |      
     |      :param bool compress:
     |          ``True`` to ask the remote client/server to compress traffic;
     |          ``False`` to refuse compression
     |      
     |      .. versionadded:: 1.5.2
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from paramiko.transport.Transport:
     |  
     |  load_server_moduli(filename=None)
     |      (optional)
     |      Load a file of prime moduli for use in doing group-exchange key
     |      negotiation in server mode.  It's a rather obscure option and can be
     |      safely ignored.
     |      
     |      In server mode, the remote client may request "group-exchange" key
     |      negotiation, which asks the server to send a random prime number that
     |      fits certain criteria.  These primes are pretty difficult to compute,
     |      so they can't be generated on demand.  But many systems contain a file
     |      of suitable primes (usually named something like ``/etc/ssh/moduli``).
     |      If you call `load_server_moduli` and it returns ``True``, then this
     |      file of primes has been loaded and we will support "group-exchange" in
     |      server mode.  Otherwise server mode will just claim that it doesn't
     |      support that method of key negotiation.
     |      
     |      :param str filename:
     |          optional path to the moduli file, if you happen to know that it's
     |          not in a standard location.
     |      :return:
     |          True if a moduli file was successfully loaded; False otherwise.
     |      
     |      .. note:: This has no effect when used in client mode.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from threading.Thread:
     |  
     |  getName(self)
     |  
     |  isAlive = is_alive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  isDaemon(self)
     |  
     |  is_alive(self)
     |      Return whether the thread is alive.
     |      
     |      This method returns True just before the run() method starts until just
     |      after the run() method terminates. The module function enumerate()
     |      returns a list of all alive threads.
     |  
     |  join(self, timeout=None)
     |      Wait until the thread terminates.
     |      
     |      This blocks the calling thread until the thread whose join() method is
     |      called terminates -- either normally or through an unhandled exception
     |      or until the optional timeout occurs.
     |      
     |      When the timeout argument is present and not None, it should be a
     |      floating point number specifying a timeout for the operation in seconds
     |      (or fractions thereof). As join() always returns None, you must call
     |      isAlive() after join() to decide whether a timeout happened -- if the
     |      thread is still alive, the join() call timed out.
     |      
     |      When the timeout argument is not present or None, the operation will
     |      block until the thread terminates.
     |      
     |      A thread can be join()ed many times.
     |      
     |      join() raises a RuntimeError if an attempt is made to join the current
     |      thread as that would cause a deadlock. It is also an error to join() a
     |      thread before it has been started and attempts to do so raises the same
     |      exception.
     |  
     |  setDaemon(self, daemonic)
     |  
     |  setName(self, name)
     |  
     |  start(self)
     |      Start the thread's activity.
     |      
     |      It must be called at most once per thread object. It arranges for the
     |      object's run() method to be invoked in a separate thread of control.
     |      
     |      This method will raise a RuntimeError if called more than once on the
     |      same thread object.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from threading.Thread:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  daemon
     |      A boolean value indicating whether this thread is a daemon thread.
     |      
     |      This must be set before start() is called, otherwise RuntimeError is
     |      raised. Its initial value is inherited from the creating thread; the
     |      main thread is not a daemon thread and therefore all threads created in
     |      the main thread default to daemon = False.
     |      
     |      The entire Python program exits when no alive non-daemon threads are
     |      left.
     |  
     |  ident
     |      Thread identifier of this thread or None if it has not been started.
     |      
     |      This is a nonzero integer. See the get_ident() function. Thread
     |      identifiers may be recycled when a thread exits and another thread is
     |      created. The identifier is available even after the thread has exited.
     |  
     |  name
     |      A string used for identification purposes only.
     |      
     |      It has no semantics. Multiple threads may be given the same name. The
     |      initial name is set by the constructor.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from paramiko.util.ClosingContextManager:
     |  
     |  __enter__(self)
     |  
     |  __exit__(self, type, value, traceback)
    
    class TqdmWrap(tqdm._tqdm.tqdm)
     |  Decorate an iterable object, returning an iterator which acts exactly
     |  like the original iterable, but prints a dynamically updating
     |  progressbar every time a value is requested.
     |  
     |  Method resolution order:
     |      TqdmWrap
     |      tqdm._tqdm.tqdm
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  viewBar(self, a, b)
     |      Monitor progress of sftp transfers
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from tqdm._tqdm.tqdm:
     |  
     |  __del__(self)
     |  
     |  __enter__(self)
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __exit__(self, *exc)
     |  
     |  __ge__(self, other)
     |      Return self>=value.
     |  
     |  __gt__(self, other)
     |      Return self>value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __init__(self, iterable=None, desc=None, total=None, leave=True, file=None, ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None, ascii=None, disable=False, unit='it', unit_scale=False, dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0, position=None, postfix=None, unit_divisor=1000, gui=False, **kwargs)
     |      Parameters
     |      ----------
     |      iterable  : iterable, optional
     |          Iterable to decorate with a progressbar.
     |          Leave blank to manually manage the updates.
     |      desc  : str, optional
     |          Prefix for the progressbar.
     |      total  : int, optional
     |          The number of expected iterations. If unspecified,
     |          len(iterable) is used if possible. As a last resort, only basic
     |          progress statistics are displayed (no ETA, no progressbar).
     |          If `gui` is True and this parameter needs subsequent updating,
     |          specify an initial arbitrary large positive integer,
     |          e.g. int(9e9).
     |      leave  : bool, optional
     |          If [default: True], keeps all traces of the progressbar
     |          upon termination of iteration.
     |      file  : `io.TextIOWrapper` or `io.StringIO`, optional
     |          Specifies where to output the progress messages
     |          (default: sys.stderr). Uses `file.write(str)` and `file.flush()`
     |          methods.
     |      ncols  : int, optional
     |          The width of the entire output message. If specified,
     |          dynamically resizes the progressbar to stay within this bound.
     |          If unspecified, attempts to use environment width. The
     |          fallback is a meter width of 10 and no limit for the counter and
     |          statistics. If 0, will not print any meter (only stats).
     |      mininterval  : float, optional
     |          Minimum progress display update interval, in seconds [default: 0.1].
     |      maxinterval  : float, optional
     |          Maximum progress display update interval, in seconds [default: 10].
     |          Automatically adjusts `miniters` to correspond to `mininterval`
     |          after long display update lag. Only works if `dynamic_miniters`
     |          or monitor thread is enabled.
     |      miniters  : int, optional
     |          Minimum progress display update interval, in iterations.
     |          If 0 and `dynamic_miniters`, will automatically adjust to equal
     |          `mininterval` (more CPU efficient, good for tight loops).
     |          If > 0, will skip display of specified number of iterations.
     |          Tweak this and `mininterval` to get very efficient loops.
     |          If your progress is erratic with both fast and slow iterations
     |          (network, skipping items, etc) you should set miniters=1.
     |      ascii  : bool, optional
     |          If unspecified or False, use unicode (smooth blocks) to fill
     |          the meter. The fallback is to use ASCII characters `1-9 #`.
     |      disable  : bool, optional
     |          Whether to disable the entire progressbar wrapper
     |          [default: False]. If set to None, disable on non-TTY.
     |      unit  : str, optional
     |          String that will be used to define the unit of each iteration
     |          [default: it].
     |      unit_scale  : bool or int or float, optional
     |          If 1 or True, the number of iterations will be reduced/scaled
     |          automatically and a metric prefix following the
     |          International System of Units standard will be added
     |          (kilo, mega, etc.) [default: False]. If any other non-zero
     |          number, will scale `total` and `n`.
     |      dynamic_ncols  : bool, optional
     |          If set, constantly alters `ncols` to the environment (allowing
     |          for window resizes) [default: False].
     |      smoothing  : float, optional
     |          Exponential moving average smoothing factor for speed estimates
     |          (ignored in GUI mode). Ranges from 0 (average speed) to 1
     |          (current/instantaneous speed) [default: 0.3].
     |      bar_format  : str, optional
     |          Specify a custom bar string formatting. May impact performance.
     |          If unspecified, will use '{l_bar}{bar}{r_bar}', where l_bar is
     |          '{desc}: {percentage:3.0f}%|' and r_bar is
     |          '| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
     |          Possible vars: bar, n, n_fmt, total, total_fmt, percentage,
     |          rate, rate_fmt, elapsed, remaining, l_bar, r_bar, desc.
     |          Note that a trailing ": " is automatically removed after {desc}
     |          if the latter is empty.
     |      initial  : int, optional
     |          The initial counter value. Useful when restarting a progress
     |          bar [default: 0].
     |      position  : int, optional
     |          Specify the line offset to print this bar (starting from 0)
     |          Automatic if unspecified.
     |          Useful to manage multiple bars at once (eg, from threads).
     |      postfix  : dict, optional
     |          Specify additional stats to display at the end of the bar.
     |          Note: postfix is a dict ({'key': value} pairs) for this method,
     |          not a string.
     |      unit_divisor  : float, optional
     |          [default: 1000], ignored unless `unit_scale` is True.
     |      gui  : bool, optional
     |          WARNING: internal parameter - do not use.
     |          Use tqdm_gui(...) instead. If set, will attempt to use
     |          matplotlib animations for a graphical output [default: False].
     |      
     |      Returns
     |      -------
     |      out  : decorated iterator.
     |  
     |  __iter__(self)
     |      Backward-compatibility to use: for x in tqdm(iterable)
     |  
     |  __le__(self, other)
     |      Return self<=value.
     |  
     |  __len__(self)
     |  
     |  __lt__(self, other)
     |      Return self<value.
     |  
     |  __ne__(self, other)
     |      Return self!=value.
     |  
     |  __repr__(self, elapsed=None)
     |      Return repr(self).
     |  
     |  clear(self, nolock=False)
     |      Clear current bar display
     |  
     |  close(self)
     |      Cleanup and (if leave=False) close the progressbar.
     |  
     |  moveto(self, n)
     |  
     |  refresh(self, nolock=False)
     |      Force refresh the display of this bar
     |  
     |  set_description(self, desc=None, refresh=True)
     |      Set/modify description of the progress bar.
     |      
     |      Parameters
     |      ----------
     |      desc  : str, optional
     |      refresh  : bool, optional
     |          Forces refresh [default: True].
     |  
     |  set_description_str(self, desc=None, refresh=True)
     |      Set/modify description without ': ' appended.
     |  
     |  set_postfix(self, ordered_dict=None, refresh=True, **kwargs)
     |      Set/modify postfix (additional stats)
     |      with automatic formatting based on datatype.
     |      
     |      Parameters
     |      ----------
     |      ordered_dict  : dict or OrderedDict, optional
     |      refresh  : bool, optional
     |          Forces refresh [default: True].
     |      kwargs  : dict, optional
     |  
     |  set_postfix_str(self, s='', refresh=True)
     |      Postfix without dictionary expansion, similar to prefix handling.
     |  
     |  unpause(self)
     |      Restart tqdm timer from last print time.
     |  
     |  update(self, n=1)
     |      Manually update the progress bar, useful for streams
     |      such as reading files.
     |      E.g.:
     |      >>> t = tqdm(total=filesize) # Initialise
     |      >>> for current_buffer in stream:
     |      ...    ...
     |      ...    t.update(len(current_buffer))
     |      >>> t.close()
     |      The last line is highly recommended, but possibly not necessary if
     |      `t.update()` will be called in such a way that `filesize` will be
     |      exactly reached and printed.
     |      
     |      Parameters
     |      ----------
     |      n  : int, optional
     |          Increment to add to the internal counter of iterations
     |          [default: 1].
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from tqdm._tqdm.tqdm:
     |  
     |  external_write_mode(file=None, nolock=False) from builtins.type
     |      Disable tqdm within context and refresh tqdm when exits.
     |      Useful when writing to standard output stream
     |  
     |  get_lock() from builtins.type
     |  
     |  pandas(*targs, **tkwargs) from builtins.type
     |      Registers the given `tqdm` class with
     |          pandas.core.
     |          ( frame.DataFrame
     |          | series.Series
     |          | groupby.DataFrameGroupBy
     |          | groupby.SeriesGroupBy
     |          ).progress_apply
     |      
     |      A new instance will be create every time `progress_apply` is called,
     |      and each instance will automatically close() upon completion.
     |      
     |      Parameters
     |      ----------
     |      targs, tkwargs  : arguments for the tqdm instance
     |      
     |      Examples
     |      --------
     |      >>> import pandas as pd
     |      >>> import numpy as np
     |      >>> from tqdm import tqdm, tqdm_gui
     |      >>>
     |      >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
     |      >>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc
     |      >>> # Now you can use `progress_apply` instead of `apply`
     |      >>> df.groupby(0).progress_apply(lambda x: x**2)
     |      
     |      References
     |      ----------
     |      https://stackoverflow.com/questions/18603270/
     |      progress-indicator-during-pandas-operations-python
     |  
     |  set_lock(lock) from builtins.type
     |  
     |  write(s, file=None, end='\n', nolock=False) from builtins.type
     |      Print a message via tqdm (without overlap with bars)
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from tqdm._tqdm.tqdm:
     |  
     |  __new__(cls, *args, **kwargs)
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  format_interval(t)
     |      Formats a number of seconds as a clock time, [H:]MM:SS
     |      
     |      Parameters
     |      ----------
     |      t  : int
     |          Number of seconds.
     |      Returns
     |      -------
     |      out  : str
     |          [H:]MM:SS
     |  
     |  format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000)
     |      Return a string-based progress bar given some parameters
     |      
     |      Parameters
     |      ----------
     |      n  : int
     |          Number of finished iterations.
     |      total  : int
     |          The expected total number of iterations. If meaningless (), only
     |          basic progress statistics are displayed (no ETA).
     |      elapsed  : float
     |          Number of seconds passed since start.
     |      ncols  : int, optional
     |          The width of the entire output message. If specified,
     |          dynamically resizes the progress meter to stay within this bound
     |          [default: None]. The fallback meter width is 10 for the progress
     |          bar + no limit for the iterations counter and statistics. If 0,
     |          will not print any meter (only stats).
     |      prefix  : str, optional
     |          Prefix message (included in total width) [default: ''].
     |          Use as {desc} in bar_format string.
     |      ascii  : bool, optional
     |          If not set, use unicode (smooth blocks) to fill the meter
     |          [default: False]. The fallback is to use ASCII characters
     |          (1-9 #).
     |      unit  : str, optional
     |          The iteration unit [default: 'it'].
     |      unit_scale  : bool or int or float, optional
     |          If 1 or True, the number of iterations will be printed with an
     |          appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)
     |          [default: False]. If any other non-zero number, will scale
     |          `total` and `n`.
     |      rate  : float, optional
     |          Manual override for iteration rate.
     |          If [default: None], uses n/elapsed.
     |      bar_format  : str, optional
     |          Specify a custom bar string formatting. May impact performance.
     |          [default: '{l_bar}{bar}{r_bar}'], where
     |          l_bar='{desc}: {percentage:3.0f}%|' and
     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
     |            '{rate_fmt}{postfix}]'
     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
     |          Note that a trailing ": " is automatically removed after {desc}
     |          if the latter is empty.
     |      postfix  : str, optional
     |          Similar to `prefix`, but placed at the end
     |          (e.g. for additional stats).
     |          Note: postfix is a string for this method. Not a dict.
     |      unit_divisor  : float, optional
     |          [default: 1000], ignored unless `unit_scale` is True.
     |      
     |      Returns
     |      -------
     |      out  : Formatted meter and stats, ready to display.
     |  
     |  format_sizeof(num, suffix='', divisor=1000)
     |      Formats a number (greater than unity) with SI Order of Magnitude
     |      prefixes.
     |      
     |      Parameters
     |      ----------
     |      num  : float
     |          Number ( >= 1) to format.
     |      suffix  : str, optional
     |          Post-postfix [default: ''].
     |      divisor  : float, optionl
     |          Divisor between prefixes [default: 1000].
     |      
     |      Returns
     |      -------
     |      out  : str
     |          Number with Order of Magnitude SI unit postfix.
     |  
     |  status_printer(file)
     |      Manage the printing and in-place updating of a line of characters.
     |      Note that if the string is longer than a line, then in-place
     |      updating may not work (it will print a new line at each refresh).
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from tqdm._tqdm.tqdm:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from tqdm._tqdm.tqdm:
     |  
     |  monitor = None
     |  
     |  monitor_interval = 10

FUNCTIONS
    s2i_client(filename, put_file=True, get_file=True, cleanup_raw=True, cleanup_processed=True, remote_dir='/tmp', host=None, port=22, username=None, ssh_key=None, password=None, debug_level=20)
        Runs siemens_to_ismrmrd on a remote computer.
        
        Main idea: allow users to use siemens_to_ismrmrd even if they don't have
        it installed locally.  They will, however, require SSH access to computer
        that does have it installed.
        
        Client puts file on server using SFTP, runs siemens_to_ismrmrd over SSH,
        and gets the file back using SFTP.  Username, password, hostname, and port
        is retrieved from the active profile in profiles.config.  Default port is
        22.  If no password is found, the RSA SSH key will be used from either the
        specified directory in profiles.config or, if empty, use '~/.ssh/id_rsa'.
        
        filename -- Raw data (.dat) file on the local machine (if put_file is True)
                    or on the remote machine (if put_file is False).
        put_file -- Whether or not to copy the raw data file from local to remote.
        get_file -- Whether or not to copy the processed file from machine to local.
        cleanup_raw -- Whether or not to delete raw data on remote.
        cleanup_processed -- Whether or not to delete processed data on remote.
        remote_dir -- Working directory on remote (default in /tmp).
        host -- hostname of remote machine.
        port -- Port of remote machine to connect to.
        username -- Username to use for SSH/SFTP connections.
        ssh_key -- RSA private key file to use for SSH/SFTP connections.
        password -- Password to use fr SSH/SFTP connections (stored in plaintext).
        debug_level -- Level of verbosity; see python logging module.


```


## mr_utils.load_data.xprot

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/xprot.py)

```
NAME
    mr_utils.load_data.xprot

CLASSES
    builtins.object
        XProtLex
        XProtParser
    
    class XProtLex(builtins.object)
     |  Methods defined here:
     |  
     |  t_COMMENT(t)
     |      \#.*
     |  
     |  t_LEFTHAND(t)
     |      [a-zA-Z\[\]0-9\. _]+=
     |  
     |  t_error(t)
     |      # Error handling rule
     |  
     |  t_newline(t)
     |      \n+
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  lexer = <ply.lex.Lexer object>
     |  
     |  t_CLASS = 'Class'
     |  
     |  t_COM = 'Comment'
     |  
     |  t_CONN = 'Connection'
     |  
     |  t_CONTEXT = 'Context'
     |  
     |  t_CONTROL = 'Control'
     |  
     |  t_DEFAULT = 'Default'
     |  
     |  t_DEPEND = 'Dependency'
     |  
     |  t_DICOM = 'Dicom'
     |  
     |  t_DLL = 'Dll'
     |  
     |  t_EVASTRTAB = 'EVAStringTable'
     |  
     |  t_EVENT = 'Event'
     |  
     |  t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
     |  
     |  t_HEX = r'0x[\dabcdef]+'
     |  
     |  t_ID = 'ID'
     |  
     |  t_INFILE = 'InFile'
     |  
     |  t_INTEGER = r'-?\d+'
     |  
     |  t_LABEL = 'Label'
     |  
     |  t_LANGLE = '<'
     |  
     |  t_LBRACE = '{'
     |  
     |  t_LIMIT = 'Limit'
     |  
     |  t_LIMRANGE = 'LimitRange'
     |  
     |  t_LINE = 'Line'
     |  
     |  t_MAXSIZE = 'MaxSize'
     |  
     |  t_MEAS = 'Meas'
     |  
     |  t_MEASYAPS = 'MeasYaps'
     |  
     |  t_METHOD = 'Method'
     |  
     |  t_MINSIZE = 'MinSize'
     |  
     |  t_NAME = 'Name'
     |  
     |  t_PARAM = 'Param'
     |  
     |  t_PARRAY = 'ParamArray'
     |  
     |  t_PBOOL = 'ParamBool'
     |  
     |  t_PCARDLAYOUT = 'ParamCardLayout'
     |  
     |  t_PCHOICE = 'ParamChoice'
     |  
     |  t_PDBL = 'ParamDouble'
     |  
     |  t_PERIOD = r'\.'
     |  
     |  t_PFUNCT = 'ParamFunctor'
     |  
     |  t_PHOENIX = 'Phoenix'
     |  
     |  t_PIPE = 'Pipe'
     |  
     |  t_PIPESERVICE = 'PipeService'
     |  
     |  t_PLNG = 'ParamLong'
     |  
     |  t_PMAP = 'ParamMap'
     |  
     |  t_POS = 'Pos'
     |  
     |  t_PRECISION = 'Precision'
     |  
     |  t_PROTCOMP = 'ProtocolComposer'
     |  
     |  t_PSTR = 'ParamString'
     |  
     |  t_RANGLE = '>'
     |  
     |  t_RBRACE = '}'
     |  
     |  t_REPR = 'Repr'
     |  
     |  t_SCINOT = r'([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))'
     |  
     |  t_SPICE = 'Spice'
     |  
     |  t_STRING = r'\"(.|\n)*?\"'
     |  
     |  t_TOOLTIP = 'Tooltip'
     |  
     |  t_UNIT = 'Unit'
     |  
     |  t_USERVERSION = 'Userversion'
     |  
     |  t_VISIBLE = 'Visible'
     |  
     |  t_XPROT = 'XProtocol'
     |  
     |  t_ignore = ' \t'
     |  
     |  tokens = ('RANGLE', 'LANGLE', 'PERIOD', 'RBRACE', 'LBRACE', 'STRING', ...
    
    class XProtParser(builtins.object)
     |  Methods defined here:
     |  
     |  raw2xml(self, xprot)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  brace_state = []
     |  
     |  mod = ''
     |  
     |  name = ''
     |  
     |  node_label = ''
     |  
     |  xml = ''


```


## mr_utils.load_data.xprot_parser

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/xprot_parser.py)

```
NAME
    mr_utils.load_data.xprot_parser - Parse XProtocol Siemens' proprietary format.

CLASSES
    builtins.object
        XProtLexer
        XProtParser
    
    class XProtLexer(builtins.object)
     |  Define tokens and rules.
     |  
     |  Methods defined here:
     |  
     |  t_COMMENT(t)
     |      \#.*
     |  
     |  t_error(t)
     |      # Error handling rule
     |  
     |  t_newline(t)
     |      \n+
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  lexer = <ply.lex.Lexer object>
     |  
     |  t_CLASS = 'Class'
     |  
     |  t_COMMENTTAG = 'Comment'
     |  
     |  t_CONNECTION = 'Connection'
     |  
     |  t_CONTEXT = 'Context'
     |  
     |  t_CONTROL = 'Control'
     |  
     |  t_DEFAULT = 'Default'
     |  
     |  t_DEPENDENCY = 'Dependency'
     |  
     |  t_DLL = 'Dll'
     |  
     |  t_EVASTRTAB = 'EVAStringTable'
     |  
     |  t_EVENT = 'Event'
     |  
     |  t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
     |  
     |  t_ID = 'ID'
     |  
     |  t_INFILE = 'InFile'
     |  
     |  t_INTEGER = r'-?\d+'
     |  
     |  t_LABEL = 'Label'
     |  
     |  t_LANGLE = '<'
     |  
     |  t_LBRACE = '{'
     |  
     |  t_LIMIT = 'Limit'
     |  
     |  t_LIMITRANGE = 'LimitRange'
     |  
     |  t_MAXSIZE = 'MaxSize'
     |  
     |  t_METHOD = 'Method'
     |  
     |  t_MINSIZE = 'MinSize'
     |  
     |  t_NAME = 'Name'
     |  
     |  t_PARAM = 'Param'
     |  
     |  t_PARAMARRAY = 'ParamArray'
     |  
     |  t_PARAMBOOL = 'ParamBool'
     |  
     |  t_PARAMCARDLAYOUT = 'ParamCardLayout'
     |  
     |  t_PARAMCHOICE = 'ParamChoice'
     |  
     |  t_PARAMDOUBLE = 'ParamDouble'
     |  
     |  t_PARAMFUNCTOR = 'ParamFunctor'
     |  
     |  t_PARAMLONG = 'ParamLong'
     |  
     |  t_PARAMMAP = 'ParamMap'
     |  
     |  t_PARAMSTRING = 'ParamString'
     |  
     |  t_PERIOD = r'\.'
     |  
     |  t_PIPE = 'Pipe'
     |  
     |  t_PIPESERVICE = 'PipeService'
     |  
     |  t_POS = 'Pos'
     |  
     |  t_PRECISION = 'Precision'
     |  
     |  t_PROTOCOLCOMPOSER = 'ProtocolComposer'
     |  
     |  t_QUOTED_STRING = r'\"(.|\n)*?\"'
     |  
     |  t_RANGLE = '>'
     |  
     |  t_RBRACE = '}'
     |  
     |  t_REPR = 'Repr'
     |  
     |  t_TOOLTIP = 'Tooltip'
     |  
     |  t_UNIT = 'Unit'
     |  
     |  t_USERVERSION = 'Userversion'
     |  
     |  t_VISIBLE = 'Visible'
     |  
     |  t_XPROT = 'XProtocol'
     |  
     |  t_ignore = ' \t'
     |  
     |  tokens = ('RANGLE', 'LANGLE', 'LBRACE', 'RBRACE', 'PERIOD', 'XPROT', '...
    
    class XProtParser(builtins.object)
     |  Parse the XProtocol.  Just do it.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  parse(self, xprot)
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
    reduce(...)
        reduce(function, sequence[, initial]) -> value
        
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.


```


# MATLAB
## mr_utils.matlab.client

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/matlab/client.py)

```
NAME
    mr_utils.matlab.client - Connect to network machine running MATLAB to run scripts.

DESCRIPTION
    A way to run MATLAB scripts inside python scripts.  Meant to run things until
    I have time to port them to Python.  It's meant to match the gadgetron client.

FUNCTIONS
    client_get(varnames, host=None, port=None, bufsize=None)
        Get variables from remote MATLAB workspace into python as numpy arrays.
        
        varnames -- List of names of variables in MATLAB workspace to get.
        host -- host/ip-address of server running MATLAB.
        port -- port of host to connect to.
        bufsize -- Number of bytes to transmit/recieve at a time.
        
        Notice that varnames should be a list of strings.
    
    client_put(varnames, host=None, port=None, bufsize=None)
        Put variables from python into MATLAB workspace.
        
        varnames -- Python variables to be injected into MATLAB workspace.
        bufsize -- Number of bytes to transmit/recieve at a time.
        
        Notice that varnames should be a dictionary: keys are the desired names of
        the variables in the MATLAB workspace and values are the python
        variables.
    
    client_run(cmd, host=None, port=None, bufsize=None)
        Run command on MATLAB server.
        
        cmd -- MATLAB command.
        host -- host/ip-address of server running MATLAB.
        port -- port of host to connect to.
        bufsize -- Number of bytes to transmit/recieve at a time.
        
        If values are not provided (i.e., None) the values for host,port,bufsize
        will be taken from the active profile in profiles.config.
    
    get_socket(host, port, bufsize)
        Open a socket to the machine running MATLAB.
        
        host -- IP address of machine running MATLAB.
        port -- port to connect to.
        bufsize -- Buffer size to use for communication.
        
        If values are not provided (i.e., None) the values for host,port,bufsize
        will be taken from the active profile in profiles.config.

```


## mr_utils.matlab.client_old

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/matlab/client_old.py)

```
NAME
    mr_utils.matlab.client_old

CLASSES
    builtins.object
        Client
    
    class Client(builtins.object)
     |  Open MATLAB subprocess to run commands and view output.
     |  
     |  Currently only works with MATLAB installations installed on the same
     |  computer the client is launched from.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  catch_output(self)
     |  
     |  exit(self)
     |      Send exit command to MATLAB.
     |  
     |  get(self, varnames)
     |      Get variables from MATLAB workspace into python as numpy arrays.
     |      
     |      varnames -- List of names of variables in MATLAB workspace to get.
     |      
     |      Notice that varnames should be a list of strings.
     |  
     |  put(self, vars)
     |      Put variables from python into MATLAB workspace.
     |      
     |      vars -- Python variables to be injected into MATLAB workspace.
     |      
     |      Notice that vars should be a dictionary: keys are the desired names of
     |      the variables in the MATLAB workspace and values are the python
     |      variables.
     |  
     |  run(self, cmd)
     |      Run MATLAB command in subprocess.
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


## mr_utils.matlab.contract

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/matlab/contract.py)

```
NAME
    mr_utils.matlab.contract - Define communication tokens for communication with MATLAB server.

```


## mr_utils.matlab.server

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/matlab/server.py)

```
NAME
    mr_utils.matlab.server - Server to be running on network machine.

DESCRIPTION
    Must be running for client to be able to connect.  Obviously, alongside this
    server, MATLAB should also be running.

CLASSES
    builtins.object
        MATLAB
    socketserver.StreamRequestHandler(socketserver.BaseRequestHandler)
        MyTCPHandler
    
    class MATLAB(builtins.object)
     |  Object on server allowing server to communicate with MATLAB instance.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  catch_output(self, log_func=None)
     |      Grab the output of MATLAB on the server.
     |  
     |  exit(self)
     |      Send exit command to MATLAB.
     |  
     |  get(self, varnames)
     |      Get variables from MATLAB workspace into python as numpy arrays.
     |      
     |      varnames -- List of names of variables in MATLAB workspace to get.
     |      
     |      Notice that varnames should be a list of strings.
     |  
     |  put(self, tmp_filename)
     |      Put variables from python into MATLAB workspace.
     |      
     |      tmp_filename -- MAT file holding variables to inject into workspace.
     |  
     |  run(self, cmd, log_func=None)
     |      Run MATLAB command in subprocess.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class MyTCPHandler(socketserver.StreamRequestHandler)
     |  Create the server, binding to localhost on port.
     |  
     |  Method resolution order:
     |      MyTCPHandler
     |      socketserver.StreamRequestHandler
     |      socketserver.BaseRequestHandler
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  handle(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from socketserver.StreamRequestHandler:
     |  
     |  finish(self)
     |  
     |  setup(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from socketserver.StreamRequestHandler:
     |  
     |  disable_nagle_algorithm = False
     |  
     |  rbufsize = -1
     |  
     |  timeout = None
     |  
     |  wbufsize = 0
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from socketserver.BaseRequestHandler:
     |  
     |  __init__(self, request, client_address, server)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from socketserver.BaseRequestHandler:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
    start_server()
        Start the server so the client can connect.

```


# OPTIMIZATION
## mr_utils.optimization.gd

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/optimization/gd.py)

```
NAME
    mr_utils.optimization.gd - General implementation of gradient descent algorithm.

DESCRIPTION
    More of a learning exercise for myself.

FUNCTIONS
    gd(f, grad, x0, alpha=None, maxiter=1000000.0, tol=1e-08)
        Gradient descent algorithm.
        
        f -- Function to be optimized.
        grad -- Function that computes the gradient of f.
        x0 -- Initial point to start to start descent.
        alpha -- Either a fixed step size or a function that returns step size.
        maxiter -- Do not exceed this number of iterations.
        tol -- Run until change in norm of gradient is within this number.


```


## mr_utils.optimization.gradient

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/optimization/gradient.py)

```
NAME
    mr_utils.optimization.gradient - Numerical derivative implementations.

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
        6th order accurate complex step difference method.
    
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

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/optimization/linesearch.py)

```
NAME
    mr_utils.optimization.linesearch - Linesearch functions.

DESCRIPTION
    Once we have a direction to step, for example, the negative gradient direction
    in a gradient descent algorithm, then we need to know how big of a step to
    take.  If we take too large or small a step, we may not find the minumum of
    the object function along the line we are stepping.  A linesearch attempts to
    find the optimal step size in a given direction with minimal gradient and
    objective evaluations.

FUNCTIONS
    linesearch(obj, x0, a0, s)
        More sophisticated linesearch.
        
        obj -- Objective function.
        x0 -- Current location.
        a0 -- Current guess at stepsize.
        s -- Search direction.
    
    linesearch_quad(f, x, a, s)
        Simple quadratic linesearch.
        
        f -- Objective function.
        x -- Current location.
        a -- Guess for stepsize.
        s -- Search direction.


```


# RECON
## mr_utils.recon.espirit.espirit

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/espirit/espirit.py)

```
NAME
    mr_utils.recon.espirit.espirit - ## Adapted from https://github.com/peng-cao/mripy

CLASSES
    builtins.object
        FFT2d
    
    class FFT2d(builtins.object)
     |  these classes apply  FFT for the input image,
     |   and some also apply mask in the forward function
     |  the order is
     |  k-space -> image for forward;
     |  image -> k-space is backward
     |  
     |  this is 2d FFT without k-space mask for CS MRI recon
     |  
     |  Methods defined here:
     |  
     |  __init__(self, axes=(0, 1))
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  backward(self, ksp)
     |      # let's call image <- k-space as backward
     |  
     |  forward(self, im)
     |      # let's call k-space <- image as forward
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
    espirit_2d(xcrop, x_shape, nsingularv=150, hkwin_shape=(16, 16), pad_before_espirit=0, pad_fact=1, sigv_th=0.01, nsigv_th=0.2)
        2d espirit
        
        Inputs
        xcrop is 3d matrix with first two dimentions as nx,ny and third one as coil
        nsingularv = 150, number of truncated singular vectors
        
        outputs
        Vim the sensitivity map
        sim the singular value map
    
    hamming2d(a, b)
    
    hankelnd_r(a, win_shape, win_strides=None)
        # the first half dimentions are window dimentions,
        # the second half dimentions are rolling/repeating dimentions
    
    pad2d(data, nx, ny)
        zero pad the 2d k-space in kx and ky dimentions


```


## mr_utils.recon.field_map.dual_echo_gre

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/field_map/dual_echo_gre.py)

```
NAME
    mr_utils.recon.field_map.dual_echo_gre - Compute field map from dual echo GRE acquisitions.

FUNCTIONS
    dual_echo_gre(m1, m2, TE1, TE2)
        Compute wrapped field map from two GRE images at different TEs.
        
        m1 -- GRE image taken with TE = TE1.
        m2 -- GRE image taken with TE = TE2.
        TE1 -- echo time corresponding to m1.
        TE2 -- echo time corresponding to m2.
        
        Returns field map in herz.


```


## mr_utils.recon.field_map.gs_field_map

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/field_map/gs_field_map.py)

```
NAME
    mr_utils.recon.field_map.gs_field_map - Use the geometric solution to the elliptical signal model for field map.

FUNCTIONS
    gs_field_map(I0, I1, I2, I3, TR, gs_recon_opts=None)
        Use the elliptical signal model to estimate the field map.
        
        I0,I1 -- First phase-cycle pair, separated by 180 degrees.
        I1,I3 -- Second phase-cycle pair, separated by 180 degrees.
        TR -- Repetition time of acquisitons in ms.
        gs_recon_opts -- Options to pass to gs_recon.
        
        Returns wrapped field map in hertz.
        
        Implements field map estimation given in:
            Taylor, Meredith, et al. "MRI Field Mapping using bSSFP Elliptical
            Signal model." Proceedings of the ISMRM Annual Conference (2017).


```


## mr_utils.recon.grappa.grappa

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/grappa/grappa.py)

```
NAME
    mr_utils.recon.grappa.grappa

FUNCTIONS
    grappa2d(coil_ims, sens, acs, Rx, Ry, kernel_size=(3, 3))


```


## mr_utils.recon.partial_fourier.partial_fourier_pocs

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/partial_fourier/partial_fourier_pocs.py)

```
NAME
    mr_utils.recon.partial_fourier.partial_fourier_pocs - # Python port of Gadgetron's 2D partial_fourier_POCS

FUNCTIONS
    apply_kspace_filter_ROE1(data, FRO, FE1)
    
    compute_2d_filter(fx, fy)
    
    generate_symmetric_filter(length, filterType, sigma=1.5, width=15)
    
    generate_symmetric_filter_ref(length, start, end)
    
    partial_fourier_pocs(kspace, startRO, endRO, startE1, endE1, transit_band_RO=0, transit_band_E1=0, iter=10, thres=0.01)
        # kspace: input kspace [RO E1 E2 ...]
        # 2D POCS is performed
        # startRO, endRO, startE1, endE1: acquired kspace range
        # transit_band_RO/E1: transition band width in pixel for RO/E1
        # iter: number of maximal iterations for POCS
        # thres: iteration threshold
    
    partial_fourier_reset_kspace(src, dst, startRO, endRO, startE1, endE1)

```


## mr_utils.recon.reordering.bart

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/bart.py)

```
NAME
    mr_utils.recon.reordering.bart

```


## mr_utils.recon.reordering.lcurve

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/lcurve.py)

```
NAME
    mr_utils.recon.reordering.lcurve

FUNCTIONS
    lcurve(norm0, norm1)


```


## mr_utils.recon.reordering.patch_reordering

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/patch_reordering.py)

```
NAME
    mr_utils.recon.reordering.patch_reordering

FUNCTIONS
    get_patches(imspace, patch_size)


```


## mr_utils.recon.reordering.rudin_osher_fatemi

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/rudin_osher_fatemi.py)

```
NAME
    mr_utils.recon.reordering.rudin_osher_fatemi

FUNCTIONS
    check_stability(dt, h, c=300000000.0)
        Check stepsize restriction, imposed for for stability.
    
    getbounds(ii, jj, u0)
    
    minmod(a, b)
        Flux limiter to make FD solutions total variation diminishing.
    
    update_all_for_loop(u0, dt, h, sigma, niters)


```


## mr_utils.recon.reordering.scr_reordering_adluru

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/scr_reordering_adluru.py)

```
NAME
    mr_utils.recon.reordering.scr_reordering_adluru

FUNCTIONS
    TVG(out_img, beta_sqrd)
    
    TVG_re_order(out_img, beta_sqrd, sort_order_real_x, sort_order_real_y)
    
    intshft(m, sh)
        Shift image m by coordinates specified by sh
    
    scr_reordering_adluru(kspace, mask, prior=None, alpha0=1, alpha1=0.002, beta2=1e-08, reorder=True, reorder_every_iter=False, enforce_consistency=False, niters=5000)
        Reconstruct undersampled data with spatial TV constraint and reordering.
        
        kspace -- Undersampled k-space data
        mask -- Undersampling mask
        prior -- Prior image estimate, what to base reordering on
        alpha0 -- Weight of the fidelity term in cost function
        alpha1 -- Weight of the TV term, regularization parameter
        beta2 -- beta squared, small constant to keep sqrt defined
        reorder -- Whether or not to reorder data
        reorder_every_iter -- Reorder each iteration based on current estimate
        enforce_consistency -- Fill in known values of kspace each iteration
        niters -- Number of iterations
        
        Ref: G.Adluru, E.V.R. DiBella. "Reordering for improved constrained
        reconstruction from undersampled k-space data". International Journal of
        Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008.
        doi:10.1155/2008/341684.
    
    sort_real_imag_parts_space(full_data_recon_complex)
        Determines the sort order for real and imag components.
    
    time(...)
        time() -> floating point number
        
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.


```


## mr_utils.recon.reordering.tsp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/reordering/tsp.py)

```
NAME
    mr_utils.recon.reordering.tsp

FUNCTIONS
    create_distance_callback(dist_matrix)
        # Distance callback
    
    generate_orderings(im=None)
    
    get_dist_matrix()
    
    get_slice(lpf=True, lpf_factor=6)
    
    get_time_series(im, x=100, y=100, real_part=True, patch=False, patch_pad=(1, 1))
    
    normalize_time_series(time_series0)
    
    ortools_tsp_solver()


```


## mr_utils.recon.ssfp.dixon

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/dixon.py)

```
NAME
    mr_utils.recon.ssfp.dixon - Collection of Dixon fat/water separation methods.

DESCRIPTION
    Implementations of methods described in Berstein (see function docstrings for
    references).

FUNCTIONS
    dixon_2pt(IP, OP)
        Naive two-point Dixon method of fat/water separation.
        
        IP -- In-phase image (corresponding to 0).
        OP -- Out-of-phase image (corresponding to pi).
        
        Returns water image, W, and fat image, F.
        
        "[This implementation] ignores additional image weighting from T2*
        relaxation, diffusion, and flow and from other phase shifts that could
        arise from hardware group delays, eddy currents, and B1 receive-field
        nonuniformity. We have also ignored the water-fat chemical shift
        separation in both the slice and readout directions"
        
        Implements method described in:
            Dixon, W. T. (1984). Simple proton spectroscopic imaging. Radiology,
        Also equations [17.52] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_2pt_mag(IP, OP)
        Solution to two-point Dixon method using magnitude of images.
        
        IP -- In-phase image (corresponding to 0).
        OP -- Out-of-phase image (corresponding to pi).
        
        Returns water image, abs(W), and fat image, abs(F).
        
        Implements equations [17.53-54] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_3pt(IP, OP1, OP2, use_2pi=True, method='glover')
        Three point Dixon method of fat/water separation.
        
        IP -- In-phase image (corresponding to 0).
        OP1 -- Out-of-phase image (corresponding to pi).
        OP2 -- Out-of-phase image (corresponding to -pi or 2*pi).
        use_2pi -- Use 2*pi for OP2 instead of -pi.
        method -- Method to use to determine pc, see dixon_pc().
        
        Returns water image, W, fat image, F, and B0 image.
        
        "The phase difference between the two opposed-phase images is due
        to B0 inhomogeneity, and they are used to compute phi. The phi map is used
        to remove the B0 inhomogeneity phase shift from one of the opposed-phase
        images and thereby determine the dominant species for each pixel (i.e.,
        whether W > F, or vice versa)."
        
        Implements method described:
            Glover, G. H., & Schneider, E. (1991). Three‐point Dixon technique for
            true water/fat decomposition with B0 inhomogeneity correction. Magnetic
            resonance in medicine, 18(2), 371-383.
        
        Also implements equations [17.71] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_3pt_dpe(I0, I1, I2, theta)
        Three point Dixon using direct phase encoding (DPE).
        
        Note that theta_0 + theta should not be a multiple of pi!
        
        Implements equations [17.83-84] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_3pt_eam(I0, I1, I2, method='glover')
        Three point Dixon including echo amplitude modulation (EAM).
        
        I0 -- In-phase image (corresponding to phi_0 phase).
        I1 -- Out-of-phase image (corresponding to phi_0 + phi).
        I2 -- Out-of-phase image (corresponding to phi_0 + 2*phi).
        method -- Method to use to determine pc, see dixon_pc().
        
        Returns water image, W, fat image, F, and A, the susceptibility dephasing
        map.
        
        "...under our assumptions, ignoring amplitude effects simply results in a
        multiplicative error in both water and fat components. This error is
        usually not serious and can be ignored...there is a SNR penalty for the
        amplitude correction, and it is best avoided unless there is a specific
        need to compute A for the application of interest."
        
        Implements equations [17.78] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_extended_2pt(IP, OP, method='glover')
        Extended two-point Dixon method for fat/water separation.
        
        IP -- In-phase image (corresponding to 0).
        OP -- Out-of-phase image (corresponding to pi).
        method -- Method to use to determine pc, see dixon_pc().
        
        Returns water image, abs(W), and fat image, abs(F).
        
        Extended 2PD attempts to address the B0 homogeneity problem by using a
        generalized pc.
        
        Implements equations [17.63] in:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    dixon_pc(IP, OP, method='vanilla')
        Methods to determine pc, fat/water fraction within a voxel.
        
        method:
            'vanilla': sign of W - F.
            'glover': maintain continuous image appearance by using cont. p value.
            'chen': alternative that performs 'glover' and then discretizes.
        
        'glover' is implementation of eq [17.62], 'chen' is implementation of eq
        [17.64-65], 'vanilla' is eq [17.54] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.


```


## mr_utils.recon.ssfp.gs_recon

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/gs_recon.py)

```
NAME
    mr_utils.recon.ssfp.gs_recon - Geometric solution to the elliptical signal model.

FUNCTIONS
    complex_sum(I1, I2, I3, I4)
        Complex sum image combination method.
    
    compute_Iw(I0, I1, Id, patch_size=(5, 5), mode='constant', isophase=3.141592653589793)
        Computes weighted sum of image pair (I0,I1).
        
        I0 -- 1st of pair of diagonal images (relative phase cycle of 0).
        I1 -- 2nd of pair of diagonal images (relative phase cycle of 180 deg).
        Id -- result of regularized direct solution.
        patch_size -- size of patches in pixels (x,y).
        mode -- mode of numpy.pad. Probably choose 'constant' or 'edge'.
        isophase -- Only neighbours with max phase difference isophase contribute.
        
        Image pair (I0,I1) are phase cycled bSSFP images that are different by
        180 degrees.  Id is the image given by the direct method (Equation [13])
        after regularization by the complex sum.  This function solves for the
        weights by regional differential energy minimization.  The 'regional'
        part means that the image is split into patches of size patch_size with
        edge boundary conditions (pads with the edge values given by mode option).
        The weighted sum of the image pair is returned.
        
        The isophase does not appear in the paper, but appears in Hoff's MATLAB
        code.  It appears that we only want to consider pixels in the patch that
        have similar tissue properties - in other words, have similar phase.  The
        default isophase is pi as in Hoff's implementation.
        
        This function implements Equations [14,18], or steps 4--5 from Fig. 2 in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    get_max_magnitudes(I1, I2, I3, I4)
        Find maximum magnitudes for each pixel over all four input images.
    
    get_max_magnitudes_for_loop(I1, I2, I3, I4)
        Find maximum magnitudes for each pixel over all four input images.
        
        This one loops over each pixel as verification for get_max_magnitudes().
    
    gs_recon(I1, I2, I3, I4, isophase=3.141592653589793, second_pass=True)
        Full 2D Geometric Solution method following Xiang and Hoff's 2014 paper.
        
        I1,I3 -- 1st diagonal pair of images (offset 180 deg).
        I2,I4 -- 2nd diagonal pair of images (offset 180 deg).
        isophase -- Only neighbours with isophase max phase difference contribute.
        second_pass -- Compute the second pass solution, increasing SNR by sqrt(2).
        
        Implements algorithm shown in Fig 2 of
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    gs_recon3d(I1, I2, I3, I4, slice_axis=-1, isophase=3.141592653589793)
        Full 3D Geometric Solution method following Xiang and Hoff's 2014 paper.
        
        I1--I4 -- Phase-cycled images.
        slice_axis -- Slice dimension, default is the last dimension.
        For more info, see mr_utils.recon.ssfp.gs_recon.
    
    gs_recon_for_loop(I1, I2, I3, I4)
        GS recon implemented using a straightfoward loop for verification.
    
    mask_isophase(numerator_patches, patch_size, isophase)
        Generate mask that chooses patch pixels that satisfy isophase.
        
        numerator_patches -- Numerator patches from second pass solution.
        patch_size -- size of patches in pixels (x,y).
        isophase -- Only neighbours with isophase max phase difference contribute.
        
        Output mask, same size as numerator_patches, to be applied to
        numerator_patches and den_patches before summation.


```


## mr_utils.recon.ssfp.multiphase

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/multiphase.py)

```
NAME
    mr_utils.recon.ssfp.multiphase

FUNCTIONS
    multiphase(kspace)
        Acquire two phase-cycled images in one Cartesian acquisiton.
        
        The idea is to acquire kspace with even lines having phase-cycle \phi_0 and
        and odd lines having phase-cycle \phi_1.  Then split the lines up into
        two R=2 undersampled images and use parallel imaging reconstruction to
        recover the two separate phase-cycled images.
        
        kspace -- Even lines phase \phi_0, odd lines phase \phi_1.


```


## mr_utils.recon.ssfp.planet

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/ssfp/planet.py)

```
NAME
    mr_utils.recon.ssfp.planet - PLANET: an ellipse fitting approach for simultaneous T1 and T2 mapping...

DESCRIPTION
    ...Using Phase-Cycled Balanced Steady-State Free Precession.

FUNCTIONS
    PLANET(I, alpha, TR, T1s=None, fit_ellipse=None, pcs=None, compute_df=False, disp=False)
        Simultaneous T1, T2 mapping using phase‐cycled bSSFP.
        
        I -- Complex voxels from phase-cycled bSSFP images.
        alpha -- Flip angle (in rad).
        TR -- Repetition time (in sec).
        pcs -- List of phase-cycles in I (required if computing df).
        T1s -- Range of T1s.
        fit_ellipse -- Function used to fit data points to ellipse.
        compute_df -- Whether or not estimate local off-resonance, df.
        disp -- Show plots.
        
        Requires at least 6 phase cycles to fit the ellipse.  The ellipse fitting
        method they use (and which is implemented here) may not be the best
        method, but it is quick.  Could add more options for fitting in the future.
        
        fit_ellipse(x, y) should take two arguments and return a vector containing
        the coefficients of the implicit ellipse equation.  If fit_ellipse=None
        then the mr_utils.utils.fit_ellipse_halir() function will be used.
        
        pcs should be a list of phase-cycles in radians.  If pcs=None, it will be
        determined as I.size equally spaced phasce-cycles on the interval [0, 2pi).
        
        Implements algorithm described in:
            Shcherbakova, Yulia, et al. "PLANET: an ellipse fitting approach for
            simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
            free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.


```


## mr_utils.recon.tv_denoising.tv_denoising

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/recon/tv_denoising/tv_denoising.py)

```
NAME
    mr_utils.recon.tv_denoising.tv_denoising - Port of TVL1denoise - TV-L1 image denoising with the primal-dual algorithm.

DESCRIPTION
    See:
    https://www.mathworks.com/matlabcentral/fileexchange/57604-tv-l1-image-denoising-algorithm

FUNCTIONS
    tv_l1_denoise(im, lam, disp=False, niter=100)
        TV-L1 image denoising with the primal-dual algorithm.
        
        im -- image to be processed
        lam -- regularization parameter controlling the amount of denoising;
               smaller values imply more aggressive denoising which tends to
               produce more smoothed results
        disp -- print energy being minimized each iteration
        niter -- number of iterations


```


# SIM
## mr_utils.sim.bloch.bloch

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/bloch/bloch.py)

```
NAME
    mr_utils.sim.bloch.bloch - Numerical bloch simulations using finite difference method.

FUNCTIONS
    gre(T1, T2, M0, Nt, h, alpha, beta, gamma, TR, TE, Bx=0, By=0, Bz=3)
        Finite difference Bloch simulation of spoiled GRE pulse sequence.
        
        T1 -- longitudinal relaxation constant.
        T2 -- transverse relaxation constant.
        M0 -- value at thermal equilibrium.
        Nt -- number of time points for finite difference solution.
        h -- step size for finite difference solutions.
        alpha,beta,gamma -- RF pulse tip angles.
        TR -- repetition time.
        TE -- echo time.
        Bx -- x component of magnetic field.
        By -- y component of magnetic field.
        Bz -- z component of magnetic field.
        
        T1,T2,M0 can be arrays (must be same size) to simulate phantoms.
    
    rotation(alpha, beta, gamma)
        Create 3D rotation matrix from alpha,beta,gamma.
    
    sim(T1, T2, M0, Nt, h, alpha, beta, gamma, Bx=0, By=0, Bz=3)
        Finite difference solution to Bloch equations.
        
        T1 -- longitudinal relaxation constant.
        T2 -- transverse relaxation constant.
        M0 -- value at thermal equilibrium.
        Nt -- number of time points for finite difference solution.
        h -- step size for finite difference solutions.
        alpha,beta,gamma -- RF pulse tip angles.
        Bx -- x component of magnetic field.
        By -- y component of magnetic field.
        Bz -- z component of magnetic field.
        
        T1,T2,M0 can be arrays (must be same size) to simulate phantoms.
        
        See:
        https://en.wikipedia.org/wiki/Bloch_equations#Matrix_form_of_Bloch_equations
    
    sim_loop(T1, T2, M0, Nt, h, alpha, beta, gamma, Bx=0, By=0, Bz=3)
        Loop implementation to verify matrix implementation.


```


## mr_utils.sim.gre.gre

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/gre/gre.py)

```
NAME
    mr_utils.sim.gre.gre - GRE simulations.

FUNCTIONS
    ernst(TR, T1)
        Computes the Ernst angle.
        
        TR -- repetition time.
        T1 -- longitudinal exponential decay time constant.
        
        Implements equation [14.9] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    fzss(T1, TR, alpha=None)
        Dimensionless measure of steady-state longitudinal magnetization.
        
        T1 -- longitudinal exponential decay time constant.
        TR -- repetition time.
        alpha -- flip angle.
        
        alpha=None will use the Ernst angle.
        
        Implements equation [14.7] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    gre_sim(T1, T2, TR=0.012, TE=0.006, alpha=1.0471975511965976, field_map=None, phi=0, dphi=0, M0=1, tol=1e-05, maxiter=None, spoil=True)
        Simulate GRE pulse sequence.
        
        T1 -- longitudinal exponential decay time constant.
        T2 -- Transverse exponential decay time constant.
        TR -- repetition time.
        TE -- echo time.
        alpha -- flip angle.
        field_map -- offresonance field map (in hertz).
        phi -- Reference starting phase.
        dphi -- phase  cycling of RF pulses.
        M0 -- proton density.
        tol -- Maximum difference between voxel intensity iter to iter until stop.
        maxiter -- number of excitations till steady state.
        
        maxiter=None will run until difference between all voxel intensities
        iteration to iteration is within given tolerance, tol (default=1e-5).
        
        Returns complex transverse magnetization (Mx + 1j*My)
    
    gre_sim_loop(T1, T2, TR=0.012, TE=0.006, alpha=1.0471975511965976, field_map=None, dphi=0, M0=1, maxiter=200)
        Simulate GRE pulse sequence.
        
        T1 -- longitudinal exponential decay time constant.
        T2 -- Transverse exponential decay time constant.
        TR -- repetition time.
        TE -- echo time.
        alpha -- flip angle.
        field_map -- offresonance field map (in hertz).
        dphi -- phase  cycling of RF pulses.
        M0 -- proton density.
        maxiter -- number of excitations till steady state.
    
    spoiled_gre(T1, T2star, TR, TE, alpha=None, M0=1)
        Spoiled, steady state GRE contrast simulation.
        
        T1 -- longitudinal exponential decay time constant.
        T2star -- Effective transverse exponential decay time constant.
        TR -- repetition time.
        TE -- echo time.
        alpha -- flip angle.
        M0 -- proton density.
        
        alpha=None will use the Ernst angle.
        
        Assuming a longitudinal steady-state and perfect spoiling. Note that
        dependence is on T2* rather than T2 because SE/STE formation is suppressed
        by spoiling and the signal is generated by gradient refocusing of an FID.
        
        Implements equation [14.8] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.
    
    spoiled_gre_k(T1, T2star, TR, TE, alpha=None, M0=1, k=1)
        Spoiled GRE contrast simulation for k excitation pulses.
        
        See spoiled_gre().
        k -- Number of excitation pulses the magnetization experiences.
        
        alpha=None will use the Ernst angle.
        
        Implements equations [14.10-11] from:
            Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
            Handbook of MRI pulse sequences. Elsevier.


```


## mr_utils.sim.motion.motion

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/motion/motion.py)

```
NAME
    mr_utils.sim.motion.motion

FUNCTIONS
    cartesian_acquire(im, im_dims, pos, time_grid)
    
    create_frames(im, traj, backfill=0)
    
    create_frames_from_position(im, im_dims, positions, time_grid)
    
    play(frames)


```


## mr_utils.sim.noise.rayleigh

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/noise/rayleigh.py)

```
NAME
    mr_utils.sim.noise.rayleigh

FUNCTIONS
    rayleigh(M, sigma)
        Generates Rayleigh distribution of pixel intensity M.
        
        Generates the noise distribution of magnitude MR image areas where only
        noise is present. This distribution governs the noise in image regions with
        no NMR signal.
        
        M -- measured image pixel intensity
        sigma -- standard deviation of the Gaussian noise in the real and the
                 imaginary images (which we assume to be equal)
        
        pM -- computed probability distribution of M
        
        Computes Equation [2] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    
    rayleigh_mean(sigma)
        Mean of the Rayleigh distribution with standard deviation sigma.
        
        Computes Equation [3] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.
    
    rayleigh_variance(sigma)
        Variance of the Rayleigh distribution with standard deviation sigma.
        
        Computes Equation [4] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.


```


## mr_utils.sim.noise.rician

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/noise/rician.py)

```
NAME
    mr_utils.sim.noise.rician

FUNCTIONS
    rician(M, A, sigma)
        Generates rician distribution of pixel intensity M.
        
        Generates the noise distribution of a magnitude MR image.
        
        M -- measured image pixel intensity
        A -- image pixel intensity in the absence of noise
        sigma -- standard deviation of the Gaussian noise in the real and the
                 imaginary images (which we assume to be equal)
        
        pM -- computed probability distribution of M
        
        Computes Equation [1] from:
        Gudbjartsson, Hákon, and Samuel Patz. "The Rician distribution of noisy MRI
            data." Magnetic resonance in medicine 34.6 (1995): 910-914.


```


## mr_utils.sim.single_voxel.single_voxel

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/single_voxel/single_voxel.py)

```
NAME
    mr_utils.sim.single_voxel.single_voxel

FUNCTIONS
    combine_images(im0, im1)
    
    single_voxel_imaging(im, patch_size)


```


## mr_utils.sim.ssfp.param_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/param_mapping.py)

```
NAME
    mr_utils.sim.ssfp.param_mapping

FUNCTIONS
    gen_dictionary(t1t2alpha, TR, TE)
    
    ssfp(T1, T2, alpha, TR, TE, fs, dphi, phi=0, M0=1)


```


## mr_utils.sim.ssfp.quantitative_field_mapping

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/quantitative_field_mapping.py)

```
NAME
    mr_utils.sim.ssfp.quantitative_field_mapping - Quantitative field mapping for bSSFP.

DESCRIPTION
    Collect quantitative MR maps (T1, T2, flip angle), then, assuming that these
    won't change during the duration of the scan, we can use these to take a single
    bSSFP scan each time point and solve for the off-resonance.  Thus we get a
    field map at time point.

FUNCTIONS
    get_df_responses(T1, T2, PD, TR, alpha, phase_cyc, dfs)
        Simulate bSSFP response across all possible off-resonances.
        
        T1 -- scalar T1 longitudinal recovery value in seconds.
        T2 -- scalar T2 transverse decay value in seconds.
        PD -- scalar proton density value scaled the same as acquisiton.
        TR -- Repetition time in seconds.
        alpha -- Flip angle in radians.
        phase_cyc -- RF phase cycling in radians.
        dfs -- Off-resonance values to simulate over.
    
    quantitative_fm(Mxys, dfs, T1s, T2s, PDs, TR, alpha, phase_cyc, mask=None)
        Find field map given quantitative maps.
    
    quantitative_fm_scalar(Mxy, dfs, T1, T2, PD, TR, alpha, phase_cyc)
        For scalar T1,T2,PD


```


## mr_utils.sim.ssfp.ssfp

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/ssfp.py)

```
NAME
    mr_utils.sim.ssfp.ssfp - SSFP constrast simulation functions.

FUNCTIONS
    elliptical_params(T1, T2, TR, alpha, M0=1)
        Return ellipse parameters M,a,b.
        
        T1 -- longitudinal exponential decay time constant.
        T2 -- transverse exponential decay time constant.
        TR -- repetition time.
        alpha -- flip angle.
        
        Outputs are the parameters of ellipse an ellipse, (M,a,b).  These
        parameters do not depend on theta.
        
        Implementation of equations [3-5] in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    get_bssfp_phase(TR, field_map, delta_cs=0, phi_rf=0, phi_edd=0, phi_drift=0)
        Additional bSSFP phase factors.
        
        TR -- repetition time.
        field_map -- off-resonance map (Hz).
        delta_cs -- chemical shift of species w.r.t. the water peak (Hz).
        phi_rf -- RF phase offset, related to the combin. of Tx/Rx phases (rad).
        phi_edd -- phase errors due to eddy current effects (rad).
        phi_drift -- phase errors due to B0 drift (rad).
        
        This is exp(-i phi) from end of p. 930 in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
        
        In Hoff's paper the equation is not explicitly given for phi, so we
        implement equation [5] that gives more detailed terms, found in
            Shcherbakova, Yulia, et al. "PLANET: An ellipse fitting approach for
            simultaneous T1 and T2 mapping using phase‐cycled balanced steady‐state
            free precession." Magnetic resonance in medicine 79.2 (2018): 711-722.
    
    get_cart_elliptical_params(M, a, b)
        Get parameters needed for cartesian representation of ellipse.
    
    get_center_of_mass(M, a, b)
        Give center of mass a function of ellipse parameters.
    
    get_center_of_mass_nmr(T1, T2, TR, alpha, M0=1)
        Give center of mass as a function of NMR parameters.
    
    get_complex_cross_point(I1, I2, I3, I4)
        Find the intersection of two straight lines connecting diagonal pairs.
        
        (xi,yi) are the real and imaginary parts of complex valued pixels in four
        bSSFP images denoted Ii and acquired with phase cycling dtheta = (i-1)*pi/2
        with 0 < i <= 4.
        
        This is Equation [13] from:
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    get_cross_point(I1, I2, I3, I4)
        Find the intersection of two straight lines connecting diagonal pairs.
        
        (xi,yi) are the real and imaginary parts of complex valued pixels in four
        bSSFP images denoted Ii and acquired with phase cycling dtheta = (i-1)*pi/2
        with 0 < i <= 4.
        
        This are Equations [11-12] from:
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
        
        There is  a typo in the paper for equation [12] fixed in this
        implementation.  The first term of the numerator should have (y2 - y4)
        instead of (x2 - y4) as written.
    
    get_geo_center(M, a, b)
        Get geometric center of ellipse.
    
    get_theta(TR, field_map, phase_cyc=0)
        Get theta, spin phase per repetition time, given off-resonance.
        
        Equation for theta=2*pi*df*TR is in Appendix A of
            Hargreaves, Brian A., et al. "Characterization and reduction of the
            transient response in steady‐state MR imaging." Magnetic Resonance in
            Medicine: An Official Journal of the International Society for Magnetic
            Resonance in Medicine 46.1 (2001): 149-158.
    
    make_cart_ellipse(xc, yc, A, B, num_t=100)
        Make a cartesian ellipse, return x,y coordinates for plotting.
    
    spectrum(T1, T2, TR, alpha)
        Generate an entire period of the bSSFP signal profile.
    
    ssfp(T1, T2, TR, alpha, field_map, phase_cyc=0, M0=1)
        SSFP transverse signal right after RF pulse.
        
        T1 -- longitudinal exponential decay time constant.
        T2 -- transverse exponential decay time constant.
        TR -- repetition time.
        alpha -- flip angle.
        field_map -- B0 field map.
        M0 -- proton density.
        
        Implementation of equations [1-2] in
            Xiang, Qing‐San, and Michael N. Hoff. "Banding artifact removal for
            bSSFP imaging with an elliptical signal model." Magnetic resonance in
            medicine 71.3 (2014): 927-933.
    
    ssfp_from_ellipse(M, a, b, TR, field_map, phase_cyc=0)
        Simulate banding artifacts given elliptical signal params and field map.
    
    ssfp_old(T1, T2, TR, alpha, field_map, phase_cyc=0, M0=1)
        Legacy SSFP sim code.  Try using current SSFP function.


```


## mr_utils.sim.ssfp.ssfp_dictionary

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/ssfp/ssfp_dictionary.py)

```
NAME
    mr_utils.sim.ssfp.ssfp_dictionary - Dictionary lookup of NMR parameters given bSSFP signal.

FUNCTIONS
    find_atom(sig, D, keys)
        Find params of dictionary atom closest to observed signal profile.
    
    get_keys(T1s, T2s, alphas)
        Generate matrix of params [T1,T2,alpha] to generate a dictionary.
        
        T1,T2 are chosen to be feasible, i.e., T1 >= T2.
    
    ssfp_dictionary(T1s, T2s, TR, alphas, df)
        Generate a dicionary of bSSFP profiles given parameters.
        
        T1s -- (1D) all T1 decay constant values to simulate.
        T2s -- (1D) all T2 decay constant values to simulate.
        TR -- repetition time for bSSFP simulation.
        alphas -- (1D) all flip angle values to simulate.
        df -- (1D) off-resonance frequencies over which to simulate.
        
        T1s,T2s,alphas should all be 1D arrays.  All feasible combinations will be
        simulated (i.e., where T1 >= T2).  The dictionary and keys are returned.
        Each dictionary column is the simulation over frequencies df.  The keys are
        a list of tuples: (T1,T2,alpha).
    
    ssfp_dictionary_for_loop(T1s, T2s, TR, alphas, df)
        Verification for ssfp_dictionary generation.


```


## mr_utils.sim.traj.cartesian

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/traj/cartesian.py)

```
NAME
    mr_utils.sim.traj.cartesian - Create sampling patterns for Cartesian k-space trajectories.

FUNCTIONS
    cartesian_gaussian(shape, undersample=(0.5, 0.5), reflines=20)
        Undersample in Gaussian pattern.
    
    cartesian_pe(shape, undersample=0.5, reflines=20)
        Randomly collect Cartesian phase encodes (lines).
        
        shape -- Shape of the image to be sampled.
        undersample -- Undersampling factor (0 < undersample <= 1).
        reflines -- Number of lines in the center to collect regardless.


```


## mr_utils.sim.traj.radial

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/traj/radial.py)

```
NAME
    mr_utils.sim.traj.radial - Generate radial sampling masks.

FUNCTIONS
    radial(shape, num_spokes, theta=None, skinny=True, extend=False)
        Create 2d binary radial sampling pattern.
        
        shape -- x,y dimensions of sampling pattern.
        num_spokes -- Number of spokes to simulate.
        theta -- Angle between spokes (rad).
        skinny -- Garuantee 1px spoke width.
        extend -- Extend spokes to the edge of array.
        
        If theta=None, use golden angle. If skinny=True, edges of spokes with large
        slope may be curved. If extend=False, spokes confined in a circle.
    
    radial_golden_ratio_meshgrid(X, Y, num_spokes)
        Create 2d binary golden angle radial sampling pattern.
        
        X,Y -- Meshgrid.
        num_spokes -- Number of spokes to simulate.
        
        Issues:
            For steep slopes, the spokes don't make it all the way to the edge of
            the image and they curve (from the skeletonize)...


```


# TEST_DATA
## mr_utils.test_data.coils.csm

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/coils/csm.py)

```
NAME
    mr_utils.test_data.coils.csm

FUNCTIONS
    simple_csm(N, dims=(64, 64))
        Generate coil channel sensitivities as linear gradients in N directions.
        
        N -- number of coil sensitivities to generate.
        dims -- tuple of dimensions.
        
        N linear gradient gradients of size dims will be generated.  These are
        simple because all we're doing is generating linear gradients at evenly
        spaced angles so the resulting maps are square.
        
        TODO: sensitivity maps also need phases, as in:
        ismrmrdtools.simulation.generate_birdcage_sensitivities
        
        Returns (N x dims[0] x dims[1]) array.


```


## mr_utils.test_data.optimization_functions.functions

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/optimization_functions/functions.py)

```
NAME
    mr_utils.test_data.optimization_functions.functions - Test functions for optimization.

DESCRIPTION
    See:
        https://en.wikipedia.org/wiki/Test_functions_for_optimization

FUNCTIONS
    ackley(x, a=20, b=0.2, c=6.283185307179586)
        Ackley function.
    
    beale(x)
        Beale function.
        
        Only for 2d x.
    
    bohachevsky1(x)
        Bohachevsky function 1.
        Only for 2d x.
    
    bohachevsky2(x)
        Bohachevsky function 2.
        Only for 2d x.
    
    bohachevsky3(x)
        Bohachevsky function 3.
        Only for 2d x.
    
    grad_ackley(f, x, a=20, b=0.2, c=6.283185307179586)
        Gradient of Ackley function.
    
    grad_bohachevsky1(f, x)
        Gradient of Bohachevsky function 1.
    
    grad_bohachevsky2(f, x)
        Gradient of Bohachevsky function 2.
    
    grad_bohachevsky3(f, x)
        Gradient of Bohachevsky function 3.
    
    grad_quadratic(f, x)
    
    quadratic(x)
    
    rastrigin(x, A=10)
        Rastrigin function.
    
    rosenbrock(x, a=1, b=100)
        Rosenbrock's function.
    
    sphere(x)
        Sphere function.


```


## mr_utils.test_data.phantom.binary_smiley

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/phantom/binary_smiley.py)

```
NAME
    mr_utils.test_data.phantom.binary_smiley - Simple numerical phantom shaped like a smiley face.  Value either 1 or 0.

FUNCTIONS
    binary_smiley(N, radius=0.75)
        Binary smiley face numerical phantom.
        
        N -- Height and width in pixels.
        radius -- Radius of circle used for head.


```


## mr_utils.test_data.phantom.cylinder_2d

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/phantom/cylinder_2d.py)

```
NAME
    mr_utils.test_data.phantom.cylinder_2d - Simple cylindrical phantoms generated with different contrasts.

FUNCTIONS
    bssfp_2d_cylinder(TR=0.006, alpha=1.0471975511965976, dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5, field_map=None, phase_cyc=0, kspace=False)
        Simulates axial bSSFP scan of cylindrical phantom.
        
        TR -- Repetition time.
        alpha -- Flip angle.
        dims -- Matrix size, (dim_x,dim_y)
        FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
        radius -- Radius of cylinder in arbitrary units.
        field_map -- (dim_x,dim_y) field map. If None, linear gradient in x used.
        phase_cyc -- Phase cycling used in simulated bSSFP acquisition.
        kspace -- Whether or not to return data in kspace or imspace.
    
    cylinder_2d(dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5, params=None)
        Base 2d cylinder maps to feed to contrast simulations.
    
    cylinder_2d_params()
        Returns properties of numerical phantom used in cylinder_2d.
    
    spgr_2d_cylinder(TR=0.3, TE=0.003, alpha=1.0471975511965976, dims=(64, 64), FOV=((-1, 1), (-1, 1)), radius=0.5, field_map=None, kspace=False)
        Simulates axial spoiled GRE scan of cylindrical phantom.
        
        TR -- Repetition time.
        TE -- Echo time.
        alpha -- Flip angle.
        dims -- Matrix size, (dim_x,dim_y)
        FOV -- Field of view in arbitrary units, ( (x_min,x_max), (y_min,y_max) )
        radius -- Radius of cylinder in arbitrary units.
        kspace -- Whether or not to return data in kspace or imspace.


```


## mr_utils.test_data.phantom.phantom

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/phantom/phantom.py)

```
NAME
    mr_utils.test_data.phantom.phantom

DESCRIPTION
    To Generate phantoms. You can call the following functions with the
    desired phantom shape as input :
    - modified_shepp_logan
    - shepp_logan
    - yu_ye_wang
    You can generate a custom phantom by specifying a list of
    ellipsoid parameters by calling the phantom function.
    Ellipsoid parameters are as follows:
    - A : value inside the ellipsoid
    - a, b, c : axis length of the ellipsoid (in % of the cube shape)
    - x0, y0, z0 : position of the center (in % of the cube shape)
    - phi, theta, psi : Euler angles defining the orientation (in degrees)
    Alternatively, you can generate only one ellipsoid by calling
    the ellipsoid function.
    Exemple
    -------
    To generate a phantom cube of size 32 * 32 * 32 :
    >>> from siddon.phantom import *
    >>> my_phantom = shepp_logan((32, 32, 32))
    >>> assert my_phantom[16, 16, 16] == -0.8
    Notes
    -----
    You can take a look at those links for explanations:
    http://en.wikipedia.org/wiki/Imaging_phantom
    http://en.wikipedia.org/wiki/Ellipsoid
    http://en.wikipedia.org/wiki/Euler_angles
    This module is largely inspired by :
    http://www.mathworks.com/matlabcentral/fileexchange/9416-3d-shepp-logan-phantom
    Author
    ------
    Nicolas Barbey

FUNCTIONS
    modified_shepp_logan(shape, **kargs)
        # define specific functions
    
    phantom(shape, parameters_list, dtype=<class 'numpy.float64'>)
        Generate a cube of given shape using a list of ellipsoid
        parameters.
        Inputs
        ------
        shape: tuple of ints
            Shape of the output cube.
        parameters_list: list of dictionaries
            List of dictionaries with the parameters defining the ellipsoids to
            include in the cube.
        dtype: data-type
            Data type of the output ndarray.
        Output
        ------
        cube: 3-dimensional ndarray
            A 3-dimensional ndarray filled with the specified ellipsoids.
        See Also
        --------
        shepp_logan : Generates the Shepp Logan phantom in any shape.
        modified_shepp_logan : Modified Shepp Logan phantom in any shape.
        yu_ye_wang : The Yu Ye Wang phantom in any shape.
        ellipsoid : Generates a cube filled with an ellipsoid of any shape.
        Notes
        -----
        http://en.wikipedia.org/wiki/Imaging_phantom
    
    shepp_logan(shape, **kargs)
    
    yu_ye_wang(shape, **kargs)

```


## mr_utils.test_data.test_data

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/test_data/test_data.py)

```
NAME
    mr_utils.test_data.test_data

CLASSES
    builtins.object
        AMPData
        BARTReordering
        BSSFPGrappa
        EllipticalSignal
        GRAPPA
        GadgetronClient
        GadgetronTestConfig
        SCGROG
        SCRReordering
        SSFPMultiphase
        ViewTestData
        XProtParserTest
    
    class AMPData(builtins.object)
     |  ## MAT FILES
     |  # For AMP:
     |  
     |  Static methods defined here:
     |  
     |  cdf97()
     |  
     |  mask()
     |  
     |  x0()
     |  
     |  y()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class BARTReordering(builtins.object)
     |  # For BART reordering recon
     |  
     |  Static methods defined here:
     |  
     |  ksp_sim()
     |  
     |  lowres_img()
     |  
     |  lowres_ksp()
     |  
     |  reco1()
     |  
     |  reco2()
     |  
     |  sens()
     |  
     |  traj_rad2()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class BSSFPGrappa(builtins.object)
     |  # For Gadgetron GRAPPA Examples
     |  
     |  Static methods defined here:
     |  
     |  pc0_r2()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class EllipticalSignal(builtins.object)
     |  # For elliptical signal model:
     |  
     |  Static methods defined here:
     |  
     |  CS()
     |  
     |  I()
     |  
     |  I1()
     |  
     |  I2()
     |  
     |  I3()
     |  
     |  I4()
     |  
     |  I_max_mag()
     |  
     |  Id()
     |  
     |  w13()
     |  
     |  w24()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class GRAPPA(builtins.object)
     |  # For GRAPPA Recon
     |  
     |  Static methods defined here:
     |  
     |  Im_Recon()
     |  
     |  S()
     |  
     |  S_ch()
     |  
     |  S_ch_new()
     |  
     |  S_ch_new_temp()
     |  
     |  S_ch_temp()
     |  
     |  S_new()
     |  
     |  T()
     |  
     |  T_ch_new_M()
     |  
     |  T_new()
     |  
     |  W()
     |  
     |  csm()
     |  
     |  phantom_ch()
     |  
     |  phantom_ch_k()
     |  
     |  phantom_ch_k_acl()
     |  
     |  phantom_ch_k_u()
     |  
     |  phantom_shl()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class GadgetronClient(builtins.object)
     |  ## HDF5 FILES
     |  # For gadgetron
     |  
     |  Static methods defined here:
     |  
     |  epi_input_filename()
     |      Gadgetron test data.
     |      http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/epi/epi_2d_out_20161020_pjv.h5
     |  
     |  generic_cartesian_grappa_filename()
     |      Gadgetron test data.
     |      http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/tse/meas_MID00450_FID76726_SAX_TE62_DIR_TSE/ref_20160319.dat
     |  
     |  grappa_input_filename()
     |  
     |  input_filename()
     |  
     |  input_h5()
     |  
     |  raw_input_filename()
     |  
     |  true_output_data()
     |  
     |  true_output_data_grappa_cpu()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class GadgetronTestConfig(builtins.object)
     |  ## XML FILES
     |  # For gadgetron
     |  
     |  Static methods defined here:
     |  
     |  default_config()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SCGROG(builtins.object)
     |  # For SC-GROG:
     |  
     |  Static methods defined here:
     |  
     |  grog_result()
     |  
     |  gx_gy_results()
     |  
     |  test_gridder_data_4D()
     |  
     |  test_grog_data_4D()
     |  
     |  test_gx_gy_data()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SCRReordering(builtins.object)
     |  # For scr_reordering_adluru:
     |  
     |  Static methods defined here:
     |  
     |  Coil1_data()
     |  
     |  TV_re_order()
     |  
     |  TV_term_update()
     |  
     |  fidelity_update()
     |  
     |  mask()
     |  
     |  recon()
     |  
     |  recon_at_iter_1()
     |  
     |  recon_at_iter_10()
     |  
     |  recon_at_iter_100()
     |  
     |  recon_at_iter_2()
     |  
     |  recon_at_iter_50()
     |  
     |  true_orderings()
     |  
     |  tv_prior()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SSFPMultiphase(builtins.object)
     |  ## NPY FILES
     |  # For ssfp multiphase:
     |  
     |  Methods defined here:
     |  
     |  ssfp_ankle_te_6_pc_180()
     |  
     |  ssfp_ankle_te_6_pc_90()
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  ssfp_ankle_te_6_pc_0()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class ViewTestData(builtins.object)
     |  # For VIEW testing:
     |  
     |  Static methods defined here:
     |  
     |  ssfp_ankle_te_6_pc_0()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class XProtParserTest(builtins.object)
     |  ## XPROT FILES
     |  # For xprot_parser
     |  
     |  Static methods defined here:
     |  
     |  full_sample_xprot()
     |  
     |  sample_xprot()
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
    
    do_planet_rotation(I)
        Rotate complex points to fit vertical ellipse centered at (xc, 0).
        
        I -- Complex points from SSFP experiment.
    
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
    
    rotate_points(x, y, phi, p=(0, 0))
        Rotate points x, y through angle phi w.r.t. point p.
        
        x, y -- Points to be rotated.
        phi -- Angle in radians to rotate points.
        p -- Point to rotate around.


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


# VIEW
## mr_utils.view.view

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/view/view.py)

```
NAME
    mr_utils.view.view - A simple viewer.

DESCRIPTION
    The idea is for this to be really simple to use.  It will do a lot of
    guessing if you don't provide it with details.  For example, if a 3D dataset
    is provided as the image and you don't say which axes are in-plane, it will
    guess that the largest two axis are in-plane.  If the 3rd dimension is small,
    then it will choose to view the images as a montage, if it is large it will
    play it as a movie.  Of course there are many options if you know what you're
    doing (and I do, since I wrote it...).
    
    Fourier transforms, logarithmic scale, coil combination, averaging, and
    converting from raw data are all supported out of the box.

FUNCTIONS
    mat_keys(filename, ignore_dbl_underscored=True, no_print=False)
        Give the keys found in a .mat filcoil_ims,coil_dim=-1,n_components=4e.
        
        filename -- .mat filename.
        ignore_dbl_underscored -- Remove keys beginng with two underscores.
    
    view(image, load_opts=None, is_raw=None, is_line=None, prep=None, fft=False, fft_axes=None, fftshift=None, avg_axis=None, coil_combine_axis=None, coil_combine_method='walsh', coil_combine_opts=None, is_imspace=False, mag=None, phase=False, log=False, imshow_opts={'cmap': 'gray'}, montage_axis=None, montage_opts={'padding_width': 2}, movie_axis=None, movie_repeat=True, save_npy=False, debug_level=10, test_run=False)
        Image viewer to quickly inspect data.
        
        image -- Name of the file including the file extension or numpy array.
        load_opts -- Options to pass to data loader.
        
        is_raw -- Inform if data is raw. Will attempt to guess from extension.
        is_line -- Whether or not this is a line plot (as opposed to image).
        prep -- Lambda function to process the data before it's displayed.
        
        fft -- Whether or not to perform n-dimensional FFT of data.
        fft_axes -- Axis to perform FFT over, determines dimension of n-dim FFT.
        fftshift -- Whether or not to perform fftshift. Defaults to True if fft.
        
        avg_axis -- Take average over given set of axes.
        coil_combine_axis -- Which axis to perform coil combination over.
        coil_combine_method -- Method to use to combine coils.
        coil_combine_opts -- Options to pass to the coil combine method.
        is_imspace -- Whether or not the data is in image space. For coil combine.
        
        mag -- View magnitude image. Defaults to True if data is complex.
        phase -- View phase image.
        log -- View log of magnitude data. Defaults to False.
        imshow_opts -- Options to pass to imshow. Defaults to { 'cmap'='gray' }.
        
        montage_axis -- Which axis is the number of images to be shown.
        montage_opts -- Additional options to pass to the skimage.util.montage.
        
        movie_axis -- Which axis is the number of frames of the movie.
        movie_repeat -- Whether or not to put movie on endless loop.
        
        save_npy -- Whether or not to save the output as npy file.
        
        debug_level -- Level of verbosity. See logging module.
        test_run -- Doesn't show figure, returns debug object. Mostly for testing.


```

