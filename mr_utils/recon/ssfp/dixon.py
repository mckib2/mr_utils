'''Collection of Dixon fat/water separation methods.

Implementations of methods described in Berstein (see function docstrings for
references).
'''

import numpy as np

def dixon_2pt(IP, OP):
    '''Naive two-point Dixon method of fat/water separation.

    Parameters
    ==========
    IP : array_like
        In-phase image (corresponding to 0).
    OP : array_like
        Out-of-phase image (corresponding to pi).

    Returns
    =======
    W : array_like
        water image
    F : array_like
        fat image

    Notes
    =====
    "[This implementation] ignores additional image weighting from T2*
    relaxation, diffusion, and flow and from other phase shifts that could
    arise from hardware group delays, eddy currents, and B1 receive-field
    nonuniformity. We have also ignored the water-fat chemical shift
    separation in both the slice and readout directions" [1]_.

    Implements method described in [1]_.  Also equations [17.52] in [2]_.

    References
    ==========
    .. [1] Dixon, W. T. (1984). Simple proton spectroscopic imaging. Radiology,

    .. [2] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    W = (IP + OP)/2
    F = (IP - OP)/2
    return(W, F)

def dixon_pc(IP, OP, method='vanilla'):
    '''Methods to determine pc, fat/water fraction within a voxel.

    Parameters
    ==========
    IP : array_like
        In-phase image (corresponding to 0).
    OP : array_like
        Out-of-phase image (corresponding to pi).
    method : {'vanilla', 'glover', 'chen'}, optional
        Method to determine pc.  See notes.

    Returns
    =======
    pc : array_like
        Fat/water fraction.

    Raises
    ======
    NotImplementedError
        When incorrect value for `method` used.

    Notes
    =====
    method:
    - 'vanilla': sign of W - F.
    - 'glover': maintain continuous image appearance by using cont. p value.
    - 'chen': alternative that performs 'glover' and then discretizes.

    'glover' is implementation of eq [17.62], 'chen' is implementation of eq
    [17.64-65], 'vanilla' is eq [17.54] from [3]_.

    References
    ==========
    .. [3] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    if method == 'glover':
        pc = np.real(OP)/np.abs(OP)

    elif method == 'chen':
        def Hc(x):
            if x > .5:
                return 1
            if x > -0.5:
                return 0
            # else...
            return -1
        pc = Hc(np.real(OP)/np.abs(OP))

    elif method == 'vanilla':
        pc = np.where(np.abs(IP) - np.abs(OP) > 0, 1, -1)

    else:
        raise NotImplementedError()

    return pc

def dixon_2pt_mag(IP, OP):
    '''Solution to two-point Dixon method using magnitude of images.

    Parameters
    ==========
    IP : array_like
        In-phase image (corresponding to 0).
    OP : array_like
        Out-of-phase image (corresponding to pi).

    Returns
    =======
    abs(W) : array_like
        water image
    abs(F) : array_like
         fat image

    Notes
    =====
    Implements equations [17.53-54] in [4]_.

    References
    ==========
    .. [4] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    # If more water than fat, then p should be 1, else -1
    p = dixon_pc(IP, OP, 'vanilla')

    # All phase information will be lost
    pOP = p*np.abs(OP)
    W = (np.abs(IP) + pOP)/2
    F = (np.abs(IP) - pOP)/2
    return(W, F)

def dixon_extended_2pt(IP, OP, method='glover'):
    '''Extended two-point Dixon method for fat/water separation.

    Parameters
    ==========
    IP : array_like
        In-phase image (corresponding to 0).
    OP : array_like
        Out-of-phase image (corresponding to pi).
    method : {'vanilla', 'glover', 'chen'}, optional
        Method to use to determine pc, see dixon_pc().

    Returns
    =======
    abs(W) : array_like
        water image
    abs(F) : array_like
        fat image

    Notes
    =====
    Extended 2PD attempts to address the B0 homogeneity problem by using a
    generalized pc.

    Implements equations [17.63] in [5]_.

    References
    ==========
    .. [5] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    pc = dixon_pc(IP, OP, method)
    pcOP = pc*np.abs(OP)
    W = (np.abs(IP) + pcOP)/2
    F = (np.abs(IP) - pcOP)/2
    return(W, F)

