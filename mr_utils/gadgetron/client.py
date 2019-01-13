#!/usr/bin/env python

## Adapted from https://github.com/gadgetron/gadgetron-python-ismrmrd-client.git
# Keeps same command line interface, but allows for import into scripts.

from . import gtconnector as gt
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import ismrmrd
    import h5py
from mr_utils.load_data import load_raw
import pathlib
import argparse
import datetime
from tempfile import NamedTemporaryFile
import logging
logger = logging.getLogger(__name__)

def client(
    data,
    address=None,
    port=None,
    outfile=None,
    in_group='/dataset',
    out_group=None,
    config='default.xml',
    config_local=None,
    loops=1,
    verbose=False):
    '''Send acquisitions to Gadgetron.

    This client allows you to connect to a Gadgetron server and process data.

    data -- Input file with file extension or numpy array.
    address -- Hostname of Gadgetron. If not set, taken from profile config.
    port -- Port to connect to. If not set, taken from profile config.
    outfile -- If provided, output will be saved to file with this name.
    in_group -- If input is hdf5, input data group name.
    out_group -- Output group name if file is written.
    config -- Remote configuration file.
    config_local -- Local configuration file.
    loops -- Number of loops.
    verbose -- Verbose mode.

    out_group=None will use the current date as the group name.
    '''

    # Make sure we have an out_group label
    if out_group is None:
        out_group = str(datetime.datetime.now())

    # Initialize logging
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)

    # If user wanted to be verbose, let's give them verbose, otherwise just
    # tell them about warnings
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    # The magic happens in the connector
    logger.debug('Instantiating Connector')
    con = gt.Connector()

    ## Register all the readers we need:
    # The readers need to know where to output the data that gadgetron sends
    # back.  The output is an hdf5 file, but if we don't want that file and
    # only care about the numpy array, then we'll create a temporary file to
    # store the output in and then kill it when we're done.
    if outfile is None:
        outfile = NamedTemporaryFile().name
    logger.debug('Writing to filename: %s' % outfile)

    # Image message readers
    for id in [ gt.GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_USHORT,gt.GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_FLOAT,gt.GADGET_MESSAGE_ISMRMRD_IMAGE_CPLX_FLOAT,gt.GADGET_MESSAGE_ISMRMRD_IMAGE ]:
        con.register_reader(id,gt.ImageMessageReader(outfile,out_group))
    # Images with attributes
    for id in [ gt.GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_USHORT,gt.GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_FLOAT,gt.GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_CPLX_FLOAT ]:
        con.register_reader(id,gt.ImageAttribMessageReader(outfile,out_group))
    # DICOM
    con.register_reader(gt.GADGET_MESSAGE_DICOM,gt.BlobMessageReader(out_group,'dcm'))
    con.register_reader(gt.GADGET_MESSAGE_DICOM_WITHNAME,gt.BlobAttribMessageReader('','dcm'))

    # Connect to Gadgetron - if no host, port were supplied then look at the
    # active profile to get the values
    if (address is None) or (port is None):
        from mr_utils.config import ProfileConfig
        profile = ProfileConfig()
        if address is None:
            address = profile.get_config_val('gadgetron.host')
        if port is None:
            port = profile.get_config_val('gadgetron.port')

    logger.debug('Connecting to Gadgetron @ %s:%d' % (address,port))
    con.connect(address,port)

    # Find the configuration file we need
    if config_local:
        logger.debug('Sending gadgetron configuration script %s' % config_local)
        con.send_gadgetron_configuration_script(config_local)
    else:
        logger.debug('Sending gadgetron configuration filename %s' % config)
        con.send_gadgetron_configuration_file(config)


    # Decide what the input was
    if type(data) is ismrmrd.Dataset:
        # User has already given us the ismrmrd dataset that gadgetron expects
        dset = data

    ## I would like to figure out a way to pass in a numpy array with header!

    # If we've given a filename:
    elif type(data) is str:
        # Find the file extension
        ext = pathlib.Path(data).suffix

        if ext == '.h5':
            # Load the dataset from hdf5 file
            dset = ismrmrd.Dataset(data,in_group,False)
        elif ext == '.dat':
            # Load the dataset from raw
            dset = load_raw(data,use='s2i',as_ismrmrd=True)

    else:
        raise Exception('data was not ismrmrd.Dataset or raw data!')

    if not dset:
        parser.error('Not a valid dataset: %s' % data)

    # Strip the dataset header and send to gadgetron
    xml_config = dset.read_xml_header()
    con.send_gadgetron_parameters(xml_config)

    # Next, send each acquisition to gadgetron
    for idx in range(dset.number_of_acquisitions()):
        logger.debug('Sending acquisition %d' % idx)
        acq = dset.read_acquisition(idx)
        try:
            con.send_ismrmrd_acquisition(acq)
        except:
            logger.error('Failed to send acquisition %d' % idx)
            return


    logger.debug('Sending close message to Gadgetron')
    con.send_gadgetron_close()
    con.wait()

    # Convert the hdf5 file into something we can use and send it back
    with h5py.File(outfile,'r') as f:
        data = f[out_group]['image_0']['data'][:]
        header = f[out_group]['image_0']['header'][:]
    return(data,header)

if __name__ == '__main__':

    # Command line interface
    parser = argparse.ArgumentParser(description='send acquisitions to Gadgetron',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data', help='Input file')
    parser.add_argument('-a', '--address', help='Address (hostname) of Gadgetron Host')
    parser.add_argument('-p', '--port', type=int, help='Port')
    parser.add_argument('-o', '--outfile', help='Output file')
    parser.add_argument('-g', '--in-group', help='Input data group')
    parser.add_argument('-G', '--out-group', help='Output group name')
    parser.add_argument('-c', '--config', help='Remote configuration file')
    parser.add_argument('-C', '--config-local', help='Local configuration file')
    parser.add_argument('-l', '--loops', type=int, help='Loops')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    parser.set_defaults(address='localhost', port='9002', outfile='out.h5',
            in_group='/dataset', out_group=str(datetime.datetime.now()),
            config='default.xml', loops=1)

    args = parser.parse_args()

    client(**args)
