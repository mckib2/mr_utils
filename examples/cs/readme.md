
# CS
## examples.cs.amp

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/amp.py)

```
NAME
    examples.cs.amp - Approximate message passing algorithm example.

DESCRIPTION
    This is a sanity check example to make sure we can recreate the results from
    the reference implementation.  See mr_utils.cs.amp2d for details.


```


## examples.cs.binary_2d_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/binary_2d_iht.py)

```
NAME
    examples.cs.binary_2d_iht - # Not sure if this works...


```


## examples.cs.binary_convex

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/binary_convex.py)

```
NAME
    examples.cs.binary_convex - Example of solving CS binary reconstruction problem using scipy.minimize.

DESCRIPTION
    I don't think this is the best way of solving this, you can get much better
    reconstructions using a simple gradient descent algorithm.  Nonetheless, I'd
    never seen anyone do it this way, so I said, "What the heck?!"

FUNCTIONS
    grad(x, A, y, lamb, beta=2.220446049250313e-16)
        d/dx_i || Ax - y ||_2^2 + lambda*|| x ||_1
        
        x -- Current image estimate.
        A -- CS measurement matrix.
        y -- Measured samples, i.e., y = A.dot(x_true).
        lamb -- Lambda, tradeoff between fidelity and sparsity constraint terms.
        beta -- Small, nonnegative constant, e.g., make 1/(x+beta) defined.
    
    obj(x, A, y, lamb)
        || Ax - y ||_2^2 + lambda*|| x ||_1
        
        x -- Current image estimate.
        A -- CS measurement matrix.
        y -- Measured samples, i.e., y = A.dot(x_true).
        lamb -- Lambda, tradeoff between fidelity and sparsity constraint terms.


```


## examples.cs.binary_cosamp

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/binary_cosamp.py)

```
NAME
    examples.cs.binary_cosamp - Simple binary CS reconstruction using CoSaMP.


```


## examples.cs.binary_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/binary_iht.py)

```
NAME
    examples.cs.binary_iht - Simple binary CS reconstruction using iterative hard thresholding.

DESCRIPTION
    Encoding matrix, A, is random (normal distribution) and the signal is of
    course sparse in the signal domain.


```


## examples.cs.binary_ist

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/binary_ist.py)

```
NAME
    examples.cs.binary_ist - Binary CS reconstruction using iterative soft thresholding.

DESCRIPTION
    Identical to set up of binary IHT example.


```


## examples.cs.binary_niht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/binary_niht.py)

```
NAME
    examples.cs.binary_niht - Binary CS reconstruction using normalized iterative hard thresholding.

DESCRIPTION
    Same setup as binary IHT example.


```


## examples.cs.convex

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/convex.py)

```
NAME
    examples.cs.convex - # How is this different from binary_convex.py?

FUNCTIONS
    grad(x, A, y, lamb, beta=2.220446049250313e-16)
        d/dx_i || Ax - y ||_2^2 + lambda*|| x ||_1
        
        x -- Current image estimate.
        A -- CS measurement matrix.
        y -- Measured samples, i.e., y = A.dot(x_true).
        lamb -- Lambda, tradeoff between fidelity and sparsity constraint terms.
        beta -- Small, nonnegative constant, e.g., make 1/(x+beta) defined.
    
    obj(x, A, y, lamb)
        || Ax - y ||_2^2 + lambda*|| x ||_1
        
        x -- Current image estimate.
        A -- CS measurement matrix.
        y -- Measured samples, i.e., y = A.dot(x_true).
        lamb -- Lambda, tradeoff between fidelity and sparsity constraint terms.


```


## examples.cs.dft_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/dft_iht.py)

```
NAME
    examples.cs.dft_iht - Example of complex valued binary CS reconstruction using IHT.

DESCRIPTION
    Signal is 1-sparse, a single atom from DFT dictionary.


```


## examples.cs.radial_binary_2d_fd_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/radial_binary_2d_fd_iht.py)

```
NAME
    examples.cs.radial_binary_2d_fd_iht

FUNCTIONS
    time(...)
        time() -> floating point number
        
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.


```


## examples.cs.radial_binary_2d_fd_iht_uft

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/radial_binary_2d_fd_iht_uft.py)

```
NAME
    examples.cs.radial_binary_2d_fd_iht_uft - # THIS DOESN'T WORK YET, BY THE WAY...

FUNCTIONS
    time(...)
        time() -> floating point number
        
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.


```


## examples.cs.selective_updates

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/selective_updates.py)

```
NAME
    examples.cs.selective_updates - Selectively update the image estimate each iteration.

DESCRIPTION
    Golden anlge radially sampled binary smiley face.  Choose proximal gradient
    descent enforcing sparsity in the wavelet domain.
    
    The idea is that we only want to update the locations that we're sure need to
    updated.  The way I've chosen to do this is to look at the difference between
    the previous iteration and next iteration and choose a percentage of the
    locations with the highest change to be updated.  Selectively updating seems
    to do a better job of not producing signal in empty space, but reduces
    homogeneity inside the face and we loose definition of eyes and mouth.
    Reordering also might help -- I'm most interested in this as a way to come up
    with a good prior, either for reordering or location contrained reconstruction.
    
    Also, choosing to reorder slows us down quite a bit...  Need to work on that.


```


## examples.cs.threshold_real_imag

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/threshold_real_imag.py)

```
NAME
    examples.cs.threshold_real_imag - Example demonstrating the differences between thresholding methods.

DESCRIPTION
    We can:
        Threshold the complex signal
        Threshold the real/imag parts separately.


```


## examples.cs.tv_iht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/tv_iht.py)

```
NAME
    examples.cs.tv_iht - Total variation example using iterative hard thresholding.

DESCRIPTION
    This is actually a dumb example, because the assumption we make a square wave
    which turns out to be a binary signal in finite differences domain, but it's
    treated as the sample problem as binary_iht.py.  Sorry about that.
    The measurements should actually be taken in the nonsparse domain (i.e.,
    y = As instead of y = Ax).


```


## examples.cs.tv_riht

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/cs/tv_riht.py)

```
NAME
    examples.cs.tv_riht - # I don't think this works yet


```

