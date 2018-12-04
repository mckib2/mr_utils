import socket
import logging
from mr_utils.config import ProfileConfig
from mr_utils.definitions import done_token

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

def client_get(varnames,host=None,port=None):
    '''Get variables from remote MATLAB workspace into python as numpy arrays.

    varnames -- List of names of variables in MATLAB workspace to get.
    host -- host/ip-address of server running MATLAB.
    port -- port of host to connect to.

    Notice that varnames should be a list of strings.
    '''

    sock,host,port = get_socket(host,port)

    # Connect to server and send data
    received_all = b''
    try:
        sock.connect((host,port))
        sock.sendall(b'PUT\n')
    finally:
        sock.close()

    logging.info(received_all.decode())
