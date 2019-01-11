
# MATLAB
## mr_utils.matlab.client

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/matlab/client.py)

```
NAME
    mr_utils.matlab.client

FUNCTIONS
    client_get(varnames, host=None, port=None, bufsize=None)
        Get variables from remote MATLAB workspace into python as numpy arrays.
        
        varnames -- List of names of variables in MATLAB workspace to get.
        host -- host/ip-address of server running MATLAB.
        port -- port of host to connect to.
        bufsize -- Number of bytes to transmit/recieve at a time.
        
        Notice that varnames should be a list of strings.
    
    client_put(vars, host=None, port=None, bufsize=None)
        Put variables from python into MATLAB workspace.
        
        vars -- Python variables to be injected into MATLAB workspace.
        bufsize -- Number of bytes to transmit/recieve at a time.
        
        Notice that vars should be a dictionary: keys are the desired names of
        the variables in the MATLAB workspace and values are the python
        variables.
    
    client_run(cmd, host=None, port=None, bufsize=None)
        Run command on MATLAB server.
        
        cmd -- MATLAB command.
        host -- host/ip-address of server running MATLAB.
        port -- port of host to connect to.
        bufsize -- Number of bytes to transmit/recieve at a time.
    
    get_socket(host, port, bufsize)

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
    mr_utils.matlab.contract - # Define 'done token' for communication with MATLAB server

```


## mr_utils.matlab.server

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/matlab/server.py)

```
NAME
    mr_utils.matlab.server

CLASSES
    builtins.object
        MATLAB
    socketserver.StreamRequestHandler(socketserver.BaseRequestHandler)
        MyTCPHandler
    
    class MATLAB(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  catch_output(self, log_func=None)
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
     |  Define self.rfile and self.wfile for stream sockets.
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

```

