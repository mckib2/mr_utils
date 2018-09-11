import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=ImportWarning)
    from scipy.io import loadmat

def load_mat(filename,key=None):
    if key is None:
        return(loadmat(filename))
    else:
        return(loadmat(filename)[key])
