import numpy as np
from scipy.ndimage.interpolation import rotate

def simple_csm(N,dims=(64,64)):
    '''Generate coil channel sensitivities as linear gradients in N directions.

    N -- number of coil sensitivities to generate.
    dims -- tuple of dimensions.

    N linear gradient gradients of size dims will be generated.  These are
    simple because all we're doing is generating linear gradients at evenly
    spaced angles so the resulting maps are square.

    TODO: sensitivity maps also need phases, as in:
    ismrmrdtools.simulation.generate_birdcage_sensitivities

    Returns (N x dims[0] x dims[1]) array.
    '''

    angles = np.linspace(0,360,N,endpoint=False)
    sens = np.zeros((N,dims[0],dims[1]))

    # We'll need to make it bigger so when we rotate we don't clip
    pad = int(np.max(dims)*np.sqrt(2))
    x = np.linspace(0,1,dims[0]+pad)
    y = np.linspace(0,1,dims[1]+pad)
    X,Y = np.meshgrid(x,y)
    for ii,angle in enumerate(angles):
        tmp = rotate(X,angle,reshape=False,mode='constant')
        sens[ii,:,:] = tmp[int(pad/2):dims[0]+int(pad/2),int(pad/2):dims[1]+int(pad/2)]
        sens[ii,:,:] /= np.max(sens[ii,:,:])
    return(sens)

if __name__ == '__main__':
    pass
