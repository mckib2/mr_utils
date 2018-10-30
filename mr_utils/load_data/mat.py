import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=ImportWarning)
    from scipy.io import loadmat

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
                    data[k] = np.array(v)
                return(data)
            else:
                return(np.array(f[key]))
