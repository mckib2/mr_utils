
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

