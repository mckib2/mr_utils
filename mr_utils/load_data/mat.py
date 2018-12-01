import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=ImportWarning)
    from scipy.io import loadmat

def deal_with_7_3(data):
    # Complex arrays will have a structured datatype...
    dt = data.dtype
    try:
        if 'imag' in dt.names:
            data = data['real'] + 1j*data['imag']
    except:
        # Not complex, we're fine
        pass

    return(data)

def load_mat(filename,key=None):
    try:
        if key is None:
            return(loadmat(filename))
        else:
            return(loadmat(filename)[key])
    except NotImplementedError:
        # MAT files v7.3 won't work with loadmat, so we use h5py
        print('Old mat file version detected...')

        import numpy as np
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=FutureWarning)
            import h5py

        with h5py.File(filename,'r') as f:
            if key is None:
                data = {}
                for k,v in f.items():
                    data[k] = deal_with_7_3(np.array(v))

                # If there's only one key, just grab that key's value
                if len(data) == 1:
                    data = list(data.values())[0]

                return(data)
            else:
                return(deal_with_7_3(np.array(f[key])))
