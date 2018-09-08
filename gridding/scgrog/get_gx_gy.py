import numpy as np
from scipy.linalg import logm,expm

def get_gx_gy(kspace,traj=None,kxs=None,kys=None,cartdims=None):
    '''Compute Self Calibrating GRAPPA Gx and Gy operators.
    '''

    # We need either traj OR kxs,kys
    assert((traj is not None) or (kxs is not None and kys is not None))

    # If the user didn't give us the desired cartesian dimensions, guess
    if cartdims is None:
        cartdims = (kspace.shape[0],kspace.shape[0])

    # Flatten the rays and get kspace trajectory in terms of kx,ky
    sx,nor,nof,nc = kspace.shape[:]
    nrays = nor*nof
    kspace = np.reshape(kspace,(sx,nrays,nc))
    if traj is not None:
        traj = np.reshape(traj,(sx,nrays))
        kxs = cartdims[0]*np.real(traj)
        kys = cartdims[1]*np.imag(traj)
    else:
        kxs = np.reshape(kxs,(sx,nrays))
        kys = np.reshape(kys,(sx,nrays))

    # Create logG ray-by-ray
    logG = np.zeros((nc,nc,nrays),dtype='complex')
    for ii in range(nrays):
        # Master Equation: targetData = gRay*sourceData
        #
        # Since we're grabbing just 1 ray from our 3D slice, targetData becomes
        # a (SX-1)x1xNC thing. But what we need is for targetData
        # and sourceData to be NCx(SX-1), so squeeze and transpose
        target = kspace[1::,ii,:].squeeze().T
        source = kspace[0:-1:,ii,:].squeeze().T

        # Now solve targetData = G*sourceData where G is an NCxNC
        # grappa-like coefficients matrix for that ray (we'll combine
        # all of the Gs from all rays later)
        G = target.dot(np.linalg.pinv(source))

        # Step 1: load G into vMatrix
        logG[:,:,ii] = logm(G)

    # Step 2: compute the pseudo-inverse of nmMatrix outside of the loop
    dkxs = kxs[1,:] - kxs[0,:]
    dkys = kys[1,:] - kys[0,:]
    dks = np.vstack((dkxs,dkys)).T
    nmMatrix_pinv = np.linalg.pinv(dks)

    # Step 3: multiply by vMatrix to get ln(Gx) and ln(Gy) for each element
    logGx = np.zeros((nc,nc),dtype='complex')
    logGy = np.zeros((nc,nc),dtype='complex')
    for row in range(nc):
        for col in range(nc):
            res = nmMatrix_pinv.dot(np.squeeze(logG[row,col,:]))
            logGx[row,col],logGy[row,col] = res[:]

    # Step 4: solve for Gx and Gy by taking matrix exponent
    Gx = expm(logGx)
    Gy = expm(logGy)

    return(Gx,Gy)


if __name__ == '__main__':
    pass
