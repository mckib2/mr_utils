'''Gadgetron client for running on network machines.

Adapted from https://github.com/gadgetron/gadgetron-python-ismrmrd-client.git
Keeps same command line interface, but allows for import into scripts.
'''

import pathlib
import argparse
import datetime
from tempfile import NamedTemporaryFile
import socket
import logging
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import ismrmrd
    import h5py

from tqdm import trange

from mr_utils.load_data import load_raw
from . import gtconnector as gt

def client(
        data,
        address=None,
        port=None,
        outfile=None,
        in_group='/dataset',
        out_group=None,
        config='default.xml',
        config_local=None,
        script=None,
        existing_modules=['numpy', 'scipy', 'h5py'],
        script_dir=None,
        verbose=False):
    '''Send acquisitions to Gadgetron.

    This client allows you to connect to a Gadgetron server and process data.

    Parameters
    ==========
    data : str or array_like
        Input file with file extension or numpy array.
    address : str, optional
        Hostname of Gadgetron. If not set, taken from profile config.
    port : int, optional
        Port to connect to. If not set, taken from profile config.
    outfile : str, optional
        If provided, output will be saved to file with this name.
    in_group : str, optional
        If input is hdf5, input data group name.
    out_group : str, optional
        Output group name if file is written.
    config : xml_str, optional
        Remote configuration file.
    config_local : xml_str, optional
        Local configuration file.
    script : str, optional
        File path to the Python script to be bundled and transfered.
    existing_modules : list, optional
        Python packages to exclude from bundling.
    script_dir : str, optional
        Directory to send script on remote machine.
    verbose : bool, optional
        Verbose mode.

    Returns
    =======
    data : array_like
        Image from Gadgetron
    header : xml
        Header from Gadgetron

    Raises
    ======
    NotImplementedError
        `script` bundling is not currently implemented.
    Exception
        `data` is not provided in the correct format.

    Notes
    =====
    out_group=None will use the current date as the group name.
    '''

    # Make sure we have an out_group label
    if out_group is None:
        out_group = str(datetime.datetime.now())

    # If user wanted to be verbose, let's give them verbose, otherwise just
    # tell them about warnings
    if verbose:
        logging.basicConfig(format='%(levelname)s: %(message)s',
                            level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s',
                            level=logging.WARNING)

    # First thing's first, we need to send the python script over!
    if script is not None:
        raise NotImplementedError()
        # from mr_utils.utils import package_script
        # package_script(script, existing_modules=existing_modules)

    # The magic happens in the connector
    logging.debug('Instantiating Connector')
    con = gt.Connector()

    ## Register all the readers we need:
    # The readers need to know where to output the data that gadgetron sends
    # back.  The output is an hdf5 file, but if we don't want that file and
    # only care about the numpy array, then we'll create a temporary file to
    # store the output in and then kill it when we're done.
    if outfile is None:
        outfile = NamedTemporaryFile().name
    logging.debug('Writing to filename: %s', outfile)

    # Image message readers
    for im_id in [
            gt.GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_USHORT,
            gt.GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_FLOAT,
            gt.GADGET_MESSAGE_ISMRMRD_IMAGE_CPLX_FLOAT,
            gt.GADGET_MESSAGE_ISMRMRD_IMAGE]:
        con.register_reader(im_id, gt.ImageMessageReader(outfile, out_group))

    # Images with attributes
    for im_id in [
            gt.GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_USHORT,
            gt.GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_FLOAT,
            gt.GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_CPLX_FLOAT]:
        con.register_reader(
            im_id, gt.ImageAttribMessageReader(outfile, out_group))

    # DICOM
    con.register_reader(
        gt.GADGET_MESSAGE_DICOM, gt.BlobMessageReader(out_group, 'dcm'))
    con.register_reader(gt.GADGET_MESSAGE_DICOM_WITHNAME,
                        gt.BlobAttribMessageReader('', 'dcm'))

    # Connect to Gadgetron - if no host, port were supplied then look at the
    # active profile to get the values
    if (address is None) or (port is None):
        from mr_utils.config import ProfileConfig
        profile = ProfileConfig()
        if address is None:
            address = profile.get_config_val('gadgetron.host')
        if port is None:
            port = profile.get_config_val('gadgetron.port')

    logging.debug('Connecting to Gadgetron @ %s:%d', address, port)
    con.connect(address, port)

    # Find the configuration file we need
    if config_local:
        logging.debug('Sending gadgetron configuration script...')
        con.send_gadgetron_configuration_script(config_local)
    else:
        logging.debug('Sending gadgetron configuration filename %s', config)
        con.send_gadgetron_configuration_file(config)


    # Decide what the input was
    if isinstance(data, ismrmrd.Dataset):
        # User has already given us the ismrmrd dataset that gadgetron expects
        dset = data

    ## I would like to figure out a way to pass in a numpy array with header!

    # If we've given a filename:
    elif isinstance(data, str):
        # Find the file extension
        ext = pathlib.Path(data).suffix

        if ext == '.h5':
            # Load the dataset from hdf5 file
            dset = ismrmrd.Dataset(data, in_group, False)
        elif ext == '.dat':
            # Load the dataset from raw
            dset = load_raw(data, use='s2i', as_ismrmrd=True)

    else:
        raise Exception('data was not ismrmrd.Dataset or raw data!')

    if not dset:
        parser.error('Not a valid dataset: %s' % data)

    # Strip the dataset header and send to gadgetron
    xml_config = dset.read_xml_header()
    con.send_gadgetron_parameters(xml_config)

    # Next, send each acquisition to gadgetron
    for idx in trange(dset.number_of_acquisitions(), desc='Send', leave=False):
        acq = dset.read_acquisition(idx)
        try:
            con.send_ismrmrd_acquisition(acq)
        except socket.error as msg:
            logging.error('Failed to send acquisition %d', idx)
            print(msg)
            return None

    logging.debug('Sending close message to Gadgetron')
    con.send_gadgetron_close()
    con.wait()

    # Convert the hdf5 file into something we can use and send it back
    with h5py.File(outfile, 'r') as f:
        # Group might not be image_0
        data = f[out_group][list(f[out_group].keys())[0]]['data'][:]
        header = f[out_group][list(f[out_group].keys())[0]]['header'][:]
        # data = f[out_group]['image_0']['data'][:]
        # header = f[out_group]['image_0']['header'][:]
    return(data, header)

if __name__ == '__main__':

    # Command line interface
    parser = argparse.ArgumentParser(
        description='send acquisitions to Gadgetron',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data', help='Input file')
    parser.add_argument('-a', '--address',
                        help='Address (hostname) of Gadgetron Host')
    parser.add_argument('-p', '--port', type=int, help='Port')
    parser.add_argument('-o', '--outfile', help='Output file')
    parser.add_argument('-g', '--in-group', help='Input data group')
    parser.add_argument('-G', '--out-group', help='Output group name')
    parser.add_argument('-c', '--config', help='Remote configuration file')
    parser.add_argument('-C', '--config-local',
                        help='Local configuration file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose mode')

    parser.set_defaults(
        address='localhost',
        port='9002',
        outfile='out.h5',
        in_group='/dataset',
        out_group=str(datetime.datetime.now()),
        config='default.xml')

    args = parser.parse_args()

    client(**args)
