import numpy as np
from tqdm import trange
from mr_utils import view

def ernst(TR,T1):
    '''Computes the Ernst angle.

    TR -- repetition time.
    T1 -- longitudinal exponential decay time constant.

    Implements equation [14.9] from:
        Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
        Handbook of MRI pulse sequences. Elsevier.
    '''

    # Don't divide by zero!
    alpha = np.zeros(T1.shape)
    idx = np.nonzero(T1)
    alpha[idx] = np.arccos(-TR/T1[idx])
    return(alpha)

def fzss(T1,TR,alpha=None):
    '''Dimensionless measure of steady-state longitudinal magnetization.

    T1 -- longitudinal exponential decay time constant.
    TR -- repetition time.
    alpha -- flip angle.

    alpha=None will use the Ernst angle.

    Implements equation [14.7] from:
        Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
        Handbook of MRI pulse sequences. Elsevier.
    '''

    if alpha is None:
        alpha = ernst(TR,T1)

    E1 = np.exp(-TR/T1)
    val = (1 - E1)/(1 - np.cos(alpha)*E1)
    return(val)

def spoiled_gre_k(T1,T2star,TR,TE,alpha=None,M0=1,k=1):
    '''Spoiled GRE contrast simulation for k excitation pulses.

    See spoiled_gre().
    k -- Number of excitation pulses the magnetization experiences.

    alpha=None will use the Ernst angle.

    Implements equations [14.10-11] from:
        Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
        Handbook of MRI pulse sequences. Elsevier.
    '''

    # Must have 1 or more excitations to do anything...
    assert(k > 0)

    # Some helper quantities
    E1 = np.exp(-TR/T1)
    E2 = np.exp(-TE/T2star)

    # If we are using ernst, then we have a closed form!
    if alpha is None:
        Sk = M0*np.sqrt((1 - E1)/(1 + E1))*(1 + E1**(2*k-1))*E2
    else:
        f = fzss(T1,TR,alpha)
        Sk = M0*np.sin(alpha)*(f + (np.cos(alpha)*E1)**(k-1)*(1 - f))*E2

    return(Sk)

def spoiled_gre(T1,T2star,TR,TE,alpha=None,M0=1):
    '''Spoiled, steady state GRE contrast simulation.

    T1 -- longitudinal exponential decay time constant.
    T2star -- Effective transverse exponential decay time constant.
    TR -- repetition time.
    TE -- echo time.
    alpha -- flip angle.
    M0 -- proton density.

    alpha=None will use the Ernst angle.

    Assuming a longitudinal steady-state and perfect spoiling. Note that
    dependence is on T2* rather than T2 because SE/STE formation is suppressed
    by spoiling and the signal is generated by gradient refocusing of an FID.

    Implements equation [14.8] from:
        Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
        Handbook of MRI pulse sequences. Elsevier.
    '''

    if alpha is None:
        alpha = ernst(TR,T1)

    # Make sure we don't divide by zero
    idx1 = np.nonzero(T1)
    idx2 = np.nonzero(T2star)
    E1 = np.zeros(T1.shape)
    E1[idx1] = np.exp(-TR/T1[idx1])
    E2 = np.zeros(T2star.shape)
    E2[idx2] = np.exp(-TE/T2star[idx2])

    # Do the thing:
    S = M0*np.sin(alpha)*(1 - E1)*E2/(1 - np.cos(alpha)*E1)
    return(S)

