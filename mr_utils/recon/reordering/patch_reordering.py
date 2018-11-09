import numpy as np
import matplotlib.pyplot as plt
import warnings # We know skimage will complain about importing imp...
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

def get_patches(imspace,patch_size):
    patches = view_as_windows(np.ascontiguousarray(imspace),patch_size)
    return(patches)

if __name__ == '__main__':
    pass
