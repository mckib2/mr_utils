'''siemens_to_ismrmrd client.'''

import uuid
import os
import logging
from tempfile import NamedTemporaryFile
import warnings

import paramiko
from tqdm import tqdm
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=FutureWarning)
    import ismrmrd

from mr_utils.config import ProfileConfig

class TqdmWrap(tqdm):
    def viewBar(self, a, b):
        '''Monitor progress of sftp transfers'''
        self.total = int(b)
        # update pbar with increment
        self.update(int(a - self.n))

class FastTransport(paramiko.Transport):
    def __init__(self, sock):
        '''Increase window size in hopes to go faster...'''
        super(FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)


def s2i_client(
        filename,
        put_file=True,
        get_file=True,
        cleanup_raw=True,
        cleanup_processed=True,
        remote_dir='/tmp',
        host=None,
        port=22,
        username=None,
        ssh_key=None,
        password=None,
        debug_level=logging.INFO):
    '''Runs siemens_to_ismrmrd on a remote computer.

    Main idea: allow users to use siemens_to_ismrmrd even if they don't have
    it installed locally.  They will, however, require SSH access to computer
    that does have it installed.

    Client puts file on server using SFTP, runs siemens_to_ismrmrd over SSH,
    and gets the file back using SFTP.  Username, password, hostname, and port
    is retrieved from the active profile in profiles.config.  Default port is
    22.  If no password is found, the RSA SSH key will be used from either the
    specified directory in profiles.config or, if empty, use '~/.ssh/id_rsa'.

    Parameters
    ==========
    filename : str
        Raw data (.dat) file on the local machine (if put_file is True)
        or on the remote machine (if put_file is False).
    put_file : bool, optional
        Whether or not to copy the raw data file from local to remote.
    get_file : bool, optional
        Whether or not to copy the processed file from machine to local.
    cleanup_raw : bool, optional
        Whether or not to delete raw data on remote.
    cleanup_processed : bool, optional
        Whether or not to delete processed data on remote.
    remote_dir : str, optional
        Working directory on remote (default in /tmp).
    host : str, optional
        hostname of remote machine.
    port : int, optional
        Port of remote machine to connect to.
    username : str, optional
        Username to use for SSH/SFTP connections.
    ssh_key : str, optional
        RSA private key file to use for SSH/SFTP connections.
    password : str, optional
        Password to use fr SSH/SFTP connections (stored in plaintext).
    debug_level : logging_level, optional
        Level of verbosity; see python logging module.

    Returns
    =======
    dset : ismrmrd.Dataset
        Result of siemens_to_ismrmrd
    '''

    # Setup logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=debug_level)

    # Grab credentials
    profile = ProfileConfig()
    if host is None:
        host = profile.get_config_val('siemens_to_ismrmrd.host')
        logging.info('profiles.config: using hostname %s', host)
    if port is None:
        host = profile.get_config_val('siemens_to_ismrmrd.port')
        logging.info('profiles.config: using port %s', str(port))
    if username is None:
        username = profile.get_config_val('siemens_to_ismrmrd.user')
        logging.info('profiles.config: using username %s', username)
    if password is None:
        password = profile.get_config_val('siemens_to_ismrmrd.password')
        # If blank, assume no password
        if password == '':
            password = None
        else:
            logging.warning(
                'profiles.config: using password stored in plaintext!')
            logging.warning('Suggested to use RSA key for connections!')

        # So now look for the RSA key
        if ssh_key is None:
            ssh_key = profile.get_config_val('siemens_to_ismrmrd.ssh_key')
            if ssh_key == '':
                ssh_key = '%s/.ssh/id_rsa' % os.environ['HOME']
                logging.info('Using defaut RSA key %s', ssh_key)
            else:
                logging.info('profiles.config: using RSA key %s', ssh_key)

    try:
        ssh_conn = FastTransport((host, port))
        ssh_conn.use_compression(True)
        if ssh_key is not None:
            ssh_conn.connect(
                pkey=paramiko.RSAKey.from_private_key_file(ssh_key),
                username=username)
        else:
            ssh_conn.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(ssh_conn)

        if put_file:
            # Upload file to the server
            remote_filename = '%s/siemens_to_ismrmrd_%s' % (
                remote_dir, str(uuid.uuid4()))
            logging.info('Starting transfer of %s to %s:%s:%s...', filename,
                         host, str(port), remote_filename)
            with TqdmWrap(ascii=True, unit='b', unit_scale=True) as pbar:
                # this can be pretty slow
                sftp.put(filename, remote_filename, callback=pbar.viewBar)
        else:
            # No file to transfer, then the filename is the name of the file
            # we need in the working directory on the remote.
            remote_filename = '%s/%s' % (remote_dir, filename)
            logging.info(
                'Not transferring, looking for remote file %s:%s:%s', host,
                str(port), remote_filename)

        # Run siemens_to_ismrmrd on remote
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if ssh_key is not None:
            ssh_client.connect(hostname=host, port=port, username=username)
        else:
            ssh_client.connect(hostname=host, port=port, username=username,
                               password=password)
        logging.info('SSH client succesfully connected!')

        processed_filename = '%s_processed' % remote_filename
        cmd = 'siemens_to_ismrmrd -f %s -o %s' % (
            remote_filename, processed_filename)
        logging.info('Running \"%s\" on remote...', cmd)
        _stdin, stdout, stderr = ssh_client.exec_command(cmd)
        for line in stdout.read().decode().splitlines():
            logging.info(line)
        if stderr.readlines():
            logging.error(stderr.read().decode())

        # Copy the processed file
        if get_file:
            tmp_name = NamedTemporaryFile().name
            logging.info(
                'Transferring processed file back to local machine...')
            with TqdmWrap(ascii=True, unit='b', unit_scale=True) as pbar:
                sftp.get(processed_filename, tmp_name, callback=pbar.viewBar)
            dset = ismrmrd.Dataset(tmp_name, '/dataset', False)
        else:
            logging.info('Not transferring processed file back from remote')
            dset = None

        # Clean files from server
        if cleanup_raw:
            logging.info('Cleaning up raw data on remote')
            sftp.remove(remote_filename)
        if cleanup_processed:
            logging.info('Cleaning up processed data on remote')
            sftp.remove(processed_filename)

    finally:
        ssh_client.close()
        sftp.close()
        ssh_conn.close()

    return dset

if __name__ == '__main__':
    pass
