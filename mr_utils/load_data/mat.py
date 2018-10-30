import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=ImportWarning)
    from scipy.io import loadmat

def deal_with_7_3_complex(data):
    # Complex arrays will have a structured datatype...
    dt = data.dtype
    if 'imag' in dt.names:
        data = data['real'] + 1j*data['imag']
    return(data)

def load_mat(filename,key=None):
    try:
        if key is None:
            return(loadmat(filename))
        else:
            return(loadmat(filename)[key])
    except NotImplementedError:
        # So mat files v7.3 won't work with loadmat, so we use h5py
        print('Old mat file version detected...')

        import numpy as np
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=FutureWarning)
            import h5py

        with h5py.File(filename,'r') as f:
            if key is None:
                data = {}
                for k,v in f.items():
                    data[k] = deal_with_7_3_complex(np.array(v))
                return(data)
            else:
                return(deal_with_7_3_complex(np.array(f[key])))
