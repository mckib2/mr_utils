
## mr_utils.cs.models.UFT

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/cs/models/UFT.py)

```
NAME
    mr_utils.cs.models.UFT

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

