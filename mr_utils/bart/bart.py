'''Simple interface to call BART's python object from mr_utils.

This will verify that BART's TOOLBOX_PATH is found, if not, an exception will
be raised.  Consider using Bartholomew, it's meant to be a better interface
to command-line BART.
'''

from mr_utils.definitions import BART_PATH

if BART_PATH is not None:
    import sys
    sys.path.insert(0, BART_PATH)
    from bart import bart as real_bart
else:
    real_bart = None

def bart(*args):
    '''Wrapper that passes arguments to BART installation.'''

    if BART_PATH is None:
        raise SystemError("BART's TOOLBOX_PATH env variable not found!")
    return real_bart(*args)
