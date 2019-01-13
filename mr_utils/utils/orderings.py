import numpy as np

def col_stacked_order(x):
    '''Find ordering of monotonically varying flattened array, x.

    x -- Array to find ordering of.

    Note that you might want to provide abs(x) if x is a complex array.
    '''
    idx = np.argsort(x.flatten())
    return(idx)

def inverse_permutation(ordering):
    '''Given some permutation, find the inverse permutation.

    ordering -- Flattened indicies, such as output of np.argsort.
    '''
    inverse_ordering = [0]*len(ordering)
    for send_from,send_to in enumerate(ordering):
        inverse_ordering[send_to] = send_from
    return(inverse_ordering)
