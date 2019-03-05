'''Load data from MATLAB file type.

Uses scipy.io.loadmat to load recent versions of .MAT files.  Version 7.3 is
supported.  It'll try to make some intelligent guesses if it runs into
trouble, meaning, 'it will die trying!'.  If you don't like that philosophy,
go ahead and use scipy.io.loadmat directly.
'''

import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=ImportWarning)
    from scipy.io import loadmat
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def deal_with_7_3(data):
    '''Clean up data structures for MATLAB 7.3.

    Version 7.3 has a structured datatype that needs to be translated as a
    complex number.
    '''

    # Complex arrays will have a structured datatype...
    dt = data.dtype
    try:
        if 'imag' in dt.names:
            data = data['real'] + 1j*data['imag']
    except:
        # Not complex, we're fine
        pass

    return data

def load_mat(filename, key=None):
    '''Load data from .MAT file.

    filename -- path to .mat file.
    key -- Specific key to extract.

    If key=None, all keys will be extracted.  If there is only one key, then
    its value will be provided directly, no dictionary will be returned.
    '''

    try:
        if key is None:
            return loadmat(filename)
        # else...
        return loadmat(filename)[key]

    except NotImplementedError:
        # MAT files v7.3 won't work with loadmat, so we use h5py
        logging.info('Old mat file version detected...')

        import numpy as np
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=FutureWarning)
            import h5py

        with h5py.File(filename, 'r') as f:
            if key is None:
                data = {}
                for k, v in f.items():
                    data[k] = deal_with_7_3(np.array(v))

                # If there's only one key, just grab that key's value
                if len(data) == 1:
                    data = list(data.values())[0]

                return data

            # else...
            return deal_with_7_3(np.array(f[key]))
