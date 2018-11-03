import numpy as np
import warnings # We know skimage will complain about importing imp...
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

def grappa2d(coil_ims,sens,acs,Rx,Ry,kernel_size=(3,3)):

    # We get coil ims in and we want these in kspace
    kspace_d = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(coil_ims),axes=(1,2)))

    # Separate the autocalibration region into patches to get source matrix
    N = sens.shape[0] # number of coils
    S0 = np.zeros((N,(acs.shape[1]-2)*(acs.shape[2]-2),kernel_size[0]*kernel_size[1]),dtype='complex')
    for ii in range(N):
        S0[ii,:,:] = view_as_windows(np.ascontiguousarray(acs[ii,:,:]),kernel_size).reshape((S0.shape[1],S0.shape[2]))

    # Remove the unknown values.  The remaiming values form source matrix,
    # S, for each coil
    S_temp = S0[:,:,[0,1,2,6,7,8]]
    S = np.hstack(S_temp[:])

    # The middle pts form target vector, T, for each coil
    T = S0[:,:,4].T

    # Invert S to find weights, W
    W = np.linalg.pinv(S).dot(T)

    # Now onto the forward problem to fill in the missing lines...

    # Make patches out of all acquired data (skip the missing lines)
    S0 = np.zeros((N,int((kspace_d.shape[1]-2)/Rx)*int((kspace_d.shape[2]-2)/Ry),kernel_size[0]*kernel_size[1]),dtype='complex')
    for ii in range(N):
        S0[ii,:,:] = view_as_windows(np.ascontiguousarray(kspace_d[ii,:,:]),kernel_size,step=(Rx,Ry)).reshape((S0.shape[1],S0.shape[2]))

    # Remove the unknown values.  The remaiming values form source matrix,
    # S, for each coil
    S_new_temp = S0[:,:,[0,1,2,6,7,8]]
    S_new = np.hstack(S_new_temp[:])

    # Now it's a forward problem to find missing values
    T_new = S_new.dot(W)

    # Back fill in the missing lines to recover the image
    lines = np.reshape(T_new.T,(N,-1,coil_ims.shape[2]-2))
    kspace_d[:,1:-1:Rx,1:-1] = lines

    # put the coil images back in image space and send it back
    recon = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(kspace_d),axes=(1,2)))
    return(recon)


if __name__ == '__main__':
    pass
