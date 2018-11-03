import numpy as np

def rmse(predictions,targets,noroot=False):
    '''Compute root mean square error between predictions and targets.'''

    # Deal with NaNs if we have 'em:
    predictions[np.isnan(predictions)] = 0
    targets[np.isnan(targets)] = 0

    val = np.mean(np.abs((predictions - targets)**2))
    if noroot:
        return(val)
    else:
        return(np.sqrt(val))
