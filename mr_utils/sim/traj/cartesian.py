import numpy as np

def cartesian(shape,undersample=.5,reflines=20):

    M,N = shape[:]
    k = int(undersample*M)
    idx = np.random.permutation(M)[:k]

    mask = np.zeros(shape)*False
    mask[idx,:] = True

    # Make sure we grab center of kspace regardless
    mask[int(M/2-reflines/2):int(M/2+reflines/2),:] = True

    return(mask)
