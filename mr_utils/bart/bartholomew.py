from mr_utils.definitions import BART_PATH
from mr_utils.bart import real_bart
import subprocess,inspect,dis
import numpy as np

class BartholomewObject(object):
    '''More friendly python interface for BART.

    I also want this to be able to run BART on remote computer through ssh, to
    remove BART as a strict dependency for the local machine, much like
    we treat Gadgetron.
    '''

    def __init__(self):
        if BART_PATH is None:
            raise SystemError("BART's TOOLBOX_PATH environment variable not found!")

        # Make a list of  supported bart functions
        result = subprocess.run(['bart'],stdout=subprocess.PIPE)
        self.commands = result.stdout.decode().replace('BART. Available commands are:','').split()

    def __getattr__(self,name,*args,**kwargs):
        def function(*args,**kwargs):

            # Make sure function user asked for is a BART function
            if name not in self.commands:
                raise AttributeError('"%s" is not a valid BART function!' % name)

            # Deal with positional arguments
            formatted_pos_args,pos_files = self.format_args(args)

            # Put the named arguments into what bart expects them to look like
            formatted_named_args,file_opts,files = self.format_kwargs(kwargs)

            # Now we need to do some strange things to figure out how many
            # outputs the user expected...  This is kind of hacky, but it's
            # what the official python interface to BART wants, so I guess
            # we'll play along...
            num_outputs = self.get_num_outputs()

            # Now call the bart python interface
            cmd = '%s %s %s' % (name,' '.join(formatted_pos_args + formatted_named_args),' '.join(file_opts))
            return(real_bart(num_outputs,cmd,*(files + pos_files)))

        return(function)

    def get_num_outputs(self):
        '''Return how many values the caller is expecting'''

        f = inspect.currentframe()
        f = f.f_back.f_back
        c = f.f_code
        i = f.f_lasti
        bytecode = c.co_code
        instruction = bytecode[i+3]
        if instruction == dis.opmap['UNPACK_SEQUENCE']:
            howmany = bytecode[i+4]
            return(howmany)
        elif instruction == dis.opmap['POP_TOP']:
            return(0)
        return(1)

    def format_args(self,args):
        '''Take in positional function arguments and format for command-line.'''

        formatted_pos_args = []
        pos_files = []
        for a in args:
            if type(a) in [ int,float ]:
                formatted_pos_args.append(str(a))
            elif type(a) is np.ndarray:
                pos_files.append(a)
            else:
                raise NotImplementedError()
        return(formatted_pos_args,pos_files)

    def format_kwargs(self,kwargs):
        '''Take in named function arguments and format for command-line.'''

        args = []
        file_opts = []
        files = []
        for k in kwargs:
            if type(kwargs[k]) is bool:
                if kwargs[k]:
                    args.append('-%s' % k)

            elif type(kwargs[k]) in [ int,float,str ]:
                # option then value
                # Note that 3 must be changed to n3D, since variables can't
                # start with numbers...
                if k == 'n3d':
                    key = '3'
                else:
                    key = k
                args.append('-%s %s' % (key,kwargs[k]))

            elif type(kwargs[k]) is list:
                # colon separated list of numbers after option
                args.append('-%s %s' % (k,':'.join([ str(el) for el in kwargs[k] ])))

            elif type(kwargs[k]) is np.ndarray:
                # This needs to be packed onto the end as a file
                file_opts.append('-%s' % k)
                files.append(kwargs[k])

        return(args,file_opts,files)

# Give an instance for the user to import, treat almost like a namespace
Bartholomew = BartholomewObject()
