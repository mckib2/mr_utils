import socket
import logging
from mr_utils.config import ProfileConfig
from mr_utils.definitions import done_token
from mr_utils.load_data import load_mat
from tempfile import NamedTemporaryFile

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

def get_socket(host,port):
    # Find host,port from profiles.config
    profile = ProfileConfig()
    if host is None:
        host = profile.get_config_val('matlab.host')
    if port is None:
        port = profile.get_config_val('matlab.port')

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return(sock,host,port)

def client_run(cmd,host=None,port=None):
    '''Run command on MATLAB server.

    cmd -- MATLAB command.
    host -- host/ip-address of server running MATLAB.
    port -- port of host to connect to.
    '''

    sock,host,port = get_socket(host,port)

    # Connect to server and send data
    received_all = b''
    try:
        sock.connect((host,port))
        sock.sendall(b'RUN\n')
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

def client_get(varnames,host=None,port=None,bufsize=1024):
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

    sock,host,port = get_socket(host,port)

    # Connect to server and send data
    received_all = b''
    try:
        sock.connect((host,port))
        sock.sendall(b'GET\n') # tell host what we want to do
        sock.sendall(('%d\n' % bufsize).encode()) # tell host bufsize

        # make varnames a comma separated list, then send
        sock.sendall((','.join(varnames) + '\n').encode())

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
