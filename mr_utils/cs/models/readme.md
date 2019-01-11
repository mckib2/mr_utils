
## mr_utils.cs.models.UFT

[Source](../master/mr_utils/cs/models/UFT.py)

```
NAME
    mr_utils.cs.models.UFT

CLASSES
    builtins.object
        UFT
    
    class UFT(builtins.object)
     |  Undersampled Fourier Transform (UFT) data acquisiton model.
     |  
     |  Developed for use with iterative thresholding algorithms. Implements
     |  functions to look like a numpy array:
     |      .dot() -- Forward transform.
     |      .conj().T -- Inverse transform.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, samp)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  conj(self)
     |  
     |  dot(self, m)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  T
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)


```

