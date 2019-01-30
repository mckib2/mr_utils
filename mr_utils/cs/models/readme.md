
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

