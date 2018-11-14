import sys
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
