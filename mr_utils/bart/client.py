'''Connect to BART over a network.

I do not believe this is working currently!

Uses paramiko to connect to a network machine (could be your own machine),
opens an instance of BART and returns the result.
'''

import paramiko

from mr_utils.config import ProfileConfig

def client(
        num_out,
        cmd,
        files,
        host=None,
        username=None,
        password=None,
        root_dir=None):
    '''BART client.

    Parameters
    ==========

    num_out : int
        Number of expected variables returned.
    cmd : str
        BART command to be run.
    files : list
        Any files to be provided to BART.
    host : str, optional
        IP address of machine we want to connect to.
    username : str, optional
        username to sign in with.
    password : str, optional
        password to use for sign in (will be plain-text!)
    root_dir : str, optional
        Root directory to run BART out of.
    '''

    # Grab credentials
    profile = ProfileConfig()
    if host is None:
        host = profile.get_config_val('bart.host')
    if username is None:
        username = profile.get_config_val('bart.user')
    if password is None:
        password = profile.get_config_val('bart.password')
    if root_dir is None:
        root_dir = profile.get_config_val('bart.root_dir')

    # Connect to host
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)

    # Send the command
    stdin, stdout, stderr = ssh_client.exec_command((
        "python3 -c 'import sys; sys.path.insert(0,\"%s/python\");"
        "from bart import bart; import numpy as np;"
        "print(bart)' " % (root_dir)))
    print(stdout.readlines())
    ssh_client.close()

if __name__ == '__main__':

    client(1, 'traj -x 512 -y 64', None)
