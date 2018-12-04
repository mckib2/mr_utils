import socket
import sys
import logging
from mr_utils.config import ProfileConfig

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

# Find host,port from profiles.config
profile = ProfileConfig()
host = profile.get_config_val('matlab.host')
port = profile.get_config_val('matlab.port')

data = ' '.join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Connect to server and send data
try:
    sock.connect((host,port))
    sock.sendall((data + '\n').encode())

    # Receive data from the server and shut down
    received = sock.recv(1024).decode()
finally:
    sock.close()

logging.info('Sent:     {}'.format(data))
logging.info('Received: {}'.format(received))
