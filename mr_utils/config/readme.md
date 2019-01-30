
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

