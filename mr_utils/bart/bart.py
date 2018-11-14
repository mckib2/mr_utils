import sys
import numpy as np
from mr_utils.definitions import BART_PATH
if BART_PATH is not None:
    sys.path.insert(0,BART_PATH)
    from bart import bart as real_bart

def bart(*args):
    '''Wrapper that passes arguments to BART installation.'''

    if BART_PATH is not None:
        return(real_bart(*args))
    else:
        raise SystemError("BART's TOOLBOX_PATH environment variable not found!")


class Bartholomew(object):
    '''More friendly python interface for BART.'''

    def __init__(self):
        if BART_PATH is not None:
            raise SystemError("BART's TOOLBOX_PATH environment variable not found!")

    @staticmethod
    def format_args(kwargs):
        args = []
        file_opts = []
        files = []
        for k in kwargs:
            if type(kwargs[k]) is bool:
                if kwargs[k]:
                    args.append('-%s' % k)
            elif type(kwargs[k]) is int:
                # option then value
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

    @staticmethod
    def traj(x,y,**kwargs):
        '''Computes k-space trajectories

        x x        readout samples
        y y        phase encoding lines
        a a        acceleration
        t t        turns
        m mb       SMS multiband factor
        l          aligned partition angle
        g          golden angle in partition direction
        r          radial
        G          golden-ratio sampling
        D          double base angle
        q delays   gradient delays: x, y, xy
        Q delays   (gradient delays: z, xz, yz)
        O          correct transverse gradient error for radial tajectories
        n3D        3D

        Output:
        <output>
        '''
        args,_,_ = Bartholomew.format_args(kwargs)
        cmd = 'traj -x %d -y %d %s' % (x,y,' '.join(args))
        return(real_bart(1,cmd))


    @staticmethod
    def scale(factor,arr):
        '''Scale array by {factor}. The scale factor can be a complex number.
        '''
        return(real_bart(1,'scale %f' % factor,arr))

    @staticmethod
    def phantom(**kwargs):
        '''Image and k-space domain phantoms.

        s nc      	nc sensitivities
        S Output    nc sensitivities
        k           k-space
        t file      trajectory
        x n         dimensions in y and z
        n3D         3D
        '''
        args,file_opts,files = Bartholomew.format_args(kwargs)
        cmd = 'phantom %s' % (' '.join(args))

        # Stick files at end of argument list and pass files to real_bart
        cmd = '%s %s' % (cmd,' '.join(file_opts))
        return(real_bart(1,cmd,*files))
