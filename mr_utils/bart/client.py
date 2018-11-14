import paramiko
from mr_utils.config import ProfileConfig
from tempfile import NamedTemporaryFile

def client(num_out,cmd,files,host=None,username=None,password=None,root_dir=None):

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


    # print(cmd)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host,username=username,password=password)

    # tmp_files = []
    # for file in files:
    #     tmp_files.append(NamedTemporaryFile().name)

    # stdin,stdout,stderr = ssh_client.exec_command('%s/bart %s' % (root_dir,cmd))
    # print("python3 -c 'import sys; sys.path.insert(0,\"%s/python\"); from bart import bart; bart(%d,\"%s\")' " % (root_dir,num_out,cmd))
    stdin,stdout,stderr = ssh_client.exec_command("python3 -c 'import sys; sys.path.insert(0,\"%s/python\"); from bart import bart; import numpy as np; print(bart)' " % (root_dir))
    print(stdout.readlines())
    # print(stderr.readlines())
    ssh_client.close()

if __name__ == '__main__':

    client(1,'traj -x 512 -y 64',None)
