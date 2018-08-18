import numpy as np
from scipy.linalg import logm,expm

def flatten_rays(kspace,traj):
    # This function compares the k-space data to the trajectory and flattens
    # 'rays' where 'rays' are the dimensions from position 2 to the end of the
    # trajectory

    # For example, let's say that the data was nReadout x nRay x nTime x nCoil.
    # This code should combine nRay and nTime to become all rays. Let's also
    # say that the trajectory has size nReadout x nRay x nTime

    # First check that k-space contains more info than the trajectory.  Since
    # this method is for multi-coil data, this should always be true.  kspace
    # should have 4 dimensions and traj should have 3
    assert(kspace.ndim - traj.ndim == 1)

    # Now figure out where the rays are and smash them
    nReadout = kspace.shape[0]
    nCoil = kspace.shape[-1]

    # Determine length of ray dimension
    rayIndices = range(1,traj.ndim) # (1,2)
    lengths = np.zeros(len(rayIndices))
    for ii in range(len(rayIndices)): # (0,1)
        lengths[ii] = kspace.shape[rayIndices[ii]]

    raySize = int(np.prod(lengths)) # nRay*nTime

    # Now reshape kspace according to the new raySize
    kspace = np.reshape(kspace,(nReadout,raySize,nCoil))

    # Now do the same for the trajectories
    traj = np.reshape(traj,(nReadout,raySize))

    return(kspace,traj)


def scgrog(kspace,traj,cartdims=None):
    '''Compute Self Calibrating GRAPPA Gx and Gy operators.
    '''

    if cartdims is None:
        cartdims = (kspace.shape[0],kspace.shape[0])

    # If kspace has more than 3 dimensions, flatten the rays
    if kspace.ndim > 3:
        kspace,traj = flatten_rays(kspace,traj);

    kxs = cartdims[0]*np.real(traj)
    kys = cartdims[1]*np.imag(traj)

    # Initialize nmMatrix and vMatrix, see docs for variable naming
    nReadouts,nRays,nCoils = kspace.shape[:]

    nmMatrix = np.zeros((2,nRays))
    vMatrix = np.zeros((nCoils,nCoils,nRays),dtype='complex')

    # Create nmMatrix and vMatrix, ray-by-ray
    for iRay in range(nRays):
        # Master Equation: targetData = gRay*sourceData
        #
        # Since we're grabbing just 1 ray from our 3D slice, targetData becomes
        # a (nReadouts-1)x1xnCoils thing. But what we need is for targetData
        # and sourceData to be nCoilsx(nReadouts-1), so squeeze and transpose
        target = kspace[1::,iRay,:].squeeze().T
        source = kspace[0:-1:,iRay,:].squeeze().T

        # Now solve targetData = gRay*sourceData where gRay is an nCoils x
        # nCoils grappa-like coefficients matrix for that ray (we'll combine
        # all of the Gs from all rays later)
        gRay = target.dot(np.linalg.pinv(source))

        # Step 1: figure out n,m for this ray
        nRay = kxs[np.round(nReadouts/2).astype(int),iRay] - kxs[np.round(nReadouts/2).astype(int)-1,iRay]
        mRay = kys[np.round(nReadouts/2).astype(int),iRay] - kys[np.round(nReadouts/2).astype(int)-1,iRay]

        # Step 2: load m,n into nmMatrix and load gRay into vMatrix
        nmMatrix[:,iRay] = (nRay,mRay)
        vMatrix[:,:,iRay] = logm(gRay)


    # Step 3: pseudo-invert nmMatrix and multiply by vMatrix to get ln(Gx) and
    # ln(Gy) for each element
    logGx = np.zeros((nCoils,nCoils),dtype='complex')
    logGy = np.zeros((nCoils,nCoils),dtype='complex')
    for row in range(nCoils):
        for col in range(nCoils):
            logResult = np.linalg.pinv(nmMatrix).T.dot(np.squeeze(vMatrix[row,col,:])).squeeze()
            logGx[row,col],logGy[row,col] = logResult[:]

    # Step 4: solve for Gx and Gy by taking matrix exponent
    Gx = expm(logGx)
    Gy = expm(logGy)

    return(Gx,Gy)


if __name__ == '__main__':
    from scipy.io import loadmat
    data = loadmat('test/test_grog_data_4D.mat')
    traj = data['testTrajectory3D']
    kspace = data['testData4D']

    Gx,Gy = scgrog(kspace,traj)

    # Test it against the known truth
    data = loadmat('test/gx_gy_results.mat')
    Gxm = data['officialGx']
    Gym = data['officialGy']

    assert(np.allclose(Gx,Gxm) == True)
    assert(np.allclose(Gy,Gym) == True)
