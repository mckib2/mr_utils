import numpy as np

def find_nearest(array,value):
    '''Given straws and needle, find the closest straw to the needle.

    array -- hay stack.
    value -- needle.
    '''
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return(idx,array[idx])
