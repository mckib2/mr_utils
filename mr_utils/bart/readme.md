
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