def gre_sim_loop(T1,T2,TR=12e-3,TE=6e-3,alpha=np.pi/3,field_map=None,dphi=0,M0=1,iter=200):
    '''Simulate GRE pulse sequence.

    T1 -- longitudinal exponential decay time constant.
    T2 -- Transverse exponential decay time constant.
    TR -- repetition time.
    TE -- echo time.
    alpha -- flip angle.
    field_map -- offresonance field map (in hertz).
    dphi -- phase  cycling of RF pulses.
    M0 -- proton density.
    iter -- number of excitations till steady state.

    '''

    if field_map is None:
        field_map = np.zeros(T1.shape)

    # Rotation matrix each Rx pulse
    rxalpha = np.array([ [1,0,0],[0,np.cos(alpha),np.sin(alpha)],[0,-np.sin(alpha),np.cos(alpha)] ])

    # Make everythinig a 1D vector, save the original size so we can hand that
    # back to the caller
    orig_size = T1.shape[:]
    field_map = field_map.flatten()
    T1 = T1.flatten()
    T2 = T2.flatten()
    M0 = M0.flatten()

    # Make sure we don't divide by zero...
    idx1 = np.nonzero(T1)
    idx2 = np.nonzero(T2)
    E1 = np.zeros(T1.shape)
    E2 = np.zeros(T2.shape)
    E3 = np.zeros(T2.shape)
    E1[idx1] = np.exp(-TR/T1[idx1])
    E2[idx2] = np.exp(-TR/T2[idx2])
    E3[idx2] = np.exp(-TE/T2[idx2])

    Mgre = np.zeros((3,T1.size))
    for ii in trange(T1.size,desc='GRE steady-state'):
        # first flip
        phi = 0
        rzdphi = np.array([ [np.cos(phi),np.sin(phi),0],[-np.sin(phi),np.cos(phi),0],[0,0,1] ])
        rznegdphi = np.array([ [np.cos(-phi),np.sin(-phi),0],[-np.sin(-phi),np.cos(-phi),0],[0,0,1] ])
        Mgre[:,ii] = np.array([0,0,1])*M0[ii]

        # This used to reference M, but I think this was a mistake
        Mgre[:,ii] = np.linalg.multi_dot((rzdphi,rxalpha,rznegdphi,Mgre[:,ii]))

        # assume steady state after 200 flips
        tmp = np.zeros((3,iter))
        tmp[:,0] = Mgre[:,ii]
        for n in range(1,iter):

            # relaxation
            tmp[0,n] = tmp[0,n-1]*E2[ii] # x
            tmp[1,n] = tmp[1,n-1]*E2[ii] # y
            tmp[2,n] = 1 + (tmp[2,n-1] - 1)*E1[ii] # z

            # convert offres into angle to tip
            cycles = field_map[ii]*TR
            rotation_angle = np.fmod(cycles,1)*2*np.pi
            rzoffres = np.array([ [np.cos(rotation_angle),np.sin(rotation_angle),0],[-np.sin(rotation_angle),np.cos(rotation_angle),0],[0,0,1] ])
            tmp[:,n] = rzoffres.dot(tmp[:,n]) # dephase by offres

            # next tip
            # delete phase information! to make it gre
            tmp[0,n] = 0
            tmp[1,n] = 0

            # will got over 2*pi but shouldn't matter
            phi += dphi

            rzdphi = np.array([ [np.cos(phi),np.sin(phi),0],[-np.sin(phi),np.cos(phi),0],[0,0,1] ])
            rznegdphi = np.array([ [np.cos(-phi),np.sin(-phi),0],[-np.sin(-phi),np.cos(-phi),0],[0,0,1] ])
            tmp[:,n] = np.linalg.multi_dot((rzdphi,rxalpha,rznegdphi,tmp[:,n]))

        # take steady state sample and relax in TE
        Mgre[0,ii] = tmp[0,-1]*E3[ii]
        Mgre[1,ii] = tmp[1,-1]*E3[ii]


        cycles = field_map[ii]*TE
        rotation_angle = np.fmod(cycles,1)*2*np.pi
        rzoffres = np.array([ [np.cos(rotation_angle),np.sin(rotation_angle),0],[-np.sin(rotation_angle),np.cos(rotation_angle),0],[0,0,1] ])
        Mgre[:,ii] = rzoffres.dot(Mgre[:,ii])

    # We want the complex transverse magnetization
    Mxy = (Mgre[0,:] + 1j*Mgre[1,:]).reshape(orig_size)
    return(Mxy)


