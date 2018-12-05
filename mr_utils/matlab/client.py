import socket
import logging
from mr_utils.config import ProfileConfig
from mr_utils.matlab.contract import done_token,RUN,GET,PUT
from mr_utils.load_data import load_mat
from tempfile import NamedTemporaryFile
from functools import partial
from scipy.io import savemat

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def get_socket(host,port,bufsize):
    # Find host,port from profiles.config
    profile = ProfileConfig()
    if host is None:
        host = profile.get_config_val('matlab.host')
    if port is None:
        port = profile.get_config_val('matlab.port')
    if bufsize is None:
        bufsize = profile.get_config_val('matlab.bufsize')

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return(sock,host,port,bufsize)

def client_run(cmd,host=None,port=None,bufsize=None):
    '''Run command on MATLAB server.

    cmd -- MATLAB command.
    host -- host/ip-address of server running MATLAB.
    port -- port of host to connect to.
    bufsize -- Number of bytes to transmit/recieve at a time.
    '''

    sock,host,port,bufsize = get_socket(host,port,bufsize)

    # Connect to server and send data
    received_all = b''
    try:
        sock.connect((host,port))
        sock.sendall(('%s\n' % RUN).encode())
        sock.sendall((cmd + '\n').encode())

        # Receive data from the server and shut down
        while True:
            received = sock.recv(1024)
            received_all += b'\n' + received
            if done_token in received.decode():
                # Remove done token from received_all
                received_all = received_all[:-len(done_token)]
                break
    finally:
        sock.close()

    logging.info(received_all.decode())

def client_get(varnames,host=None,port=None,bufsize=None):
    '''Get variables from remote MATLAB workspace into python as numpy arrays.

    varnames -- List of names of variables in MATLAB workspace to get.
    host -- host/ip-address of server running MATLAB.
    port -- port of host to connect to.
    bufsize -- Number of bytes to transmit/recieve at a time.

    Notice that varnames should be a list of strings.
    '''

    if type(varnames) is not list:
        try:
            varnames = list(varnames)
        except:
            raise ValueError('varnames should be a list of variable names!')

    sock,host,port,bufsize = get_socket(host,port,bufsize)

    # Connect to server and send data
    try:
        sock.connect((host,port))
        sock.sendall(('%s\n' % GET).encode()) # tell host what we want to do
        sock.sendall(('%d\n' % bufsize).encode()) # tell host bufsize

        # make varnames a space separated list, then send
        sock.sendall((' '.join(varnames) + '\n').encode())

        # Get ready to recieve file
        tmp_filename = NamedTemporaryFile().name
        with open(tmp_filename,'wb') as f:
            done = False
            while not done:
                received = sock.recv(bufsize)
                if bytes(done_token,'utf-8') in received:
                    received = received[:-len(done_token)]
                    done = True
                f.write(received)

        # Now load transfered MAT file into memory
        try:
            data = load_mat(tmp_filename)
            vals = { key: data[key] for key in varnames }
        except:
            raise ValueError('Was not able to read MATLAB workspace variables.')

    finally:
        sock.close()

    logging.info('Received variables!')
    return(vals)

def client_put(vars,host=None,port=None,bufsize=None):
    '''Put variables from python into MATLAB workspace.

    vars -- Python variables to be injected into MATLAB workspace.
    bufsize -- Number of bytes to transmit/recieve at a time.

    Notice that vars should be a dictionary: keys are the desired names of
    the variables in the MATLAB workspace and values are the python
    variables.
    '''

    if type(vars) is not dict:
        raise ValueError('vars should be a dictionary of python variables!')

    sock,host,port,bufsize = get_socket(host,port,bufsize)

    # Connect to server and send data
    try:
        sock.connect((host,port))
        sock.sendall(('%s\n' % PUT).encode()) # tell host what we want to do
        sock.sendall(('%d\n' % bufsize).encode()) # tell host bufsize

        # Write the variables to mat file
        tmp_filename = NamedTemporaryFile(suffix='.mat').name
        savemat(tmp_filename,vars)

        # Send binary file over socket
        with open(tmp_filename,'rb') as f:
            for chunk in iter(partial(f.read,bufsize),b''):
                sock.send(chunk)
        sock.send(done_token.encode())

    finally:
        sock.close()

    logging.info('Transfered variables!')
