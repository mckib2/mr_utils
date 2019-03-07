
# GADGETRON
## examples.gadgetron.bssfp_grappa

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/gadgetron/bssfp_grappa.py)

```
NAME
    examples.gadgetron.bssfp_grappa - Simple example demonstrating how to send data to gadgetron.

DESCRIPTION
    We will use the gadgetron client and assume a profiles.config file is already
    created and located in the root directory as described in readme.  Gadgetron
    should be running on a network machine with IP address and port listed in
    profiles.config.
    
    We will load in example undersampled (R=2) bSSFP data and send it to
    Gadgetron to reconstruct using GRAPPA.


```


## examples.gadgetron.example_config

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/gadgetron/example_config.py)

```
NAME
    examples.gadgetron.example_config - Example of how to programmatically generate a config file.


```


## examples.gadgetron.gs_recon_gadget

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/gadgetron/gs_recon_gadget.py)

```
NAME
    examples.gadgetron.gs_recon_gadget - Make a Gadgetron chain that includes a python gadget.


```


## examples.gadgetron.python_gadgets

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/gadgetron/python_gadgets.py)

```
NAME
    examples.gadgetron.python_gadgets - Send data to Gadgetron to be processed using python Gadgets.


```


## examples.gadgetron.send_python_script_to_remote

[Source](https://github.com/mckib2/mr_utils/blob/master/examples/gadgetron/send_python_script_to_remote.py)

```
NAME
    examples.gadgetron.send_python_script_to_remote - Remote Gadgetron execution of custom Python Gadget.

DESCRIPTION
    Example demonstrating how to use the Gadgetron client to send a python Gadget
    to the remote Gadgetron server and use it in a Gadget chain.
    
    The idea is to "bundle" all of the dependencies of the script together so
    that there is no extra setup/installation step before the remote machine is
    able to run the custom python Gadget.

```

