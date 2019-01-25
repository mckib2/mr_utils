import numpy as np

def col_stacked_order(x):
    '''Find ordering of monotonically varying flattened array, x.

    x -- Array to find ordering of.

    Note that you might want to provide abs(x) if x is a complex array.
    '''
    idx = np.argsort(x.flatten())
    return(idx)

def colwise(x):
    '''Find ordering of monotonically varying columns.

    x -- Array to find ordering of.
    '''
    indicies = np.arange(x.size).reshape(x.shape)
    idx = np.argsort(x,axis=0)
    for ii in range(x.shape[1]):
        indicies[:,ii] = indicies[:,ii][idx[:,ii]]
    return(indicies.flatten())

def rowwise(x):
    '''Find ordering of monotonically varying rows.

    x -- Array to find ordering of.
    '''
    indicies = np.arange(x.size).reshape(x.shape)
    idx = np.argsort(x,axis=1)
    for ii in range(x.shape[0]):
        indicies[ii,:] = indicies[ii,:][idx[ii,:]]
    return(indicies.flatten())

def inverse_permutation(ordering):
    '''Given some permutation, find the inverse permutation.

    ordering -- Flattened indicies, such as output of np.argsort.
    '''
    inverse_ordering = [0]*len(ordering)
    for send_from,send_to in enumerate(ordering):
        inverse_ordering[send_to] = send_from
    return(inverse_ordering)

if __name__ == '__main__':

    from mr_utils import view
    data = np.random.random((10,5))
    # idx = colwise(data)
    idx = rowwise(data)
    view(data.flatten()[idx].reshape(data.shape))

    ridx = inverse_permutation(idx)
    assert np.allclose(data.flatten()[idx][ridx],data.flatten())
