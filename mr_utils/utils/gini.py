'''Compute Gini index.

References
----------
.. [1] https://github.com/oliviaguest/gini/blob/master/gini.py
'''

import numpy as np

def gini(array, eps=1e-8):
    '''Calculate the Gini coefficient of a numpy array.

    Notes
    -----
    based on bottom eq on [2]_.

    References
    ----------
    .. [2]_ http://www.statsdirect.com/help/
            default.htm#nonparametric_methods/gini.htm
    '''

    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)

    # Values cannot be 0:
    array += eps

    # Values must be sorted:
    array = np.sort(array)

    # Index per array element:
    index = np.arange(1, array.shape[0]+1)

    # Number of array elements:
    n = array.shape[0]

    # Gini coefficient:
    return (
        np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))
