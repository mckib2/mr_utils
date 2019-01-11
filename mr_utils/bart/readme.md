
# BART
## mr_utils.bart.bart

[Source](../master/mr_utils/bart/bart.py)

```
NAME
    mr_utils.bart.bart

FUNCTIONS
    bart(*args)
        Wrapper that passes arguments to BART installation.

```


## mr_utils.bart.bartholomew

[Source](../master/mr_utils/bart/bartholomew.py)

```
NAME
    mr_utils.bart.bartholomew

CLASSES
    builtins.object
        BartholomewObject
    
    class BartholomewObject(builtins.object)
     |  More friendly python interface for BART.
     |  
     |  I also want this to be able to run BART on remote computer through ssh, to
     |  remove BART as a strict dependency for the local machine, much like
     |  we treat Gadgetron.
     |  
     |  Import:
     |      import Bartholomew as B
     |  Usage:
     |      B.[bart-func](args)
     |  Example:
     |      traj_rad = B.traj(x=512,y=64,r=True)
     |      ksp_sim = B.phantom(k=True,s=8,t=traj_rad)
     |      igrid = B.nufft(ksp_sim,i=True,t=traj_rad)
     |  
     |  Notice that input ndarrays are positional arguments (e.g., ksp_sim is the
     |  first argument for nufft instead of the last).
     |  
     |  To get comma separated lists (e.g., -d x:x:x), use the List type:
     |      img = B.nufft(ksp_sim,i=True,d=[24,24,1],t=traj_rad)
     |  
     |  To get space separated lists (e.g., resize [-c] dim1 size1 ... dimn), use
     |  Tuple type:
     |      ksp_zerop = B.resize(lowres_ksp,c=(0,308,1,308))
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

[Source](../master/mr_utils/bart/client.py)

```
NAME
    mr_utils.bart.client

FUNCTIONS
    client(num_out, cmd, files, host=None, username=None, password=None, root_dir=None)


```

