import numpy as np
import matplotlib.pyplot as plt


def cartesian_pe(shape,undersample=.5,reflines=20):

    assert 0 < undersample <= 1,'Undersampling factor must be in (0,1]!'

    M,N = shape[:]
    k = int(undersample*M)
    idx = np.random.permutation(M)[:k]

    mask = np.zeros(shape)*False
    mask[idx,:] = True

    # Make sure we grab center of kspace regardless
    mask[int(M/2-reflines/2):int(M/2+reflines/2),:] = True

    return(mask)

def cartesian_gaussian(shape,undersample=(.5,.5),reflines=20):

    assert 0 < undersample[0] <= 1 and 0 < undersample[1] <= 1,'Undersampling factor must be in (0,1]!'

    M,N = shape[:]
    km = int(undersample[0]*M)
    kn = int(undersample[1]*N)

    mask = np.zeros(N*M).astype(bool)
    idx = np.arange(mask.size)
    np.random.shuffle(idx)
    mask[idx[:km*kn]] = True
    mask = mask.reshape(shape)

    # Make sure we grab the reference lines in center of kspace
    mask[int(M/2-reflines/2):int(M/2+reflines/2),:] = True

    return(mask)
