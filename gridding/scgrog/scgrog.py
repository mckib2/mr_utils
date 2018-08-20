import numpy as np
from scipy.linalg import fractional_matrix_power
from get_gx_gy import get_gx_gy

def grog_interp(kspace,Gx,Gy,traj,cartdims):
    '''Moves radial k-space points onto a cartesian grid via the GROG method.

    kspace    -- A 3D (sx,sor,soc) slice of k-space
    Gx,Gy     -- The unit horizontal and vertical cartesian GRAPPA kernels
    trak      -- k-space trajectory
    cartdims  -- (nrows,ncols), size of Cartesian grid
    '''

    sx,nor,noc = kspace.shape[:]
    nrows,ncols = cartdims[0:2]

    kxs = np.real(traj)*nrows
    kys = np.imag(traj)*ncols

    # Pre-allocate kspace_out with an extra row,col
    kspace_out = np.zeros((nrows+1,ncols+1,noc),dtype='complex')
    countMatrix = np.zeros((nrows+1,ncols+1))

    # Find nearest integer coordinates
    kxs_round = np.round(kxs)
    kys_round = np.round(kys)

    # Find
    dkxs = kxs_round - kxs
    dkys = kys_round - kys

    for ii in range(sx):
        for jj in range(nor):
            # Pull this point's multi-coil signal
            # thisInputSignal = kspace[ii,jj,:].squeeze()

            # Get distance - is it quicker if we truncate?
            # dkx = np.round(dkxs[ii,jj],decimals=5)
            # dky = np.round(dkys[ii,jj],decimals=5)
            # dkx = dkxs[ii,jj]
            # dky = dkys[ii,jj]

            # Shifted cartesian point, this is a time bottle-neck
            shiftedPoint = np.linalg.multi_dot([ fractional_matrix_power(Gx,dkxs[ii,jj]),fractional_matrix_power(Gy,dkys[ii,jj]),kspace[ii,jj,:] ])

            # Find matrix indices corresponding to k-space coordinates
            xx = int(kxs_round[ii,jj] + nrows/2)
            yy = int(kys_round[ii,jj] + ncols/2)

            # Load result into output matrix and bump the counter
            kspace_out[xx,yy,:] += shiftedPoint
            countMatrix[xx,yy] += 1

    # Lastly, use point-wise division of kspace_out by weightMatrix to average
    nonZeroCount = countMatrix > 0
    countMatrixMasked = countMatrix[nonZeroCount]
    for ii in range(noc):
        # Extract one coil
        coilSignal = kspace_out[:,:,ii]
        # Perform point-wise division
        coilSignal[nonZeroCount] /= countMatrixMasked
        # Store in output
        kspace_out[:,:,ii] = coilSignal

    # Regridding results in +1 size increase so drop first row,col arbitrarily
    kspace_out = kspace_out[1::,1::]

    return(kspace_out)

def scgrog(kspace,traj,Gx,Gy,cartdims=None):

    # If the user didn't give us the desired cartesian dimensions, guess
    if cartdims is None:
        cartdims = (kspace.shape[0],kspace.shape[0],kspace.shape[2],kspace.shape[3])

    # Permute time to end of 4D data for convenience
    if kspace.ndim == 4:
        kspace = np.transpose(kspace,(0,1,3,2))
        tmp = list(cartdims)
        tmp[2],tmp[3] = tmp[3],tmp[2]
        cartdims = tuple(tmp)

    # Interpolate frame-by-frame
    kspace_cart = np.zeros(cartdims,dtype='complex')
    for ii in range(kspace.shape[-1]):
        time_frame = kspace[:,:,:,ii]
        traj_frame = traj[:,:,ii]
        kspace_cart[:,:,:,ii] = grog_interp(time_frame,Gx,Gy,traj_frame,cartdims)

    # Permute back if needed
    if kspace_cart.ndim == 4:
        kspace_cart = np.transpose(kspace_cart,(0,1,3,2))

    # Create mask
    mask = (np.abs(kspace_cart) > 0)

    return(kspace_cart,mask)


if __name__ == '__main__':

    # Load in the test data
    from scipy.io import loadmat
    data = loadmat('test/test_gridder_data_4D.mat')['KSpaceData']
    kspace = data['kSpace'][0][0]
    traj = data['trajectory'][0][0]
    cartdims = tuple(list(data['cartesianSize'][0][0][0]))

    # First get Gx,Gy
    Gx,Gy = get_gx_gy(kspace,traj,cartdims=cartdims)

    # Check to make sure Gx,Gy are correct
    data = loadmat('test/test_gx_gy_data.mat')
    Gxm = data['Gx']
    Gym = data['Gy']

    assert(np.allclose(Gx,Gxm) == True)
    assert(np.allclose(Gy,Gym) == True)
    print('GET_GX_GY ran successfully!')

    # Now use Gx,Gy to regrid using grog
    kspace,mask = scgrog(kspace,traj,Gx,Gy,cartdims)

    # Check our work to see if it worked
    data = loadmat('test/grog_result.mat')
    kspacem = data['officialCartesianKSpace']
    maskm = data['officialKMask']
    assert(np.allclose(kspace,kspacem) == True)
    assert(np.allclose(mask,maskm) == True)
    print('SCGROG ran successfully!')
