
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
    client(data, address=None, port=None, outfile=None, in_group='/dataset', out_group=None, config='default.xml', config_local=None, verbose=False)
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
        verbose -- Verbose mode.
        
        out_group=None will use the current date as the group name.


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

