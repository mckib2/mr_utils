import numpy as np

def multiphase(kspace):
    '''Acquire two phase-cycled images in one Cartesian acquisiton.

    The idea is to acquire kspace with even lines having phase-cycle \phi_0 and
    and odd lines having phase-cycle \phi_1.  Then split the lines up into
    two R=2 undersampled images and use parallel imaging reconstruction to
    recover the two separate phase-cycled images.

    kspace -- Even lines phase \phi_0, odd lines phase \phi_1.
    '''

    kspace_phi_0 = np.zeros(kspace.shape,dtype='complex')
    kspace_phi_1 = np.zeros(kspace.shape,dtype='complex')
    kspace_phi_0[::2,:] = kspace[::2,:]
    kspace_phi_1[1::2,:] = kspace[1::2,:]

    

if __name__ == '__main__':
    pass