def dixon_3pt(IP, OP1, OP2, use_2pi=True, method='glover'):
    '''Three point Dixon method of fat/water separation.

    Parameters
    ==========
    IP : array_like
        In-phase image (corresponding to 0).
    OP1 : array_like
        Out-of-phase image (corresponding to pi).
    OP2 : array_like
        Out-of-phase image (corresponding to -pi or 2*pi).
    use_2pi : bool, optional
        Use 2*pi for OP2 instead of -pi.
    method : {'vanilla', 'glover', 'chen'}, optional
        Method to use to determine pc, see dixon_pc().

    Returns
    =======
    W : array_like
        water image
    F: array_like
        fat image
    B0 : array_like
        B0 inhomogeneity image.

    Notes
    =====
    "The phase difference between the two opposed-phase images is due
    to B0 inhomogeneity, and they are used to compute phi. The phi map is used
    to remove the B0 inhomogeneity phase shift from one of the opposed-phase
    images and thereby determine the dominant species for each pixel (i.e.,
    whether W > F, or vice versa)."

    Implements method described [6]_. Also implements equations [17.71] in
    [7]_.

    References
    ==========
    .. [6] Glover, G. H., & Schneider, E. (1991). Three‐point Dixon technique
           for true water/fat decomposition with B0 inhomogeneity correction.
           Magnetic resonance in medicine, 18(2), 371-383.

    .. [7] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    phi = np.angle(np.conj(IP)*OP2)/2
    if not use_2pi:
        # OP2 is a -pi phase
        OP1phi = OP1*np.exp(-1j*phi)
        W = (IP + OP1phi)/2
        F = (IP - OP1phi)/2
    else:
        # OP2 is a 2*pi - this is better!

        # Should we be using I0 instead of IP?  We loose complex with I0...
        pc = dixon_pc(IP, OP1, method)
        I0 = np.sqrt(np.abs(IP)*np.abs(OP2))
        pcOP1 = pc*np.abs(OP1)
        W = (I0 + pcOP1)/2
        F = (I0 - pcOP1)/2

    return(W, F, phi)

def dixon_3pt_eam(I0, I1, I2, method='glover'):
    '''Three point Dixon including echo amplitude modulation (EAM).

    Parameters
    ==========
    I0 : array_like
        In-phase image (corresponding to phi_0 phase).
    I1 : array_like
        Out-of-phase image (corresponding to phi_0 + phi).
    I2 : array_like
        Out-of-phase image (corresponding to phi_0 + 2*phi).
    method : {'vanilla', 'glover', 'chen'}, optional
        Method to use to determine pc, see dixon_pc().

    Returns
    =======
    W : array_like
        water image
    F : array_like
        fat image
    A :array_like
        The susceptibility dephasing map.

    Notes
    =====
    "...under our assumptions, ignoring amplitude effects simply results in a
    multiplicative error in both water and fat components. This error is
    usually not serious and can be ignored...there is a SNR penalty for the
    amplitude correction, and it is best avoided unless there is a specific
    need to compute A for the application of interest" [8]_.

    Implements equations [17.78] from [8]_.

    References
    ==========
    .. [8] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    # Find A, the susceptibility dephasing map, and pc values
    A = np.sqrt(np.abs(I2)/np.abs(I0))
    pc = dixon_pc(I0, I1, method)

    pcI1 = pc*np.abs(I1)/A
    W = (np.abs(I0) + pcI1)/2
    F = (np.abs(I0) - pcI1)/2

    return(W, F, A)

def dixon_3pt_dpe(I0, I1, I2, theta):
    '''Three point Dixon using direct phase encoding (DPE).

    Parameters
    ==========
    I0 : array_like
        In-phase image (corresponding to phi_0 phase).
    I1 : array_like
        Out-of-phase image (corresponding to phi_0 + phi).
    I2 : array_like
        Out-of-phase image (corresponding to phi_0 + 2*phi).
    theta : float
        Phase term.

    Returns
    =======
    W : array_like
        Water image
    F : array_like
        Fat image.

    Notes
    =====
    Note that theta_0 + theta should not be a multiple of pi!

    Implements equations [17.83-84] from [9]_.

    References
    ==========
    .. [9] Notes from Bernstein, M. A., King, K. F., & Zhou, X. J. (2004).
           Handbook of MRI pulse sequences. Elsevier.
    '''

    etheta = np.exp(1j*theta)
    delI = ((etheta + 1)**2 - 4*etheta*I0*I2)/(etheta - 1)

    W = np.abs((I1 + delI)/2)
    F = np.abs((I1 - delI)/2)

    return(W, F)
