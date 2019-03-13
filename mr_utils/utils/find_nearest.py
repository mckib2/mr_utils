'''Finding closest values in an array.'''

import numpy as np

def find_nearest(array, value):
    '''Given straws and needle, find the closest straw to the needle.

    Parameters
    ==========
    array : array_like
        hay stack.
    value : float
        needle.

    Returns
    =======
    idx : int
        Flattened index where value is located (or closest value is located).
    float
        The actual value at idx.
    '''
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return(idx, array[np.unravel_index(idx, array.shape)])
