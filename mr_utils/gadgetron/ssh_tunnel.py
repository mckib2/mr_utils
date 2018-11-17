## Let's make an ssh tunnel if we find it in profiles.config
from mr_utils.config import ProfileConfig
from paramiko.transport import Transport
import socket

if __name__ == '__main__':
    profile = ProfileConfig()
    ssh_host = profile.get_config_val('ssh.host')
    ssh_user = profile.get_config_val('ssh.user')
    host = profile.get_config_val('gadgetron.host')
    port = profile.get_config_val('gadgetron.port')

    print(ssh_host,ssh_user)

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ssh_host,22))
    transport = Transport(sock)
    transport.connect(username=ssh_user, password=None)
    chan = transport.open_channel('session',dest_addr=(host,port))
    print(chan)
    chan.close()
    transport.close()
    sock.close()
