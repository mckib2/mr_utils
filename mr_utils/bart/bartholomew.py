'''More friendly python interface for BART.

I also want this to be able to run BART on remote computer through ssh, to
remove BART as a strict dependency for the local machine, much like
we treat Gadgetron.

Import:
    import Bartholomew as B
Usage:
    B.[bart-func](args)
Example:
    traj_rad = B.traj(x=512,y=64,r=True)
    ksp_sim = B.phantom(k=True,s=8,t=traj_rad)
    igrid = B.nufft(ksp_sim,i=True,t=traj_rad)

Notice that input ndarrays are positional arguments (e.g., ksp_sim is the
first argument for nufft instead of the last).

To get comma separated lists (e.g., -d x:x:x), use the List type:
    img = B.nufft(ksp_sim,i=True,d=[24,24,1],t=traj_rad)

To get space separated lists (e.g., resize [-c] dim1 size1 ... dimn), use
Tuple type:
    ksp_zerop = B.resize(lowres_ksp,c=(0,308,1,308))
'''

import subprocess
import inspect

import numpy as np

from mr_utils.definitions import BART_PATH
from mr_utils.bart import real_bart

class BartholomewObject(object):
    '''Bartholomew object - more simple Python interface for BART.

    User is meant to import instance Bartholomew, e.g.,
        from mr_utils.bart import Bartholomew as B
    '''

    def __init__(self):
        if BART_PATH is None:
            print("BART's TOOLBOX_PATH environment variable not found!")

        # Make a list of  supported bart functions
        try:
            result = subprocess.run(['bart'], stdout=subprocess.PIPE)
            self.commands = result.stdout.decode().replace(
                'BART. Available commands are:', '').split()
        except FileNotFoundError:
            pass

    def __getattr__(self, name, *args, **kwargs):
        def function(*args, **kwargs):
            '''Pass arguments to the real_bart function.'''

            # Make sure function user asked for is a BART function
            if name not in self.commands:
                raise AttributeError(
                    '"%s" is not a valid BART function!' % name)

            # Deal with positional arguments
            formatted_pos_args, pos_files = self.format_args(args)

            # Put the named arguments into what bart expects them to look like
            formatted_named_args, file_opts, files = self.format_kwargs(kwargs)

            # Now we need to do some strange things to figure out how many
            # outputs the user expected...  This is kind of hacky, but it's
            # what the official python interface to BART wants, so I guess
            # we'll play along... This should really be changed...
            num_outputs = self.get_num_outputs()

            # Now call the bart python interface
            cmd = '%s %s %s' % (name, ' '.join(
                formatted_pos_args+formatted_named_args), ' '.join(file_opts))
            return real_bart(num_outputs, cmd, *(files + pos_files))

        return function

    def get_num_outputs(self):
        '''Return how many values the caller is expecting'''

        try:
            idx = inspect.stack()[2].code_context[0].split().index('=')
            howmany = len(
                inspect.stack()[2].code_context[0].split()[idx-1].split(','))
            return howmany
        except ValueError:
            # we didn't find an equal sign - guess 1
            return 1

    def format_args(self, args):
        '''Take in positional function arguments and format for command-line.
        '''

        formatted_pos_args = []
        pos_files = []
        for a in args:
            if isinstance(a, (int, float)):
                formatted_pos_args.append(str(a))
            elif isinstance(a, tuple):
                formatted_pos_args.append(' '.join([str(el) for el in a]))
            elif isinstance(a, np.ndarray):
                pos_files.append(a)
            else:
                raise NotImplementedError()
        return(formatted_pos_args, pos_files)

    def format_kwargs(self, kwargs):
        '''Take in named function arguments and format for command-line.'''

        args = []
        file_opts = []
        files = []
        for k in kwargs:
            if isinstance(kwargs[k], bool):
                if kwargs[k]:
                    args.append('-%s' % k)

            elif isinstance(kwargs[k], (int, float, str)):
                # option then value
                # Note that 3 must be changed to n3D, since variables can't
                # start with numbers...
                if k == 'n3d':
                    key = '3'
                else:
                    key = k
                args.append('-%s %s' % (key, kwargs[k]))

            elif isinstance(kwargs[k], list):
                # colon separated list of numbers after option
                args.append(
                    '-%s %s' % (k, ':'.join([str(el) for el in kwargs[k]])))

            elif isinstance(kwargs[k], tuple):
                # space separated list of numbers after the option
                args.append(
                    '-%s %s' % (k, ' '.join([str(el) for el in kwargs[k]])))

            elif isinstance(kwargs[k], np.ndarray):
                # This needs to be packed onto the end as a file
                file_opts.append('-%s' % k)
                files.append(kwargs[k])

        return(args, file_opts, files)

# Give an instance for the user to import, treat almost like a namespace
Bartholomew = BartholomewObject()
