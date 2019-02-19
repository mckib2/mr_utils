'''Simple root sum of squares image combination.'''

import numpy as np

def sos(im, axes=0):
    '''Root sum of squares combination along given axes.

    im -- Input image.
    axes -- Dimensions to sum across.
    '''
    return np.sqrt(np.sum(np.abs(im)**2, axis=axes))

if __name__ == '__main__':
    pass
