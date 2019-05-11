
import numpy as np

def sort_real_imag_parts(data, axis=0):
    '''To determine temporal sort order for real and imag components.
    '''

    return(np.argsort(data.real, axis), np.argsort(data.imag, axis))
