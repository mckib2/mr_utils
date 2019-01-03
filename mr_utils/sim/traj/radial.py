import numpy as np
from skimage.morphology import skeletonize
from skimage.transform import rotate

def radial(shape,num_spokes,theta=None,skinny=True,extend=True):
    '''Create 2d binary radial sampling pattern.

    shape -- x,y dimensions of sampling pattern.
    num_spokes -- Number of spokes to simulate.
    theta -- Angle between spokes (rad).
    skinny -- Garuantee 1px spoke width.
    extend -- Extend spokes to the edge of array.

    If theta=None, use golden angle. If skinny=True, edges of spokes with large
    slope may be curved. If extend=False, spokes confined in a circle.
    '''

    # Decide if we want to go all the way to edge of the array or not
    if extend:
        mode = 'wrap'
    else:
        mode = 'constant'

    # Use golden angle if no angle given
    if theta is None:
        theta = np.pi*(3 - np.sqrt(5))

    # initialze binary sampling image
    idx = np.zeros(shape,dtype=bool)

    # Create prototype spoke that we'll rotate
    idx0 = np.zeros(idx.shape,dtype=bool)
    idx0[int(shape[0]/2),:] = 1

    # Create all the spokes
    for ii in range(num_spokes):
        # Rotate prototype spoke to desired angle
        idx1 = rotate(idx0,np.rad2deg(theta*ii),resize=False,mode=mode).astype(bool)

        # If we want the spokes to gave 1px width
        if skinny:
            idx1 = skeletonize(idx1)

        # Add spoke to sampling mask
        idx |= idx1

    return(idx)

def radial_golden_ratio_meshgrid(X,Y,num_spokes):
    '''Create 2d binary golden angle radial sampling pattern.

    X,Y -- Meshgrid.
    num_spokes -- Number of spokes to simulate.

    Issues:
        For steep slopes, the spokes don't make it all the way to the edge of
        the image and they curve (from the skeletonize)...

    '''

    from scipy.ndimage.morphology import binary_dilation

    N = X.shape[0]
    h = np.abs(X[0,1] - X[0,0])

    golden = np.pi*(3 - np.sqrt(5))
    samp = np.zeros((N,N))
    idx = np.zeros(samp.shape,dtype=bool)
    for ii in range(num_spokes):

        # Get spoke
        m = np.tan(golden*ii) # slope
        idx0 = np.isclose(Y,m*X,atol=h/2)

        # But we need to make sure everything is connected -- sometimes the
        # slope is too large and we get gaps in spoke
        if np.abs(m) > 1:
            idx0 = binary_dilation(idx0,iterations=6)
            idx0 = skeletonize(idx0)
            # idx0 = binary_erosion(idx0,iterations=1)

        # plt.title(np.tan(golden*ii))
        # plt.imshow(idx0)
        # plt.show()

        idx |= idx0

        # idx |= rot(golden*ii).dot(x == x)
        # idx |= (Y == X*np.tan(golden*ii))
        # plt.plot(x,np.tan(golden*ii)*x)

    samp[idx] = 1
    return(samp)

if __name__ == '__main__':
    pass
