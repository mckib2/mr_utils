import socketserver
from subprocess import Popen,PIPE
from tempfile import NamedTemporaryFile
from mr_utils.load_data import load_mat
import logging
from mr_utils.config import ProfileConfig
from mr_utils.matlab.contract import done_token,RUN,GET,PUT
from functools import partial

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

class MATLAB(object):
    def __init__(self):

        # When we run a command we need to know when we're done...
        self.done_token = done_token

        # start instance of matlab of host
        cmd = 'matlab -nodesktop -nosplash'
        self.process = Popen(cmd.split(),stdin=PIPE,stdout=PIPE,bufsize=1,universal_newlines=True)
        self.process.stdin.write("fprintf('%s\\n')\n" % self.done_token)

        # Read out opening message
        self.catch_output()

    def run(self,cmd,log_func=None):
        '''Run MATLAB command in subprocess.'''

        self.process.stdin.write(('%s\n' % cmd))
        self.process.stdin.write("fprintf('%s\\n')\n" % self.done_token)
        logging.info(cmd)
        if log_func is not None:
            log_func(cmd)

        # Capture output if any from command.  There will at least be the
        # done_token to collect.
        self.catch_output(log_func=log_func)

    def catch_output(self,log_func=None):
        for l in self.process.stdout:
            if log_func is not None:
                log_func(l.rstrip())
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
        self.run(cmd)

        return(tmp_filename)

    def put(self,tmp_filename):
        '''Put variables from python into MATLAB workspace.

        tmp_filename -- MAT file holding variables to inject into workspace.
        '''

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

        # Incoming connection...
        logging.info('%s connected' % self.client_address[0])

        # See what they want to do
        self.what = self.rfile.readline().strip().decode()
        if self.what == RUN:

            # The command will be coming next
            self.cmd = self.rfile.readline().strip()
            # logging.info('cmd issued: %s' % self.cmd.decode())
            self.server.matlab.run(self.cmd.decode(),log_func=lambda x: self.wfile.write(x.encode()))

        elif self.what == GET:

            # Client will say what the bufsize is:
            bufsize = int(self.rfile.readline().strip().decode())
            logging.info('bufsize for %s is %d' % (GET,bufsize))

            # The list of varnames to get from the workspace will be next
            varnames = self.rfile.readline().strip().decode()
            tmp_filename = self.server.matlab.get(varnames.split())

            # Send binary file over socket
            with open(tmp_filename,'rb') as f:
                for chunk in iter(partial(f.read,bufsize),b''):
                    self.wfile.write(chunk)
            self.wfile.write(done_token.encode())

        elif self.what == PUT:

            # Client will say what the bufsize is:
            bufsize = int(self.rfile.readline().strip().decode())
            logging.info('bufsize for %s is %d' % (PUT,bufsize))

            # Get ready to recieve file
            tmp_filename = NamedTemporaryFile().name
            with open(tmp_filename,'wb') as f:
                done = False
                while not done:
                    received = self.rfile.read(bufsize)
                    if bytes(done_token,'utf-8') in received:
                        received = received[:-len(done_token)]
                        done = True
                    f.write(received)

            self.server.matlab.put(tmp_filename)

        else:
            msg = 'Not quite sure what you want me to do, %s is not a valid identifier.' % self.what
            self.wfile.write(msg.encode())
            logging.info(msg)

def start_server():
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
        logging.info('Just a sec, stopping matlab and freeing up ports...')
        matlab.exit()


if __name__ == '__main__':
    start_server()
