
import numpy as np

def sort_real_imag_parts(data):
    '''To determine temporal sort order for real and imag components'''

    return(np.argsort(data.real, 0), np.argsort(data.imag, 0))
