import numpy as np
from subprocess import Popen,PIPE
import logging

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

class Client():
    '''Open MATLAB subprocess to run commands and view output.

    Currently only works with MATLAB installations installed on the same
    computer the client is launched from.
    '''

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
        self.process.stdin.write(('%s\n' % cmd))
        self.process.stdin.write("fprintf('%s\\n')\n" % self.done_token)

        # Capture output if any from command
        self.catch_output()

    def catch_output(self):
        for l in self.process.stdout:
            if self.done_token in l.rstrip():
                break
            logging.info(l.rstrip())

    def transfer(self,varname):
        '''Get variable from MATLAB workspace into python as numpy array.

        varname -- Name of variable in MATLAB workspace to be transfered.

        The idea is to create a temporary file to transfer data between
        MATLAB and python environments.  In this case, the tmp file is an hdf5
        file that can be read into python using h5py.
        '''
        pass

    def exit(self):
        out,err = self.process.communicate('exit\n')

        exit_message = 'MATLAB finished with return code %d' % self.process.returncode
        if self.process.returncode == 0:
            logging.info(exit_message)
        else:
            logging.error(exit_message)

if __name__ == '__main__':
    pass
