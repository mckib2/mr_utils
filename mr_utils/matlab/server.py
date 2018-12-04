import socketserver
from subprocess import Popen,PIPE
from tempfile import NamedTemporaryFile
from mr_utils.load_data import load_mat
from scipy.io import savemat
import logging
from mr_utils.config import ProfileConfig

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

class MATLAB(object):
    def __init__(self):

        # When we run a command we need to know when we're done...
        self.done_token = '__mr_utils_done__'

        # start instance of matlab of host
        cmd = 'matlab -nodesktop -nosplash'
        self.process = Popen(cmd.split(),stdin=PIPE,stdout=PIPE,bufsize=1,universal_newlines=True)
        self.process.stdin.write("fprintf('%s\\n')\n" % self.done_token)

        # Read out opening message
        self.catch_output()

    def run(self,cmd):
        '''Run MATLAB command in subprocess.'''

        self.process.stdin.write(('%s\n' % cmd))
        self.process.stdin.write("fprintf('%s\\n')\n" % self.done_token)
        logging.info(cmd)

        # Capture output if any from command.  There will at least be the
        # done_token to collect.
        self.catch_output()

    def catch_output(self):
        for l in self.process.stdout:
            if self.done_token in l.rstrip():
                break
            logging.info(l.rstrip())

    def get(self,varnames):
        '''Get variables from MATLAB workspace into python as numpy arrays.

        varnames -- List of names of variables in MATLAB workspace to get.

        Notice that varnames should be a list of strings.
        '''

        if type(varnames) is not list:
            try:
                varnames = list(varnames)
            except:
                raise ValueError('varnames should be a list of variable names!')

        tmp_filename = NamedTemporaryFile(suffix='.mat').name
        cmd = "save('%s',%s)" % (tmp_filename,','.join([ "'%s'" % vname for vname in varnames ]))
        # logging.info(cmd)
        self.run(cmd)

        try:
            data = load_mat(tmp_filename)
        except:
            raise ValueError('Was not able to read MATLAB workspace variables.')

        vals = { key: data[key] for key in varnames }
        return(vals)

    def put(self,vars):
        '''Put variables from python into MATLAB workspace.

        vars -- Python variables to be injected into MATLAB workspace.

        Notice that vars should be a dictionary: keys are the desired names of
        the variables in the MATLAB workspace and values are the python
        variables.
        '''

        if type(vars) is not dict:
            raise ValueError('vars should be a dictionary of python variables!')

        tmp_filename = NamedTemporaryFile(suffix='.mat').name
        savemat(tmp_filename,vars)
        cmd = "load('%s','-mat')" % tmp_filename
        self.run(cmd)

    def exit(self):
        '''Send exit command to MATLAB.'''

        out,err = self.process.communicate('exit\n')

        exit_message = 'MATLAB finished with return code %d' % self.process.returncode
        if self.process.returncode == 0:
            logging.info(exit_message)
        else:
            logging.error(exit_message)

# Create the server, binding to localhost on port
class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        self.cmd = self.rfile.readline().strip()
        logging.info('%s connected' % self.client_address[0])
        logging.info('cmd issued: %s' % self.cmd.decode())

        self.server.matlab.run(self.cmd.decode())

        self.wfile.write(self.cmd.upper())



if __name__ == '__main__':

    # Find host,port from profiles.config
    profile = ProfileConfig()
    host = profile.get_config_val('matlab.host')
    port = profile.get_config_val('matlab.port')

    # Start an instance of MATLAB
    try:
        matlab = MATLAB()
        server = socketserver.TCPServer((host,port),MyTCPHandler)
        server.matlab = matlab

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        logging.info('Server running on %s:%d' % (host,port))
        logging.info('Interrupt the server with Ctrl-C')
        server.serve_forever()
    finally:
        matlab.exit()