def gre_sim(T1,T2,TR=12e-3,TE=6e-3,alpha=np.pi/3,field_map=None,dphi=0,M0=1,tol=1e-5,iter=None):
    '''Simulate GRE pulse sequence.

    T1 -- longitudinal exponential decay time constant.
    T2 -- Transverse exponential decay time constant.
    TR -- repetition time.
    TE -- echo time.
    alpha -- flip angle.
    field_map -- offresonance field map (in hertz).
    dphi -- phase  cycling of RF pulses.
    M0 -- proton density.
    tol -- Maximum difference between voxel intensity iter to iter until stop.
    iter -- number of excitations till steady state.

    iter=None will run until difference between all voxel intensities iteration
    to iteration is within given tolerance, tol (default=1e-5).

    Returns complex transverse magnetization (Mx + 1j*My)
    '''

    if field_map is None:
        field_map = np.zeros(T1.shape)

    # We have 2 states: current, previous iteration
    Mgre = np.zeros((3,2) + T1.shape)
    Mgre[2,0,...] = M0

    # Rotation matrix each Rx pulse
    rxalpha = np.array([ [1,0,0],[0,np.cos(alpha),np.sin(alpha)],[0,-np.sin(alpha),np.cos(alpha)] ])

    # first flip
    phi = 0
    c_phi,s_phi = np.cos(phi),np.sin(phi)
    rzdphi = np.array([ [c_phi,s_phi,0],[-s_phi,c_phi,0],[0,0,1] ])
    rznegdphi = np.array([ [c_phi,-s_phi,0],[s_phi,c_phi,0],[0,0,1] ])
    rot_vec = np.linalg.multi_dot((rzdphi,rxalpha,rznegdphi))
    Mgre[:,0,...] = np.tensordot(rot_vec,Mgre[:,0,...],axes=1)

    # Precompute some values we each loop, making sure we don't divide by zero
    idx1 = np.nonzero(T1)
    idx2 = np.nonzero(T2)
    E1 = np.zeros(T1.shape)
    E2 = np.zeros(T2.shape)
    E1[idx1] = np.exp(-TR/T1[idx1])
    E2[idx2] = np.exp(-TR/T2[idx2])
    cycles = field_map*TR
    rotation_angle = np.fmod(cycles,1)*2*np.pi
    c_ra = np.cos(rotation_angle)
    s_ra = np.sin(rotation_angle)

    # Heavy lifting function run each iteration
    def iter_fun(Mgre,phi=0):
        # relaxation
        Mgre[0,1,...] = Mgre[0,0,...]*E2 # x
        Mgre[1,1,...] = Mgre[1,0,...]*E2 # y
        Mgre[2,1,...] = 1 + (Mgre[2,0,...] - 1)*E1 # z

        # Here's where we spend most of our time:
        for idx,fm in np.ndenumerate(field_map):
            rzoffres = np.array([ [c_ra[idx[0],idx[1]],s_ra[idx[0],idx[1]],0],[-s_ra[idx[0],idx[1]],c_ra[idx[0],idx[1]],0],[0,0,1] ])
            Mgre[:,1,idx[0],idx[1]] = rzoffres.dot(Mgre[:,1,idx[0],idx[1]])

        # next tip - delete phase information! to make it gre
        Mgre[0,1,...] = 0
        Mgre[1,1,...] = 0

        # will got over 2*pi but shouldn't matter
        phi += dphi

        c_phi,s_phi = np.cos(phi),np.sin(phi)
        rzdphi = np.array([ [c_phi,s_phi,0],[-s_phi,c_phi,0],[0,0,1] ])
        rznegdphi = np.array([ [c_phi,-s_phi,0],[s_phi,c_phi,0],[0,0,1] ])
        rot_vec = np.linalg.multi_dot((rzdphi,rxalpha,rznegdphi))
        Mgre[:,1,...] = np.tensordot(rot_vec,Mgre[:,1,...],axes=1)

        # Update prev iteration
        Mgre[:,0,...] = Mgre[:,1,...]

        return(Mgre,phi)

    # Do either fixed number of iter or until tolerance achieved
    if iter is not None:
        # assume steady state after iter flips
        for n in trange(iter,desc='GRE steady-state'):
            Mgre,phi = iter_fun(Mgre,phi)
    else:
        # Run until all voxels within tolerance
        Mgre_prev = np.ones(Mgre.shape)*np.inf
        stop_cond = False
        while not stop_cond:
            Mgre,phi = iter_fun(Mgre,phi)
            stop_cond = np.any(np.abs(Mgre - Mgre_prev) < tol)
            Mgre_prev = Mgre


    # take steady state sample and relax in TE
    Mss = np.zeros((3,) + T1.shape)
    E2 = np.zeros(T2.shape)
    E2[idx2] = np.exp(-TE/T2[idx2])
    Mss[0,...] = Mgre[0,-1,...]*E2
    Mss[1,...] = Mgre[1,-1,...]*E2
    Mss[2,...] = Mgre[2,-1,...]

    cycles = field_map*TE
    rotation_angle = np.fmod(cycles,1)*2*np.pi
    c_ra,s_ra = np.cos(rotation_angle),np.sin(rotation_angle)
    for idx,fm in np.ndenumerate(field_map):
        rzoffres = np.array([ [c_ra[idx[0],idx[1]],s_ra[idx[0],idx[1]],0],[-s_ra[idx[0],idx[1]],c_ra[idx[0],idx[1]],0],[0,0,1] ])
        Mss[:,idx[0],idx[1]] = rzoffres.dot(Mss[:,idx[0],idx[1]])

    return(Mss[0,...] + 1j*Mss[1,...])
